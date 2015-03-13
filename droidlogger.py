import sys
import os
import time
import logging
import inspect

def android_logger( file_level, console_level = None):
	function_name = inspect.stack()[1][3]
	logger = logging.getLogger(function_name)
	logger.setLevel(logging.DEBUG) #By default, logs all messages

	if console_level != None:
		ch = logging.StreamHandler() #StreamHandler logs to console
		ch.setLevel(console_level)
		ch_format = logging.Formatter('[%(asctime)s] - %(message)s')
		ch.setFormatter(ch_format)
		logger.addHandler(ch)

	#fh = logging.FileHandler("{0}.log".format(function_name))
	#filename = file_name + ".log"
	fh = logging.FileHandler('androidlinkmetertest.log')
	fh.setLevel(file_level)
	fh_format = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
	fh.setFormatter(fh_format)
	logger.addHandler(fh)

	return logger

def android_logger2(file_name , file_level, console_level = None):
	function_name = inspect.stack()[1][3]
	logger = logging.getLogger(function_name)
	logger.setLevel(logging.DEBUG) #By default, logs all messages

	if console_level != None:
		ch = logging.StreamHandler() #StreamHandler logs to console
		ch.setLevel(console_level)
		#ch_format = logging.Formatter('%(asctime)s - %(message)s')
		ch_format = logging.Formatter('%(asctime)s - %(message)s')
		ch.setFormatter(ch_format)
		logger.addHandler(ch)

	#fh = logging.FileHandler("{0}.log".format(function_name))
	filename = file_name + ".log"
	fh = logging.FileHandler(filename)
	fh.setLevel(file_level)
	#fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s')
	fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s')
	fh.setFormatter(fh_format)
	logger.addHandler(fh)

	return logger
	
'''
def android_logger(name):
	formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

	handler = logging.StreamHandler()
	handler.setFormatter(formatter)

	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)
	logger.addHandler(handler)
	return logger
	
def getLogger(name, logdir=LOGDIR_DEFAULT, level=logging.DEBUG, logformat=FORMAT):
	
	base = os.path.basename(__file__)
	loggerName = "%s.%s" % (base, name)
	logFileName = os.path.join(logdir, "%s.log" % loggerName)
	logger = logging.getLogger(loggerName)
	logger.setLevel(level)
	i = 0
	while os.path.exists(logFileName) and not os.access(logFileName, os.R_OK | os.W_OK):
		i += 1
		logFileName = "%s.%s.log" % (logFileName.replace(".log", ""), str(i).zfill((len(str(i)) + 1)))
	try:
		#fh = logging.FileHandler(logFileName)
		fh = RotatingFileHandler(filename=logFileName, mode="a", maxBytes=1310720, backupCount=50)
	except IOError, exc:
		errOut = "Unable to create/open log file \"%s\"." % logFileName
		if exc.errno is 13: # Permission denied exception
			errOut = "ERROR ** Permission Denied ** - %s" % errOut
		elif exc.errno is 2: # No such directory
			errOut = "ERROR ** No such directory \"%s\"** - %s" % (os.path.split(logFileName)[0], errOut)
		elif exc.errno is 24: # Too many open files
			errOut = "ERROR ** Too many open files ** - Check open file descriptors in /proc/<PID>/fd/ (PID: %s)" % os.getpid()
		else:
				errOut = "Unhandled Exception ** %s ** - %s" % (str(exc), errOut)
		raise LogException(errOut)
	else:
		formatter = logging.Formatter(logformat)
		fh.setLevel(level)
		fh.setFormatter(formatter)
		logger.addHandler(fh)
	return logger
'''