#!/usr/bin/python3
"""
    packege all files as tgz
"""


from fabric.api import *
import time



def do_pack():
    strtime = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        file_name = "web_static_{}.tgz".format(strtime)
        local("tar -cvzf versions/{} web_static".format(file_name))
        return("versions/{}".format(file_name))
    except:
        return None
