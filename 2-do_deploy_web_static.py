#!/usr/bin/python3
"""
This script defines a Fabric task to deploy an archive to web servers.
"""

from fabric.api import *
import os
env.hosts = ['54.160.94.67', '100.25.38.2']


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
