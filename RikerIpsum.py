import sublime
import sublime_plugin
import random
import re
import threading
import os

class RikerIpsumCommand(sublime_plugin.TextCommand):

    lines = []
    linesLoaded = 0
    lock = threading.Lock()

    def ensureLinesLoaded(self):

        self.lock.acquire()
        try:
  
            # Make sure our lines are loaded
            if not self.linesLoaded:
                # Find the current directory of this script
                curDir = os.path.dirname(__file__)

                # Open up the text lines file in the script directory
                with open(os.path.join(curDir,"rikerlines.txt"), 'r') as f:
                    for line in iter(f):
                        # Strip the line
                        strippedLine = line.strip()

                        # Make sure it's not a blank line
                        if len(strippedLine):
                            self.lines.append(line.strip())

                print "loading lines"
                self.linesLoaded = 1

        finally:
            self.lock.release()

    def run(self, edit, qty=5):

        # Make sure our lines are loaded up
        self.ensureLinesLoaded()

        selections = self.view.sel()
        for selection in selections:

            para = ""
            editor = self.view.begin_edit()

            for i in range(0, qty):
                from random import choice
                para += choice(self.lines) + " "

            # erase region
            self.view.erase(editor, selection)

            last = self.view.substr(sublime.Region(selection.begin()-1, selection.end()))
            if last == ".":
                para = " " + para

            # insert para before current cursor position
            self.view.insert(editor, selection.begin(), para)

            # insert para over the top of selection, but remaining selected (not behavior we want)
            # self.view.replace(editor, self.view.sel()[0], para)

            self.view.end_edit(editor)
