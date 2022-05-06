# -*- coding: utf-8 -*-
# --author-- lanhua.zhou
from functools import wraps,partial
import os
import time
import sys
import socket
import tempfile
import hashlib
import logging

from Qt import QtCore

logger = logging.getLogger(__file__)

BUFFER_SIZE = 1024*1024

def get_internal_trans_server_addr():
    import zfused_api
    _ip, _port = zfused_api.zFused.CLOUD_TRANS_SERVER_ADDR.split(":")
    return (_ip, int(_port))

def md5_for_file(f, block_size=2**20):
    with open(f) as fHandle:
        md5 = hashlib.md5()
        while True:
            data = fHandle.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()
    return md5.hexdigest()

def is_hash_equal(f1, f2):
    if f1 == f2:
        return True
    if os.path.isfile(f1) and os.path.isfile(f2):
        str1 = md5_for_file(f1)  
        str2 = md5_for_file(f2)  
        return str1 == str2 
    return False


# 添加回调进度百分比
# 类似指针
class Progress:
    value = 0

def trans( func ):
    @wraps(func)
    def wrap( *args, **kwargs ):
        global _socket
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect(get_internal_trans_server_addr())
        # Turn $gMainPane Off:
        # mel.eval("paneLayout -e -manage false $gMainPane")
        try:
            return func( *args, **kwargs )
        except Exception as e:
            # raise # will raise original error
            logger.warning(e)
        finally:
            _socket.close()
            # mel.eval("paneLayout -e -manage true $gMainPane")
    return wrap

# @trans
def send_file_to_server(src_file, dst_file, progress = [0]):
    if is_hash_equal(src_file, dst_file):
        return True

    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.connect(get_internal_trans_server_addr())
    try:
        _src_file = src_file
        _dst_file = dst_file
        _file_size = os.path.getsize(_src_file)
        _send_commond = "send {} {}".format(_dst_file, _file_size)
        _socket.send( _send_commond.encode() )
        data = _socket.recv(BUFFER_SIZE)
        if data.decode().startswith("start"):
            print("start send file")
            # send_file_to_server(_src_file, _socket)
            with open(src_file, "rb") as f:
                _send_data_size = 0
                _f_data = f.read(BUFFER_SIZE)
                while True:
                    _socket.send( _f_data )
                    _send_data_size += BUFFER_SIZE
                    if _send_data_size >= _file_size:
                        progress[0] = 100
                    else:
                        _send_progress = _send_data_size/_file_size
                        _progress_value =  "{:>02f}".format(_send_progress*100)
                        progress[0] = float(_progress_value)
                    #print(progress[0])
                    _f_data = f.read(BUFFER_SIZE)
                    if not _f_data:
                        progress[0] = 100
                        _socket.send("fileover".encode())
                        break
            # 接收反馈
            data = _socket.recv(BUFFER_SIZE)
            if data.decode().startswith("get "):
                print("send success")
                progress[0] = 100
                return True
            else:
                print("send fail")
                return False
    except:
        return False
    finally:
        _socket.close()

def get_file_from_server(src_file, dst_file, progress = [0]):
    if is_hash_equal(src_file, dst_file):
        return True

    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.connect(get_internal_trans_server_addr())
    try:
        _src_file = src_file
        _dst_file = dst_file
        # _file_size = os.path.getsize(_src_file)
        print(_src_file, _dst_file)
        _send_commond = "get {} {}".format(_src_file, _dst_file)
        print(_send_commond)
        _socket.send( _send_commond.encode() )
        data = _socket.recv(BUFFER_SIZE)
        arrayOfCommands = data.decode().split(" ")
        print(arrayOfCommands)
        if arrayOfCommands[0] == "send":
            # 判定文件是否存在
            _file_name = arrayOfCommands[1]
            if os.path.isfile(_file_name):
                _file_size = os.path.getsize(_file_name)
                if str(_file_size) == arrayOfCommands[2]:
                    return True
            _file_size = int(arrayOfCommands[2])
            # 开始接受文件
            _socket.send( "start ".encode() )

            # 创建文件夹
            _dir_name = os.path.dirname(_dst_file)
            if not os.path.isdir(_dir_name):
                os.makedirs(_dir_name)

            _get_byte = 0
            with open(_dst_file, "wb") as f:
                while True: 
                    # progress
                    # print(progress[0])
                    if _get_byte >= _file_size:
                        progress[0] = 100
                    else:
                        _send_progress = _get_byte/_file_size
                        _progress_value =  "{:>02f}".format(_send_progress*100)
                        progress[0] = float(_progress_value)
                    #print(progress[0])
                    _recv = _socket.recv(BUFFER_SIZE)                    
                    _length = len(_recv)
                    if _length <= 0:
                        break
                    if _length < 8 :
                        # 补全
                        _get_byte += (_length - 8)
                        a = "fileover"
                        print("nali ")
                        if _get_byte >= _file_size:
                            if a[8-_length:8] == _recv[0:_length].decode():
                                f.truncate(_get_byte)
                                break
                        else:
                            f.write(_recv[0:_length])
                            _get_byte += 8
                    else:
                        res = _recv[(_length - 8):_length]
                        try:
                            if res.decode() == "fileover":
                                f.write(_recv[0: (_length - 8)]) 
                                break
                            else:
                                f.write(_recv[0:_length])
                                _get_byte += _length
                        except:
                            f.write(_recv[0:_length])
                            _get_byte += _length

                # print(_get_byte)
            # 接收反馈
            _socket.send( "get {}".format(_get_byte).encode() )   
            progress[0] = 100      
            return True
    except Exception as e:
        print(e)
        return False
    finally:
        _socket.close()

