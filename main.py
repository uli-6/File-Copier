import logging 
import time 
import fileCopy
import fileCopyGUI

if __name__ == '__main__':     

    FILECOPY_VERSION='1.0'

    #turn on logging     
    logging.basicConfig(filename='fileCopyLog.log', level=logging.DEBUG, format='%(asctime)s %(message)s')     
    
    #processes the command line args     
    userArgs = fileCopy.ParseCommandLine()     
    log=logging.getLogger('main.fileCopy')  
    log.info('')     
    log.info('program started')     
    
    #record the start time     
    startTime = time.time()     
    

    #perform copy in cli if no gui called
    if userArgs.gui:
        fileCopyGUI.gui()
    else:    
        fileCopy.copyFiles(userArgs)     
    
    #record the ending time     
    endTime = time.time()     
    duration = endTime - startTime     
    log.info('elapsed time: ' + str(duration) + 'seconds')     
    log.info('')     
    log.info('program terminated normally')

