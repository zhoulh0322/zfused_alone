# coding:utf-8
# --author-- lanhua.zhou

import os
import sys
import glob

# PATH = os.path.abspath("./resources")
PATH = os.path.dirname(__file__)
RESOURCE_DIRNAME = os.path.dirname(PATH)

from . import resources


def get(*args):
    """
    This is a convenience function for returning the resource path.

    :rtype: str 
    """
    # return Resource().get(*args)
    # return os.path.join(":", *args).replace(os.sep, "/")

    return os.path.join("{}/resources".format(RESOURCE_DIRNAME), *args).replace(os.sep, "/")

    # return os.path.join(":/resources", *args).replace(os.sep, "/")



# class Resource(object):
#     DEFAULT_DIRNAME = RESOURCE_DIRNAME

#     def __init__(self, *args):
#         """"""
#         dirname = ""

#         if args:
#             dirname = os.path.join(*args)

#         if os.path.isfile(dirname):
#             dirname = os.path.dirname(dirname)

#         self._dirname = dirname or self.DEFAULT_DIRNAME

#     def dirname(self):
#         """
#         :rtype: str
#         """
#         return self._dirname

#     def get(self, *args):
#         """
#         Return the resource path for the given args.

#         :rtype: str
#         """
#         return os.path.join(self.dirname(), *args).replace(os.sep, "/")
#         # _res = os.path.join(":/resources", *args).replace(os.sep, "/")
#         # return os.path.join(":/resources", *args).replace(os.sep, "/")