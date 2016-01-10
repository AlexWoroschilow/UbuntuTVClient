#!/usr/bin/python3

import sys
import logging

from optparse import OptionParser
from application.UbuntuTv import UbuntuTv


"""
Parse arguments an configure context
to run power manager
"""
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-g", "--debug", action="store_true", default=False, dest="debug", help="enable debug mode")

    (options, args) = parser.parse_args()

    application = UbuntuTv()
    application.start()
