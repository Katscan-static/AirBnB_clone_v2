#!/usr/bin/python3
"""
This script defines a Fabric task that packages the contents of the web_static
folder into a .tgz archive and stores it in the 'versions' directory.

The generated archive is named 'web_static_<year><month><day><hour><minute><second>.tgz'.
"""

from fabric.api import *
import time

def do_pack():
    """
    Create a compressed archive from the contents of the web_static folder.

    Returns:
        str: Archive path if successful, None if the archive wasn't created.
    """
    strtime = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        file_name = "web_static_{}.tgz".format(strtime)
        local("tar -cvzf versions/{} web_static".format(file_name))
        return "versions/{}".format(file_name)
    except Exception as e:
        return None

if __name__ == "__main__":
    do_pack()
