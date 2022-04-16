# coding:utf-8
# --author-- lanhua.zhou
import os
import sys
import json
import logging

__all__ = ["get_menu_data", "MENU_KEY", "MENU_FILE"]

DIRNAME = os.path.dirname(__file__)
MENU_DIRNAME = os.path.dirname(os.path.dirname(DIRNAME))
MENU_FILE = "{}/conf/menu.json".format(MENU_DIRNAME)

MENU_KEY = [ "utility", 
             "modeling", 
            "shading",
            # "rigging", 
            # "assembly", 
             "animation", 
            # "fx", 
            # "rendering", 
            # "technology",
             "help" ]

logger = logging.getLogger(__name__)

def get_menu_data():
    """
    get menu scripts 

    rtype: list
    """
    _menu_data = []

    logger.info("read menu json file data")
    
    _version = sys.version_info
    if _version.major == 3:
        with open(MENU_FILE, "r", encoding='UTF-8') as _file_handle:
            _data = _file_handle.read()
            _menu_data = json.loads(_data)
    else:
        with open(MENU_FILE, "r") as _file_handle:
            _data = _file_handle.read()
            _menu_data = json.loads(_data)
    return _menu_data