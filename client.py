#!/usr/bin/env python
# -*- coding: utf8 -*-

import options
import sys
import os
from commands.handlers import CommandExists, ExecuteCommand, cmdList

def main(args):
    if len(args) <=0:
        # если никаких аргументов не передали, показываем список доступных команд
        print "No arguments passed!\nYou may use these commands:\n"
        for item in cmdList:
            print "- %s - %s\n\tusage: %s" % (item, cmdList[item]['desc'], cmdList[item]['usage'], )
    else:
        # иначе, если команда доступна, выполняем ее
        if CommandExists(args[0]):
            print "Execing %s..." % args[0]
            ExecuteCommand(args[0], args[0:])
        # а если не доступна, говорим об этом
        else:
            print "Error! The Command %s is not defined" % args[0]



if __name__ == "__main__":
    main(sys.argv[1:])

