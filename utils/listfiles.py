
import os, sys, time
import shutil
import thread
#from validation.managefiles.mediafiles import *
import mediafiles

oldest = 0

def folderpolling(watch_folder, timeout=60):
    
    before = dict ([(f, None) for f in os.listdir (watch_folder)])
    print before
    pollingstop = timeout/5
    while 1:
        time.sleep (5)
        after = dict ([(f, None) for f in os.listdir (watch_folder)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added:
            return 1
        pollingstop = pollingstop - 1
        if pollingstop == 0:
            return 0


def getSortByDateDebugFiles(filepath):
    a = [files for files in os.listdir(filepath)
        if files.endswith(".txt") and ("arbitron" in files)]
    a.sort(key=lambda files: os.path.getmtime(os.path.join(filepath, files)))
    return a

def getSortByDateFiles(filepath, extension, filenamematch):
    a = [files for files in os.listdir(filepath)
        if files.endswith(extension) and (filenamematch in files)]
    a.sort(key=lambda files: os.path.getmtime(os.path.join(filepath, files)))
    return a

def getLastSessionApplog(pid):
    sessions = []
    sessions = getAllSessionsLog("C:\\ProgramData\\App\\appLog_"+pid+".txt","EventLogger: Startup")
    if sessions:
        return sessions[-1]
    elif sessions == None:
        print "Error: App output file doesn't exist."
        return 0
    else:
        return -1

def getLastSessionPluginlog():
    lastsession = []
    lastsession = getAllSessionsLog("C:\\ProgramData\\App\\output_log.txt","==[ ")
    if lastsession:
        return lastsession[-1]
    elif lastsession == None:
        print "Error: App file doesn't exist."
        return 0
    else:
        return -1

def getAllSessionsLog(logname, startLine):

    linenumber = 0
    sessionNumber = 0
    sessiontext = ""
    sessionStart=[]
    sessions=[]
    
    f = openfile(logname)
    if(f):
        textfile = f.readlines()
        for line in textfile: 
            linenumber = linenumber + 1
            if startLine in line:
                sessionNumber = sessionNumber + 1
                sessionStart.append(linenumber)
                
        totalsessions = len(sessionStart)
        
        for i in range(totalsessions):
            if i<totalsessions-2:
                sessionText = textfile[sessionStart[i]-1 : sessionStart[i+1]-1]
            else:
                sessionText = textfile[sessionStart[i]-1 : linenumber]
                
            sessions.append("".join(sessionText))
            
        f.close()
        
    return sessions
     
    
def openfile(fn):
    try:
        file = open(fn)
        return file
    except IOError:
        print "Error:  The " + fn + " file doesn't appear to exist."
        #sys.exit(0)
        return None
    
def existfile(pathfn):
 
    if os.path.isfile(pathfn):
        return True
    else:
        print "ERROR: %s file doesn't exist" % pathfn
        return False
    
def existfolder(path):
    if os.path.exists(path):
        return True
    else:
        print "ERROR %s folder doesn't exist" % path
        return False
        