#!/usr/bin/env python3

from langoon import Command

class Ping(Command):

    def __init__(self):
        # Pings that the device is up and running
        self.send_response({ "success": True })

if __name__ == "__main__":
    Ping()
