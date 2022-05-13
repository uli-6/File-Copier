import sys
import shutil
import argparse
import os
import itertools
import threading
import time
import logging
from tracemalloc import start

log = logging.getLogger('main.fileCopy')
done = False

def ParseCommandLine():

    parser = argparse.ArgumentParser('FileCopy')
    parser.add_argument('-cDir', '--copyDir', nargs='+', type=validateDirectory, required=False, help='Directory to copy from')
    parser.add_argument('-sDir', '--saveDir', type=validateDirectory, required=False, help='Directory to save to, will create if it doesnt exists and path is writable')
    parser.add_argument('--gui', action=argparse.BooleanOptionalAction)
    userArgs = parser.parse_args()

    return userArgs

def validateDirectory(theDir):

    #Validate the path is a directory
    if not os.path.isdir(theDir):

        os.makedirs(theDir)

        #raise argparse.ArgumentTypeError('Directory does not exist')

    #Validate the path is writable
    if os.access(theDir, os.W_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('directory is not writable')

def animate():  
    #animation to show programm is still running
    for c in itertools.cycle(['-----','*----', '**---', '***--', '****-', '*****']):
        if done:
            break
        sys.stdout.write('\rWorking on it ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')


#main function that does all the work,
#copies files and folders to designated path
def copyFiles(userArgs):
    copyDir = userArgs.copyDir
    saveDir = userArgs.saveDir
    copyCount = 0

    t = threading.Thread(target=animate)
    t.start()


    log.info("copy start")
    for theDir in copyDir:

        print(theDir)

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

                copyCount += 1
    print('files coppied: %s' % (copyCount))
    log.info('files coppied: %s' % (copyCount))
    global done
    done = True
    