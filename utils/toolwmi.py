
import wmi
import pythoncom

def getallprocesses():
    pythoncom.CoInitialize()
    
    c = wmi.WMI ()
    
    processList = []
    pidlist = []
    
    print " get processes - "
    for process in c.Win32_Process ():
        pid = str(process.ProcessId)
        pname = str(process.Name)
        processList.append([pid,pname])
        pidlist.append(pid)
                
          
    processList.sort(key=lambda x: x[1])
    pythoncom.CoUninitialize ()
            
    return processList