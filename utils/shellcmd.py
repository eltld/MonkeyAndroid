
class shellcmd(object):
    
    def __init__(self, command):
        self.command = command
        
        
    def run(self, shell=True):
        import subprocess as sp
        process = sp.Popen(self.command, shell = shell, stdout = sp.PIPE, stderr = sp.PIPE)
        self.pid = process.pid
        self.output, self.error = process.communicate()
        self.failed = process.returncode
        return self
    
    @property
    def returncode(self):
        return self.failed
def usage():
    print "Usage : shellcmd -c [shell command]"
    
def runShellCmd(cmd):
    #Julio - 9/4/2013 deprecated by shellcmd.py
    shellresponse=[]
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = p.stdout.readline()
        if line:
            shellresponse.append(line)
        if not line:
            break
    return shellresponse

if __name__ == "__main__":
    import sys, getopt
    
    cmd = ''
    # Read command line args
    try:
        opts, args = getopt.getopt(sys.argv[1:],"c:")
    except getopt.GetoptError as err:
        print ("ERROR: " + str(err))
        usage()
        sys.exit()
    
    #-- No arguments found
    if not opts:
        usage()
        sys.exit()
    ###############################
    # o == option
    # a == argument passed to the o
    ###############################
    for o, a in opts:
        if o == '-c':
            cmd = a
        else:
            usage()
            sys.exit()
    #================== Run shellcmd() ===================
    if cmd:
        com = shellcmd(cmd).run(True)
        if not com.failed:
            print com.output
        else:
            print "Error: " + com.error