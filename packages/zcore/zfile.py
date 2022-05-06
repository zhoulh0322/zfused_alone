# coding:utf-8
# --author-- lanhua.zhou

import os
import time
import threading
import shutil
import hashlib
import tempfile
import uuid

from PIL import Image

from Qt import QtGui,QtCore

import zfused_api
from . import video
from . import transfer

from .support import *

# 文件最大接受字节
FILE_MAX_SIZE = 1024*1024*50 #52428800

# 计算文件md5值
def md5_for_file(f, block_size=2**20):
    with open(f, 'rb') as fHandle:
        md5 = hashlib.md5()
        while True:
            data = fHandle.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()
    return md5.hexdigest()

def get_file_info(src_file, dst_file):
    _file_information = {}

    _file_information["path"] = dst_file
    _file_information["name"] = os.path.basename(dst_file)

    _size = os.path.getsize(src_file)
    _file_information["size"] = _size

    _md5 = md5_for_file(src_file)
    _file_information["md5"] = _md5
    
    _format = src_file.split(".")[-1]
    _file_information["format"] = _format
    
    _suffix = os.path.splitext(src_file)[-1]
    _file_information["suffix"] = _suffix

    return _file_information

class download(QtCore.QThread):
    progress_started = QtCore.Signal()
    progress_changed = QtCore.Signal(float)
    progress_finished = QtCore.Signal(bool)
    def __init__(self, parent, src_file, dst_file, progress_value):
        super(download, self).__init__(parent)

        self._src_file = src_file
        self._dst_file = dst_file
        self._progress_value = progress_value

    def run(self):
        self.progress_started.emit()
        _err = transfer.get_file_from_server(self._src_file, self._dst_file, self._progress_value, self)
        if _err:
            self._progress_value = [100]
            self.progress_finished.emit(True)
        else:
            self.progress_finished.emit(False)


