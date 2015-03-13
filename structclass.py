import sys
import os
import time
import subprocess
import re
import os.path
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
from sys import stdout


#comparestruct = Struct1('found','diffvalue','x','y')


def Struct1(*args, **kwargs):
    def init(self):
        for k,v in kwargs.items():
            setattr(self, k, v)
    name = kwargs.pop("name", "ImageProcessResultStruct")
    kwargs.update(dict((k, None) for k in args))
    return type(name, (object,), {'__init__': init, '__slots__': kwargs.keys()})
