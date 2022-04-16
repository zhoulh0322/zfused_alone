# coding:utf-8
# --author-- lanhua.zhou
import os
import json
import logging

__all__ = ["get_component_color_data", "LetterColor"]

DIRNAME = os.path.dirname(__file__)
MENU_DIRNAME = os.path.dirname(os.path.dirname(DIRNAME))
COMPONENT_COLOR_FILE = "{}/conf/componentcolor.json".format(MENU_DIRNAME)

logger = logging.getLogger(__name__)

def get_component_color_data():
    """
    get menu scripts 

    rtype: list
    """
    _menu_data = []

    logger.info("read menu json file data")
    
    with open(COMPONENT_COLOR_FILE, "r") as _file_handle:
        _data = _file_handle.read()
        _menu_data = json.loads(_data)
    return _menu_data


class LetterColor(object):
    _color_dict = {
            "a":"#E5A3B4",
            "b":"#EDC89A",
            "c":"#F2F08F",
            "d":"#E0E67A",
            "e":"#BBDB97",
            "f":"#ACD9BA",
            "g":"#A1DAE1",
            "h":"#C19FCA",
            "i":"#CF2027",
            "j":"#D96927",
            "k":"#ECDA42",
            "l":"#A5C33B",
            "m":"#77C258",
            "n":"#54958C",
            "o":"#486EB6",
            "p":"#77449A",
            "q":"#7F7E80",
            "r":"#7C1214",
            "s":"#83421B",
            "t":"#86792F",
            "u":"#587232",
            "v":"#417135",
            "w":"#3D6C4C",
            "x":"#253676",
            "y":"#462165",
            "z":"#1D1D1D"
        }


    @classmethod
    def color(cls, letter):
        if letter not in cls._color_dict:
            return "#666666"
        return cls._color_dict[letter]

def convert(value):
    """ change color value type
    
    """
    digit = list(map(str, range(10))) + list("ABCDEF")
    if isinstance(value, tuple):
        string = '#'
        for i in value:
            a1 = i // 16
            a2 = i % 16
            string += digit[a1] + digit[a2]
        return string
    elif isinstance(value, str):
        a1 = digit.index(value[1]) * 16 + digit.index(value[2])
        a2 = digit.index(value[3]) * 16 + digit.index(value[4])
        a3 = digit.index(value[5]) * 16 + digit.index(value[6])
        return (a1, a2, a3)


if __name__ == "__main__":
    convert((0.3606775104999542, 0.5447165369987488, 0.12387274205684662))