class CloudFile(QtCore.QObject):
    progress_started = QtCore.Signal()
    progress_changed = QtCore.Signal(float)
    progress_finished = QtCore.Signal(bool)
    def __init__(self, file_database, parent = None):
        super(CloudFile, self).__init__(parent)

        self._file_database = file_database

        self._cloud_file = self._file_database["Path"]
        _temp_dir = tempfile.gettempdir()
        # self._file = "{}/{}".format(_temp_dir, self._cloud_file)
        _file_path = os.path.dirname(self._cloud_file)
        self._file = "{}/{}/{}".format(_temp_dir, _file_path, self._file_database["Name"])
        self._md5 = self._file_database["MD5"]

        self._file_type = "image"
        self._is_image = os.path.splitext(self._file)[-1] in SUPPORT_IMAGE
        self._is_video = os.path.splitext(self._file)[-1] in SUPPORT_VIDEO

        self._video_image_path = ""

        self._local_thumbnail_path = ""
        self._cloud_thumbnail_path = self._file_database["ThumbnailPath"]

        # self._progress = [0]
        self._file_transfer = transfer.FileTransfer(self._cloud_file, self._file)
        self._file_transfer.progress_started.connect(self.progress_started.emit)
        self._file_transfer.progress_changed.connect(self.progress_changed.emit)
        self._file_transfer.progress_finished.connect(self.progress_finished.emit)
        self._transfer_thread = QtCore.QThread(self)
        self._file_transfer.moveToThread(self._transfer_thread)
        self._file_transfer.progress_finished.connect(self._transfer_thread.quit)
        self._transfer_thread.started.connect(self._file_transfer.download)

    def cloud_thumbnail_path(self):
        return self._cloud_thumbnail_path

    def md5(self):
        return self._md5

    def file_md5(self):
        return self._md5

    def file_type(self):
        return self._file_type

    def file_format(self):
        _suffix = os.path.splitext(self._file)[-1]
        _format = FORMAT_SUFFIX[_suffix]
        return _format

    def file_name(self):
        return os.path.basename(self._file)

    def _get_size(self):
        return os.path.getsize(self._file)

    def _get_path(self):
        _suffix = os.path.splitext(self._file)[-1]
        _time_path = time.strftime("/%Y/%m/%d")
        return "storage/{}/{}/{}{}".format(self._file_type, _time_path, self._md5, _suffix)
    
    def _get_thumbnail_path(self):
        if self._is_video:
            _suffix = os.path.splitext(self._thumbnail_image)[-1]
            _md5 = md5_for_file(self._thumbnail_image)
            _time_path = time.strftime("/%Y/%m/%d")
            return "storage/{}/{}/{}{}".format(self._file_type, _time_path, _md5, _suffix)
        elif self._is_image:
            return self._get_path()
        return ""

    def thread_download(self):
        self.progress_started.emit()
        if os.path.isfile(self._file):
            _md5 = md5_for_file(self._file)
            if _md5 == self._md5:
                self.progress_finished.emit(True)
                return True
        self._transfer_thread.start()

        # self._progress = [0]
        # _download_thread = download(self, self._cloud_file, self._file, self._progress)
        # _download_thread.progress_started.connect(self.progress_started.emit)
        # _download_thread.progress_changed.connect(self.progress_changed.emit)
        # _download_thread.progress_finished.connect(self.progress_finished.emit)
        # _download_thread.start()
        # _download_thread.start()
        # _res = transfer.get_file_from_server(self._cloud_file, self._file, self._progress)
        # self.progress_finished.emit(_res)
        # return _res

    def download(self):
        self.progress_started.emit()
        if os.path.isfile(self._file):
            _md5 = md5_for_file(self._file)
            if _md5 == self._md5:
                self.progress_finished.emit(True)
                return True
        self._progress = [0]
        _res = transfer.get_file_from_server(self._cloud_file, self._file, self._progress)
        self.progress_finished.emit(_res)
        return _res

    def load(self):
        if self._is_image or self._is_video:
            _image = self._file_database["ThumbnailPath"].split("storage/")[-1]
            _url = "{}/{}".format(zfused_api.zFused.CLOUD_IMAGE_SERVER_ADDR, _image)
            req = requests.get(_url)
            _pixmap = QtGui.QPixmap()
            _pixmap.loadFromData(req.content)
            _pixmap = _pixmap.scaled(THUMNAIL_SIZE[0],THUMNAIL_SIZE[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.thumbnail_label.setPixmap(_pixmap)
        else:
            self._file_type = "doc"
            self.thumbnail_label.setStyleSheet("QLabel{background-color: #FF0000}")
        self.name_button.setText( self._file_database["Name"] )


class LocalFile(QtCore.QObject):
    progress_started = QtCore.Signal()
    progress_changed = QtCore.Signal(float)
    progress_finished = QtCore.Signal(bool)
    # def __init__(self, file_database, parent = None):
    #     super(CloudFile, self).__init__(parent)
    def __init__(self, file_path, theme = "", parent = None):
        super(LocalFile, self).__init__(parent)
        self._file = file_path
        self._theme = theme

        self._md5 = md5_for_file(self._file)

        self._file_type = "image"      # 默认image
        self._is_image = os.path.splitext(self._file)[-1] in SUPPORT_IMAGE
        self._is_video = os.path.splitext(self._file)[-1] in SUPPORT_VIDEO
        self._is_document = os.path.splitext(self._file)[-1] in SUPPORT_DOCUMENT

        self._video_image_path = ""

        self._local_thumbnail_path = ""
        self._cloud_thumbnail_path = ""

        self._init()

        print(self._file, self._get_path())
        self._file_transfer = transfer.FileTransfer(self._file, self._get_path())
        self._file_transfer.progress_started.connect(self.progress_started.emit)
        self._file_transfer.progress_changed.connect(self.progress_changed.emit)
        self._file_transfer.progress_finished.connect(self.progress_finished.emit)
        self._transfer_thread = QtCore.QThread(self)
        self._file_transfer.moveToThread(self._transfer_thread)
        self._file_transfer.progress_finished.connect(self._transfer_thread.quit)
        self._transfer_thread.started.connect(self._file_transfer.upload)
        
    def is_media(self):
        if self._is_image or self._is_video:
            return True
        return False

    def is_document(self):
        if self._is_document:
            return True
        return False

    def file_type(self):
        return self._file_type

    def file_format(self):
        _suffix = os.path.splitext(self._file)[-1]
        _format = FORMAT_SUFFIX[_suffix]
        return _format

    def file_md5(self):
        return self._md5

    def file_name(self):
        return os.path.basename(self._file)

    def _init(self):
        if self._is_image:
            self._file_type = "image"
            _pixmap = QtGui.QPixmap(self._file)
            tempDir = tempfile.gettempdir()
            self._local_thumbnail_path =  "{}/{}{}".format(tempDir,time.time(), os.path.splitext(self._file)[-1])
            shutil.copy(self._file, self._local_thumbnail_path)
            _pixmap = QtGui.QPixmap(self._local_thumbnail_path)
            _pixmap_save = _pixmap.scaled(200,200,QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            _pixmap_save.save(self._local_thumbnail_path)
        elif self._is_video:
            self._file_type = "video"
            # cut image
            tempDir = tempfile.gettempdir()
            self._video_image_path = "%s/%s_image.png"%(tempDir,time.time())
            self._local_thumbnail_path =  "%s/%s.png"%(tempDir,time.time())
            video.cut_image(self._file, self._local_thumbnail_path)
            video.cut_image(self._file, self._video_image_path)
            _pixmap = QtGui.QPixmap(self._local_thumbnail_path)
            _pixmap_save = _pixmap.scaled(200,200,QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            _pixmap_save.save(self._local_thumbnail_path)
        elif self._is_document:
            self._file_type = "document"

    def _get_size(self):
        return os.path.getsize(self._file)

    def _get_width(self):
        if self._is_image:
            return  Image.open(self._file).width
        elif self._is_video:
            return  Image.open(self._video_image_path).width
        return None

    def _get_height(self):
        if self._is_image:
            return  Image.open(self._file).height
        elif self._is_video:
            return  Image.open(self._video_image_path).height
        return None

    def get_local_thumbnail_size(self):
        return Image.open(self._local_thumbnail_path).size

    def _get_path(self):
        _suffix = os.path.splitext(self._file)[-1]
        _time_path = time.strftime("%Y/%m/%d")
        if not self._theme:
            _path = "storage/{}/{}/{}{}".format(self._file_type, _time_path, self._md5, _suffix)
        else:
            _path = "storage/{}/{}/{}/{}{}".format(self._theme, self._file_type, _time_path, self._md5, _suffix)
        return _path
    
    # def thumbnail_path(self):
    #     return self._get_thumbnail_path()

    def _get_thumbnail_path(self):
        if self._cloud_thumbnail_path:
            return self._cloud_thumbnail_path
        if self._local_thumbnail_path:
            _suffix = os.path.splitext(self._local_thumbnail_path)[-1]
            # _file_basename = os.path.basename(self._file)
            # _md5 = md5_for_file(self._local_thumbnail_path)
            _md5 = str(uuid.uuid1()).lower().replace('-','')
            _time_path = time.strftime("%Y/%m/%d")
            if not self._theme:
                _path = "storage/{}/{}/{}{}".format(self._file_type, _time_path, _md5, _suffix)
            else:
                _path = "storage/{}/{}/{}/{}{}".format(self._theme, self._file_type, _time_path, _md5, _suffix)
            self._cloud_thumbnail_path = _path
            return _path
        return ""

    def thread_upload(self):
        self.progress_started.emit()
        _file = zfused_api.zFused.get("file", filter = {"MD5": self._md5})
        if _file:
            self._cloud_thumbnail_path = _file[0]["ThumbnailPath"]
            self.progress_finished.emit(True)
            return True
        self._transfer_thread.start()

        if self._local_thumbnail_path:
            _progress = [0]
            _is_upload = transfer.send_file_to_server(self._local_thumbnail_path, self._get_thumbnail_path(), _progress)
            while True:
                if _progress[0] == 100:
                    break
        _suffix = os.path.splitext(self._file)[-1]
        _format = FORMAT_SUFFIX[_suffix]
        _size = self._get_size()
        _width = self._get_width()
        _height = self._get_height()

        # print(_suffix, _format, _size, _width, _height)
        _id,_err = zfused_api.file.new_file(self._md5, self._get_path(), os.path.basename(self._file), _format, _suffix, _size, self._get_thumbnail_path(), _width, _height)
        # print(_id, _err)
        if _id:
            return True
        else:
            return False


    def upload(self):
        _file = zfused_api.zFused.get("file", filter = {"MD5": self._md5})
        if _file:
            self._cloud_thumbnail_path = _file[0]["ThumbnailPath"]
        else:
            _progress = [0]
            _is_upload = transfer.send_file_to_server(self._file, self._get_path(), _progress)
            while True:
                if _progress[0] == 100:
                    break
            if self._local_thumbnail_path:
                _progress = [0]
                _is_upload = transfer.send_file_to_server(self._local_thumbnail_path, self._get_thumbnail_path(), _progress)
                while True:
                    if _progress[0] == 100:
                        break
                # self._cloud_thumbnail_path = self._get_thumbnail_path()
        _suffix = os.path.splitext(self._file)[-1]
        _format = FORMAT_SUFFIX[_suffix]
        _size = self._get_size()
        _width = self._get_width()
        _height = self._get_height()

        print(_suffix, _format, _size, _width, _height)
        _id,_err = zfused_api.file.new_file(self._md5, self._get_path(), os.path.basename(self._file), _format, _suffix, _size, self._get_thumbnail_path(), _width, _height)
        print(_id, _err)
        if _id:
            return True
        else:
            return False