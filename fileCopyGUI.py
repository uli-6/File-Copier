#from tkinter import *

import logging
import threading
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
import os
import shutil
import queue

#from ttkthemes import ThemedTk
#import fileCopy

log = logging.getLogger('main.fileCopy')

class Window():
    def __init__(self):
        self.master = tk.Tk()

        #self.master = master
        self.master.title("File Copier")
        self.master.geometry('500x600')
        self.master.grid_rowconfigure(7,weight=1)
        self.master.grid_columnconfigure(0,weight=1)
        self.entries = []
        self.buttons = []
        self.files = []
        self.row = 2
        self.output = ''

        self.threadQueue = queue.Queue()


        #make the frames for the master
        self.frameMain = ttk.LabelFrame(self.master, text="Select destination to copy from and save destination")
        self.frameMain.grid()
        self.frameInput =  ttk.Frame(self.frameMain)
        self.frameInput.grid()
        self.frameOutput = ttk.LabelFrame(self.frameMain, text='files processed')
        self.frameOutput.grid()
        self.frameAction = ttk.LabelFrame(self.frameInput, text='action')
        self.frameAction.grid(row=2)

        #creates all the entries and the default text and binds it to their respective clear functions

        self.txtbxCopyPath = ttk.Entry(self.frameInput, width=15)
        self.txtbxCopyPath.insert(0, "'copy path'")
        self.txtbxCopyPath.bind("<Button-1>", self.clearCopyPath)
        self.txtbxCopyPath.grid(row=1, column=1)

        self.txtbxSavePath = ttk.Entry(self.frameInput, width=15)
        self.txtbxSavePath.insert(0, "'save path'")
        self.txtbxSavePath.bind("<Button-1>", self.clearSavePath)
        self.txtbxSavePath.grid(row=0, column=1)
            
        #creates all buttons

        self.btncopyPath = ttk.Button(self.frameInput, text=". . .", command=self.clkCopyPath)
        self.btncopyPath.grid(row=1, column=2)

        self.btnSavePath = ttk.Button(self.frameInput, text=". . .", command=self.clkSavePath)
        self.btnSavePath.grid(row=0, column=2)

        self.btnStart = ttk.Button(self.frameInput, text="Start", command=self.startThread)
        self.btnStart.grid(row=2, column=0)

        self.btnAddEntry = ttk.Button(self.frameInput, width=4, text="+", command=self.addEntry)
        self.btnAddEntry.grid(row=1, column=3)

        self.btnAddEntry = ttk.Button(self.frameInput, width=4, text="-", command=self.reomoveEntry)
        self.btnAddEntry.grid(row=1, column=4)

        self.btnClear = ttk.Button(self.frameOutput, text="Clear", command=self.clkClearList, width = 40)
        self.btnClear.grid(row=3)

        #creates listbox, progressbar, scrollbar

        self.output = tk.Listbox(self.frameOutput, width=60, height=20)
        self.output.grid(row=0)

        self.prgrsbarOutput = ttk.Progressbar(self.frameOutput, length=480, mode='indeterminate')
        self.prgrsbarOutput.grid()

        self.scrlbarOutput = ttk.Scrollbar(self.frameOutput, orient='vertical')
        self.scrlbarOutput.grid(row=0, column=1)
        self.scrlbarOutput.config(command=self.output.yview)
        
        self.master.after(1, self.listBoxQueue)
        self.master.mainloop()

    def startThread(self):
        t = threading.Thread(target=self.copyFiles)
        t.start()

    def displayText(self, text):
        self.output.insert(0, text)

    def listBoxQueue(self):
        try:
            self.text = self.threadQueue.get(0)
            self.displayText(self.text)
            self.master.after(1, self.listBoxQueue)
        except:
            self.master.after(1, self.listBoxQueue)    

    # adds entries and buttons depending on copy locatiions user wants
    def addEntry(self):
        log.info("\nADD ENTRY\n")

        entryI = ttk.Entry(self.frameInput, width=15)
        entryI.insert(0, "'copy path'")
        entryI.grid(row = self.row, column = 1)
        btnI = ttk.Button(self.frameInput, text=". . .", command=self.clkCopyPathGenerator(entryI))
        #btnI.grid(row=self.row, column=2)

        self.entries.append(entryI)
        self.buttons.append(btnI)

        self.row += 1
    
    #removes entries and buttons
    def reomoveEntry(self):
        if self.entries:
            log.info("\nREMOVE ENTRY\n")

            self.buttons[-1].destroy()
            self.buttons.pop()

            self.entries[-1].destroy()
            self.entries.pop()
            self.row -= 1
        

    #functions to clear the default text in each entry
    def clearCopyPath(self, event):
        if (self.txtbxCopyPath.get() == "'Save Path'"):
            self.txtbxCopyPath.delete(0, "end")
        return None
    def clearSavePath(self, event):
        if (self.txtbxSavePath.get() == "'Save Path'"):
            self.txtbxSavePath.delete(0, "end")
        return None
    
    #functions for the buttons to open a directory to select path
    #clears anything already in the entry
    def clkCopyPath(self):
        self.txtbxCopyPath.delete(0, "end")
        copyPath = askdirectory()
        self.txtbxCopyPath.insert(0, copyPath)
    
    def clkCopyPathGenerator(self, entryI):
        entryI.delete(0, "end")
        copyPath = askdirectory()
        entryI.insert(0, copyPath)

    def clkSavePath(self):
        self.txtbxSavePath.delete(0, "end")
        savePath = askdirectory()
        self.txtbxSavePath.insert(0, savePath)
    
    #checkEntries checks to see that none of the default entries are remaining in order for program to start
    def chkEntries(self):
        if (self.txtbxCopyPath.get() != "'copy path'" 
                and self.txtbxSavePath.get() != "'destination path'"):
            return True

    '''
    def clkCopyFiles(self):
        if self.chkEntries():
            self.prgrsbarOutput.start(10)
            self.copyFiles()
            #prgrsbarOutput.stop()
    '''

    def clkClearList(self):
        last = self.output.grid_size()
        self.output.delete(0, last[1])

    #where all the magic happens
    def copyFiles(self):
        copyCount = 0
        copyDir = []
        copyDir.append(self.txtbxCopyPath.get())
        saveDir = self.txtbxSavePath.get()
        entriesList = self.entries

        #makes sure that extra entries are not empty and are a valid dir
        for entries in entriesList:
            if entries.get() != 'copy path' and entries.get() != '':
                if os.path.isdir(entries.get()):
                    copyDir.append(entries.get())

        log.info("copy start")
        #loops through all desired copy from directories
        for theDir in copyDir:

            for dirPath, dirNames, fileNames in os.walk(theDir):
                log.info(dirPath)
                newSaveDir = dirPath.split(theDir)
                newSaveDir = newSaveDir[-1] 
                newSaveDir = '%s/%s' % (saveDir, newSaveDir)

                if not os.path.isdir(newSaveDir):
                    os.makedirs(newSaveDir)

                for fileName in fileNames:

                    if theDir == dirPath:
                        shutil.copy('%s/%s' % (dirPath, fileName), '%s/%s' % (saveDir, fileName))

                    else:
                        shutil.copy('%s/%s' % (dirPath, fileName), '%s/%s' % (newSaveDir, fileName))
                    
                    #output.insert(0, fileName)
                    self.threadQueue.put(fileName)
                copyCount += 1
    
        log.info('files coppied: %s' % (copyCount))


def gui():
    app = Window()
