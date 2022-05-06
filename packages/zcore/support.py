# coding:utf-8
# --author-- lanhua.zhou

import hashlib

# SUPPORT_FORMAT = [ ".avi", 
#                    ".mov", 
#                    ".mp4", 
#                    ".webm", 
#                    ".mkv", 
#                    ".jpg",
#                    ".png",
#                    ".docx",
#                    ".xlsx",
#                    ".pdf" ]
SUPPORT_IMAGE = [".jpg", ".png"]
SUPPORT_VIDEO = [".avi", ".mov", ".mp4", ".webm", ".mkv"]
SUPPORT_DOCUMENT = [".docx",".xlsx",".pdf"]
SUPPORT_FORMAT = SUPPORT_IMAGE + SUPPORT_VIDEO + SUPPORT_DOCUMENT

FORMAT_SUFFIX = {
    ".jpg": "JPEG",
    ".png": "PNG", 
    ".avi": "AVI", 
    ".mov": "MOV", 
    ".mp4": "MP4", 
    ".webm": "WEBM", 
    ".mkv": "MKV", 
    ".pdf": "PDF", 
    ".docx": "WORD",
    ".xlsx": "EXCEL"
}

# 文件最大接受字节
FILE_MAX_SIZE = 1024*1024*50 #52428800

# def md5_for_file(f, block_size=2**20):
#     with open(f, 'rb') as fHandle:
#         md5 = hashlib.md5()
#         while True:
#             data = fHandle.read(block_size)
#             if not data:
#                 break
#             md5.update(data)
#         return md5.hexdigest()
#     return md5.hexdigest()