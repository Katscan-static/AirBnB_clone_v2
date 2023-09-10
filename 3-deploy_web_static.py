#!/usr/bin/python3
"""
This script defines a Fabric task to deploy an archive to web servers.
"""

from fabric.api import *
import os
import time
env.hosts = ['54.160.94.67', '100.25.38.2']


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

def do_deploy(archive_path):
    """
        Distribute an archive to web servers and deploy it.

        Args:
            archive_path (str): The path to the archive to deploy.

        Returns:
            bool: True if deployment is successful, False otherwise.
    """

    if not os.path.exists(archive_path):
        return False

    try:
        new_name = archive_path.split("/")[-1]
        folder = ("/data/web_static/releases/" + new_name.split(".")[0])
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(folder))
        run("sudo tar -xzf /tmp/{} -C {}".
            format(new_name, folder))
        run("sudo rm /tmp/{}".format(new_name))
        run("sudo mv {}/web_static/* {}/".format(folder, folder))
        run("sudo rm -rf {}/web_static".format(folder))
        run('sudo rm -rf /data/web_static/current')
        run("sudo ln -s {} /data/web_static/current".format(folder))
        return True
    except Exception:
        return False


def deploy():
    """
        deploy including pack

        Return:
            value if successful or None
    """
    try:
        archive_name = do_pack()
        value = do_deploy(archive_name)
        return value
    except:
        return False