class FileTransfer(QtCore.QObject):
    progress_started = QtCore.Signal()
    progress_changed = QtCore.Signal(float)
    progress_finished = QtCore.Signal(bool)

    def __init__(self, src_file, dst_file):
        super(FileTransfer, self).__init__()

        self._src_file = src_file
        self._dst_file = dst_file

    def upload(self):
        if is_hash_equal(src_file, dst_file):
            return True

        self.progress_started.emit()
        print("start ...")
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect(get_internal_trans_server_addr())
        try:
            _file_size = os.path.getsize(self._src_file)
            _send_commond = "send {} {}".format(self._dst_file, _file_size)
            _socket.send( _send_commond.encode() )
            data = _socket.recv(BUFFER_SIZE)
            if data.decode().startswith("start"):
                print("start send file")
                _progress_value = 0
                with open(self._src_file, "rb") as f:
                    _send_data_size = 0
                    _f_data = f.read(BUFFER_SIZE)
                    while True:
                        _socket.send( _f_data )
                        _send_data_size += BUFFER_SIZE
                        if _send_data_size >= _file_size:
                            _progress_value = 100
                        else:
                            _send_progress = _send_data_size/_file_size
                            _progress_value =  float("{:>02f}".format(_send_progress*100))
                        _f_data = f.read(BUFFER_SIZE)
                        if not _f_data:
                            _progress_value = 100
                            _socket.send("fileover".encode())
                            break
                        print(_progress_value)
                        self.progress_changed.emit(_progress_value)
                # 接收反馈
                data = _socket.recv(BUFFER_SIZE)
                if data.decode().startswith("get "):
                    print("send success")
                    progress[0] = 100
                    # return True
                    self.progress_finished.emit(True)
                else:
                    print("send fail")
                    # return False
                    self.progress_finished.emit(False)
        except:
            # return False
            self.progress_finished.emit(False)
        finally:
            _socket.close()         

    def download(self):
        if is_hash_equal(src_file, dst_file):
            return True

        self.progress_started.emit()
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect(get_internal_trans_server_addr())
        try:
            _send_commond = "get {} {}".format(self._src_file, self._dst_file)
            _socket.send( _send_commond.encode() )
            data = _socket.recv(BUFFER_SIZE)
            arrayOfCommands = data.decode().split(" ")
            if arrayOfCommands[0] == "send":
                # 判定文件是否存在
                _file_name = arrayOfCommands[1]
                if os.path.isfile(_file_name):
                    _file_size = os.path.getsize(_file_name)
                    if str(_file_size) == arrayOfCommands[2]:
                        self.progress_finished.emit(True)
                        return True
                _file_size = int(arrayOfCommands[2])
                # 开始接受文件
                _socket.send( "start ".encode() )
                # 创建文件夹
                _dir_name = os.path.dirname(self._dst_file)
                if not os.path.isdir(_dir_name):
                    os.makedirs(_dir_name)
                _get_byte = 0
                _progress_value = 0
                with open(self._dst_file, "wb") as f:
                    while True:
                        if _get_byte >= _file_size:
                            _progress_value = 100
                        else:
                            _send_progress = _get_byte/_file_size
                            _progress_value =  float("{:>02f}".format(_send_progress*100))
                        _recv = _socket.recv(BUFFER_SIZE)                    
                        _length = len(_recv)
                        if _length <= 0:
                            break
                        if _length < 8 :
                            # 补全
                            _get_byte += (_length - 8)
                            a = "fileover"
                            if _get_byte >= _file_size:
                                if a[8-_length:8] == _recv[0:_length].decode():
                                    f.truncate(_get_byte)
                                    break
                            else:
                                f.write(_recv[0:_length])
                                _get_byte += 8
                        else:
                            res = _recv[(_length - 8):_length]
                            try:
                                if res.decode() == "fileover":
                                    f.write(_recv[0: (_length - 8)]) 
                                    break
                                else:
                                    f.write(_recv[0:_length])
                                    _get_byte += _length
                            except:
                                f.write(_recv[0:_length])
                                _get_byte += _length
                        self.progress_changed.emit(_progress_value)
                    print(_get_byte)
                # 接收反馈
                _socket.send( "get {}".format(_get_byte).encode() )   
                self.progress_finished.emit(True)

        except Exception as e:
            self.progress_finished.emit(False)
        finally:
            _socket.close()



if __name__ == "__main__":
    # HOST = "47.103.77.93:7005"
    _s_t = time.clock()
    import zfused_api
    zfused_api.zFused.CLOUD_TRANS_SERVER_ADDR = "47.103.77.93:7005"
    # send_file_to_server(_src_file, _dst_file, Progress.value)

    from PySide2 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)

    _label = QtWidgets.QLabel()
    _label.show()

    _dst_file = "D:/storage.zip"
    _src_file = "D:/storage.zip"
    #print(time.strftime("/%Y_%m/%d/%H_%M_%S"))
    a = [0]
    _file_transfer = FileTransfer(_dst_file, _src_file)
    
    def p(v):
        _label.setText(str(v))

    _file_transfer.progress_changed.connect(p)


    _thread = QtCore.QThread(_label)
    _file_transfer.moveToThread(_thread)
    _thread.started.connect(_file_transfer.download)
    _file_transfer.progress_finished.connect(_thread.quit)
    # _file_transfer.progress_changed.connect()
    _thread.start()
    # _file_transfer.download()

    # ['send', 'C:\\Users\\LANHUA~1.ZHO\\AppData\\Local\\Temp/storage/review/video/2020/03/19/c714bae6a00c37357195e2df387dca65.webm', '46575515', 'c714bae6a00c37357195e2df387dca65']
    # print(send_file_to_server(_dst_file, _src_file, a))
    _e_t = time.clock()
    # print("asset cache time = " + str(1000*(_e_t - _s_t)) + "ms")
