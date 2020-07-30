#!/usr/bin/env python3


import subprocess
from langoon import Command

class GitPull(Command):

    def __init__(self):
        # Pull from origin master branch
        command = subprocess.Popen([ "git", "pull", "origin", "master" ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        message, error = command.communicate()
        if command.returncode != 0:
            raise Exception(error)
        else:
            self.send_response({ "success": True, "message": message })

if __name__ == "__main__":
    GitPull()
