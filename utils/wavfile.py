
import wave
import os
 
class wavfile(object):
   
    
    def __init__(self, wavfilename):
        self.wavfilename = wavfilename
        
        
    def getChiInfo(self):
        wav = self.openwavfile()
        if not wav:
            wav.close()
            return None
        ch = wav.getnchannels()
        wav.close()
        return ch
    
    def getByteInfo(self):
        wav = self.openwavfile()
        if not wav:
            wav.close()
            return None
        byte = wav.getsampwidth()
        wav.close()
        return byte
    
    def getFreqInfo(self):
        wav = self.openwavfile()
        if not wav:
            wav.close()
            return None
        f = wav.getframerate()
        wav.close()
        return f
    
    def getFramesInfo(self):
        wav = self.openwavfile()
        if not wav:
            wav.close()
            return None
        frames = wav.getnframes()
        wav.close()
        return frames
    
    def getCompressionInfo(self):
        wav = self.openwavfile()
        if not wav:
            wav.close()
            return None
        comp = wav.getcompname()
        wav.close()
        return comp
    
    def getWavLength(self):
        wav = self.openwavfile()
        if not wav:
            wav.close()
            return None
        rate = wav.getframerate()
        frames = wav.getnframes()
        wavlength = frames/rate
        wav.close()
        return wavlength
    
    def getDataRateInfo(self):
        wav = self.openwavfile()
        if not wav:
            wav.close()
            return None
        rawdata = wav.readframes()
    
        wav.close()
        return "done"
    
    def openwavfile(self):
        if not os.path.isfile(self.wavfilename):
            print "ERROR:  WAVE file doesn't exist - %s" % self.wavfilename
            return False
        
        wav = wave.open(self.wavfilename,'r')
        
        return wav
    
def usage():
    print "Usage: wavfile.py -i [path + WAV-filename]"
    print "        -i: file name (including path) of a WAV file"
    
if __name__ == "__main__":
    import getopt
    import sys,os.path

    # Read command line args
    inputfile = ''
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"i:")
    except getopt.GetoptError as err:
        print ("ERROR: " + str(err))
        usage()
        sys.exit()
    
    #-- No arguments found
    if not opts:
        usage()
        sys.exit()
    #-----------------------------
    # o == option
    # a == argument passed to the o
    #-----------------------------------
    for o, a in opts:
        if o == '-i':
            inputfile = a
        else:
            usage()
            sys.exit()
            
    #print "input: " + inputfile
    wav = wavfile(inputfile)
    ch = wav.getChiInfo()
    f = wav.getFreqInfo()
    c = wav.getCompressionInfo()
    frames = wav.getFramesInfo()
    length = wav.getWavLength()
    d = wav.getDataRateInfo()
    print "Channels: %s" % ch
    print "Frequency: %s Hz" % f
    print "compression: %s" % c
    print "frames: %s" % frames
    print "length: %s seconds" % length
    print "datarate: %s " % d
    