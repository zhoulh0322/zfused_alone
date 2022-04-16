 # coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function
from functools import wraps

import os
import logging
# from multiprocessing import Process

from Qt import QtWidgets, QtGui, QtCore

from . import window
from . import progress_bar

logger = logging.getLogger(__name__)


def set_range(mini, maxi):
    progress_bar.set_range(mini, maxi)

def set_label_text(text):
    progress_bar.set_label_text(text)

def set_value(value):
    progress_bar.set_value(value)


def set_sub_range(mini, maxi):
    progress_bar.set_sub_range(mini, maxi)

def set_sub_label_text(text):
    progress_bar.set_sub_label_text(text)

def set_sub_value(value):
    progress_bar.set_sub_value(value)


def progress(title):
    def _progress( func ):
        __progress = progress_bar.ProgressBar(title)
        @wraps(func)
        def wrap( *args, **kwargs ):
            # QtWidgets.QApplication.processEvents()
            __progress.start()
            # QtWidgets.QApplication.processEvents()
            try:
                return func( *args, **kwargs )
            except Exception as e:
                logger.warning(e)
            finally:
                __progress.stop()
        return wrap
    
    return _progress