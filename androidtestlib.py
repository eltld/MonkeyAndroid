import sys
import os
import time
import subprocess
import re
import os.path
from time import clock, time

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
from sys import stdout
from structclass import *
from loadtestimages import *
from droidlogger import *

sys.path.append("C:\\Program Files (x86)\\Sikuli X\\sikuli-script.jar\\Lib")
#sys.path.append("C:\\Program Files\\Sikuli X\\sikuli-script.jar\\Lib")

#import org.sikuli.script.Finder # Sikuli vision engine loaded.
from sikuli import Finder

AppPackage = "com.android.app"
comparestruct = Struct1('found','diffvalue','x','y')


AppURLEmpanelment = "https://qa.environgmnet.url"


devicefolder = "droid10a"
#pathimage = "App_images\\"+devicefolder
pathimage = "App_images"

logit = android_logger(logging.DEBUG, logging.DEBUG)


def loadTestImgFiles(id):
	
	if(id == '02885005431fc557'):
		return droid10a
	
	elif(id == '0123456789ABCDEF'):
		return droid21c
		
	elif(id == 'SH1ART501305'):
		return droid14d
	
	elif(id == 'HT176HL09379'):
		return droid13a
		
	elif(id == 'HT17KV800328'):
		return droid14e
		
	elif(id == 'HT188HL04500'):
		return droid13b
	
def OpenApp(app, device):
	
	app2Run = appTrackList
	
	#----------  check if apps are listed in App  -----------
	if app.lower() in str(app2Run).lower():
		pass
	else:
		msg = "%s is not found.  Please add app info to App" % app
		logit.error(msg)
		return 0
	#---------------------------- open App ---------------------------
	for appname, (pkgapp, appstart) in app2Run.iteritems():	
		
		if appname.lower() == app.lower():
		
			appInstalled = isAndroidAppInstalled(pkgapp, device)
			if appInstalled:
				cmd = "am start -n " + appstart
				response = device.shell(cmd)
				
				if response.startswith('Warning'):
				
					'''
					Note:  can't get serial-number from some devices Samsung Galaxy Ace
							so need to return two value, one including the error or warning
							message.
							
					deviceId = getSerialNo(device)
					imgfile = loadTestImgFiles(deviceId)
					msg = "%s - Started App: %s - %s" % (deviceId,appname, response.strip())
					logit.warn(msg)
					MonkeyRunner.sleep(2)
					'''
					return 1, "Warning: " + response
				elif response.startswith('Error'):
					#logit.error(response)
					return 0, "Error: " + response
				else:
					#msg = imgfile['id']+ " - Start App: %s" % appname
					#logit.info(msg)
					#MonkeyRunner.sleep(2)
					return 1, "Info: " + appname
			else:
				#msg = imgfile['id']+ " - %s is not installed on android device " % app
				#logit.warn(msg)
				return 0, "Warning: " + app + " is not installed on adnroid device"

def OpenListofApps(appDict, timeTransition, device): # 1-key 2-value dict
	
	apps2Run={}
	
	#----------  check if apps are installed first -----------
	for  app, (pkg,cmp) in appDict.iteritems():
		if app and pkg and cmp :
			appInstalled = isAndroidAppInstalled(pkg, device)
			#appsInstalled = 1
			if appInstalled:
				apps2Run[app]=(pkg,cmp)
			else:
				msg = "%s is not installed on android device " % app
				logit.warn(msg)
				#print"> WARNING: %s is not installed on android device" % app
		else:
			msg = "Empy package app name = %s " % app
			logit.warn(msg)
			#print "> WARNING: Empy package app name = %s " % app

	#-------------- open apps one by one at every timeTransition ----------
	exit = 0
	while not exit:
		if not apps2Run:
			exit = 1
		else:
			for appname, (pkgapp, appstart) in apps2Run.iteritems():
				
				cmd = "am start -n " + appstart
		
				response = device.shell(cmd)
				
				if response.startswith('Warning'):
					#print "> Started App : %s" % appname
					#print "> WARNING: %s" % response
					msg = "Started App: %s - %s" % (appname, response)
					logit.warn(msg)
					MonkeyRunner.sleep(timeTransition)
					logit.info('Home Screen')
					goHomeScreen(device)
					MonkeyRunner.sleep(10)
					
				elif response.startswith('Error'):
					print "> ERROR:  %s " % response
				else:
					#print "> Started App %s " % appname
					msg = "Start App: %s" % appname
					logit.info(msg)
					MonkeyRunner.sleep(timeTransition)
					logit.info('Home Screen')
					goHomeScreen(device)
					MonkeyRunner.sleep(10)
				
			exit = 1

def typeInPhNumber(pn, device):
	#print "> Entering phone number..."
	mft = device.shell('getprop ro.product.manufacturer')

	if mft.strip() == "HTC":
		keycode = 'KEYCODE_DPAD_RIGHT'
	else:
		keycode = 'KEYCODE_TAB'
	
	if 10 == len(pn) and pn.isdigit():
	
		MonkeyRunner.sleep(2)
		for c in pn[0:3]:
			device.type(c)
		
		device.press(keycode, MonkeyDevice.DOWN_AND_UP)
		for c in pn[3:6]:
			device.type(c)
			
		device.press(keycode, MonkeyDevice.DOWN_AND_UP)
		for c in pn[6:10]:
			device.type(c)
			
	else:
		print ">  ERROR:  not a 10 digit number"

def IntallArbitronApp2(imgfile, device): 		# Deprecated on March 2013. 

	InstallState = enum(finished = 0, StartInstallation= 1, Empanel=2, SecurityWarning=3, AppInstalledOpen=4, PhoneNumberVerification=5, LandingPage=6)

	print "--------  Test Remote Installation Android App ----------"

	
	
	
	if 1 != isInternetOn(device):
		print "> ERROR:  No internet connection detected"
		sys.exit(0)
		
	exit = 0
	#installstate = InstallState.StartInstallation
	installstate = InstallState.LandingPage
	
	while not exit:
	
		if installstate == InstallState.StartInstallation:
			if (isArbAppInstalled(device)):
				print "> ERROR:  App is already installed"
				print "> Removing App being removed"
				UninstallQuick(device)
				MonkeyRunner.sleep(3)
				installstate = InstallState.Empanel
			else:
				installstate = InstallState.Empanel
				
		if installstate == InstallState.Empanel:
			stdout.write("> VERIFY App Download....")
			stdout.flush()
			GoToUrl(AppURLEmpanelment,imgfile['urltextbox']  , device)
			HomeButton(device)
			MonkeyRunner.sleep(5)
			OpenNotification(device)
			isfound, xClick, yClick = findSubimageClickLocation(imgfile['dlcompletenotify'],device)
			if (isfound):
				stdout.write("PASS\n")
				stdout.flush()
				installstate = InstallState.SecurityWarning
				device.touch(xClick, yClick, 'DOWN_AND_UP')
				MonkeyRunner.sleep(2)
			else:
				stdout.write("FAILED\n")
				print "> ERROR:  App apk file not found under Notification tray."
				exit=1
				
		elif installstate == InstallState.SecurityWarning:
			stdout.write("> VERIFY Security Warning page...")
			stdout.flush()
			isfound, xClick, yClick = findSubimageClickLocation(imgfile['securitywarning'] ,device)
			if (isfound):
				stdout.write("PASS\n")
				stdout.flush()
				installstate = InstallState.AppInstalledOpen
				device.touch(xClick, yClick, 'DOWN_AND_UP')
				MonkeyRunner.sleep(4)
			else:
				stdout.write("FAILED\n")
				print "ERROR: Security Access Request"
				exit = 1
				
		elif installstate == InstallState.AppInstalledOpen:
			stdout.write("> VERIFY App successfuly installed....")
			isfound, xClick, yClick = findSubimageClickLocation(imgfile['installed'],device)
			if(isfound):
				stdout.write("PASS\n")
				stdout.flush()
				installstate = InstallState.PhoneNumberVerification
				device.touch(xClick, yClick, 'DOWN_AND_UP')
				MonkeyRunner.sleep(3)
			else:
				stdout.write("FAILED\n")
				stdout.flush()
				print "ERROR: Installation not successful"
				exit = 1
				
		elif installstate == InstallState.PhoneNumberVerification:
			stdout.write("> VERIFY Phone Number page....")
			stdout.flush()
			isfound, xClick, yClick = findSubimageClickLocation(imgfile['phoneverify'],device)
			if(isfound):
				device.touch(xClick, yClick, 'DOWN_AND_UP')
				typeInPhNumber(qaph,device)
				#ClickonScreen("droid10A_Click_PhoneVerificationPage_PhoneNumberReady_OK.png",100,device)		# click on the OK buton, no verification needed. just find and click
				isfound, xClick, yClick= findSubimageClickLocation( imgfile['phoneOKbutton'] ,device)
				if(isfound):
					stdout.write("PASS\n")
					stdout.flush()
					device.touch(xClick, yClick, 'DOWN_AND_UP')
					MonkeyRunner.sleep(7)
					installstate = InstallState.LandingPage
				else:
					stdout.write("FAILED\n")
					stdout.flush()
					print "> ERROR: Phone Verification, couldn't find the OK button"
					exit = 1
			else:
				stdout.write("FAILED\n")
				stdout.flush()
				print"ERROR:  Phone Verification, couldn't find the textbox to enter number."
				exit = 1
				
		elif installstate == InstallState.LandingPage:
			stdout.write("> Verify landing page ....")
			stdout.flush()
			capturedfile 		= imgfile['imgfoldername']+"_CapturedLandingPage.png"
			capturedfilepathed 	= imgfile['imgfoldername']+"\\"+ capturedfile 
			ScreenCaptureDevice(capturedfilepathed,device)
			
		
			#
			comparescore = compareImgsSikuli(imgfile['landingpage'] ,capturedfilepathed )
			if(comparescore):
				stdout.write("PASS\n")
				installstate = InstallState.finished
				
			else:
				stdout.write("FAILED\n")
				stdout.flush()
				print "ERROR:  Landing page is not th same"
				exit = 1
				
		elif installstate == InstallState.finished:
			print". ------ Installation Completed Successfuly ---------"
			exit = 1
			
		else:
			print "> ERROR: During Remote Installation"
			exit = 1
			
def IntallArbitronApp(imgfile, device):

	InstallState = enum(finished = 0, StartInstallation= 1, Empanel=2, SecurityWarning=3, AppInstalledOpen=4, PhoneNumberVerification=5, LandingPage=6)

	logit.info("--------  Test Installation of App " + imgfile['id']+" ----------")
	
	if 1 != isInternetOn(device):
		logit.error(imgfile['id']+" - ERROR:  No internet connection detected")
		sys.exit(0)
		
		
	exit = 0
	installstate = InstallState.StartInstallation
	#installstate = InstallState.PhoneNumberVerification
	
	while not exit:
	
		if installstate == InstallState.StartInstallation:
			if (isArbAppInstalled(device)):
				logit.warn(imgfile['id']+" - WARNING:  App is already installed")
				logit.info(imgfile['id']+" - Uninstalling App...")
				#isUninstall = UninstallQuick(device)
				if not UninstallQuick(device):
					logit.error(imgfile['id']+" - ERROR:  Uninstalling App")
					exit = 1
				else:
					pass
				MonkeyRunner.sleep(3)
				installstate = InstallState.Empanel
			else:
				installstate = InstallState.Empanel
				
		if installstate == InstallState.Empanel:
			GoToUrl(AppURLEmpanelment,imgfile['urltextbox']  , device)
			goHomeScreen(device)
			MonkeyRunner.sleep(15)
			OpenNotification(device)
			isfound, xClick, yClick = findSubimageClickLocation(imgfile['dlcompletenotify'],device)
			if (isfound):
				logit.info(imgfile['id']+" - VERIFY App Download...PASS")
				installstate = InstallState.SecurityWarning
				device.touch(xClick, yClick, 'DOWN_AND_UP')
				MonkeyRunner.sleep(2)
			else:
				logit.info(imgfile['id']+" - VERIFY App Empanel/Download...FAILED")
				logit.error(imgfile['id']+" - ERROR:  App apk file not found under Notification tray.")
				exit=1
				
		elif installstate == InstallState.SecurityWarning:
			isfound, xClick, yClick = findSubimageClickLocation(imgfile['securitywarning'] ,device)
			
			if (isfound):
				logit.info(imgfile['id']+" - VERIFY Security Warning page...PASS")
				installstate = InstallState.AppInstalledOpen
				device.touch(xClick, yClick, 'DOWN_AND_UP')
				MonkeyRunner.sleep(4)
			else:
				logit.info(imgfile['id']+" - VERIFY Security Warning page...FAILED")
				logit.error(imgfile['id']+" - ERROR: Security Access Request")
				exit = 1
				
		elif installstate == InstallState.AppInstalledOpen:
			isfound, xClick, yClick = findSubimageClickLocation(imgfile['installed'],device)
			if(isfound):
				logit.info(imgfile['id']+" - VERIFY App successfuly installed...PASS")
				installstate = InstallState.PhoneNumberVerification
				device.touch(xClick, yClick, 'DOWN_AND_UP')
				MonkeyRunner.sleep(3)
			else:
				logit.info(imgfile['id']+" - VERIFY App successfuly installed...FAILED")
				#print "ERROR: Installation not successful"
				logit.error(imgfile['id']+" - ERROR:  Installation not successful")
				exit = 1
				
		elif installstate == InstallState.PhoneNumberVerification:
			isfound, xClick, yClick = findSubimageClickLocation(imgfile['phoneverify'],device)
			if(isfound):
				device.touch(xClick, yClick, 'DOWN_AND_UP')
				
				#====== Type in Phone Number ==================
				typeInPhNumber(qaph,device)
				
				isfound, xClick, yClick= findSubimageClickLocation( imgfile['phoneOKbutton'] ,device)
				
				#========= HTC EVOs with two size screens ============================
				if ('HT176HL09379' or 'HT188HL04500' in imgfile['id']) and not isfound:
					isfound, xClick, yClick= findSubimageClickLocation( imgfile['phoneOKbutton2'] ,device)
				
				if(isfound):
					logit.info(imgfile['id']+" - VERIFY Phone Number page...PASS")
					device.touch(xClick, yClick, 'DOWN_AND_UP')
					MonkeyRunner.sleep(12)
					installstate = InstallState.LandingPage
				else:

					logit.info(imgfile['id']+" - VERIFY Phone Number page...FAILED")
					logit.error(imgfile['id']+" - ERROR: Phone Verification, couldn't find the OK button")
					exit = 1
			else:

				logit.info(imgfile['id']+" - VERIFY Phone Number page...FAILED")
				logit.error(imgfile['id']+" - ERROR: Phone Verification, couldn't find the textbox to enter phone number")
				exit = 1
				
		elif installstate == InstallState.LandingPage:

			capturedfile 		= imgfile['imgfoldername']+"_CapturedLandingPage.png"
			capturedfilepathed 	= imgfile['imgfoldername']+"\\"+ capturedfile 
			ScreenCaptureDevice(capturedfilepathed,device)
			
			#if(ImageCaptureVerify(imgfile['landingpage'] ,"LandingPagecapture.png",2600,device)): # bigger threshold value.
			# 3/11/13 - replace for the Sikuli img comparison solution instead.
			#
			comparescore = compareImgsSikuli(imgfile['landingpage'] ,capturedfilepathed )
			if(comparescore):
				#stdout.write("PASS\n")
				logit.info(imgfile['id']+" - VERIFY landing page...PASS")
				installstate = InstallState.finished
				
			else:
				#stdout.write("FAILED\n")
				#stdout.flush()
				logit.info(imgfile['id']+" - VERIFY landing page...FAILED")
				#print "ERROR:  Landing page is not th same"
				logit.error(imgfile['id']+" - ERROR: Landing page is not the same")
				exit = 1
				
		elif installstate == InstallState.finished:
			logit.info("-------- Installation Completed Successfuly " + imgfile['id']+" ---------")
			goHomeScreen(device)
			
			exit = 1
			
		else:
			logit.error(imgfile['id']+" - ERROR: During Remote Installation")
			exit = 1

def GoToUrl(url, urltextbox, device):

	if(1 != isInternetOn(device)):
		print"> WARNING:  No internet connection detected"
		sys.exit(0)
		
	OpenBrowser(device)
	MonkeyRunner.sleep(8)
	ScrollUp(device)
	h,w = FindScreenSize(device)
	
	
	#--------------- Sikuli find subimage ---------------
	isfound, xClick, yClick = findSubimageClickLocation(urltextbox,device)
	if(isfound):
		device.touch(int(int(w)/2), yClick, 'DOWN_AND_UP')
		MonkeyRunner.sleep(2)
		
		#==========  for HTC browsers only =================
		mft = getDeviceMft(device)
		if 'HTC' in mft:
			for i in range(1,14):
				device.press('KEYCODE_DEL', MonkeyDevice.DOWN_AND_UP)
		MonkeyRunner.sleep(1)
		#=========================================================	
	
		for c in url:  # 1/14 - sometimes this may not work and trigger other events.  reboot phone.
			device.type(c)
	else:
		print"> ERROR:  couldn't find URL textbox"
		sys.exit(0)
		
	MonkeyRunner.sleep(3)
	device.press('KEYCODE_ENTER', MonkeyDevice.DOWN_AND_UP)
	MonkeyRunner.sleep(15)
	


def rename2ReferenceImg(filename):
	if filename.endswith(".png"):
		newfilename = filename[:-4]
		return newfilename + '_referenceimage.png'
	
def findSubimageClickLocation(subImage,device):
	
	path=os.getcwd()
	
	referenceImageFilename = rename2ReferenceImg(subImage)
	ScreenCaptureDevice(referenceImageFilename,device)
	subImgPathed = path +"\\"+ pathimage  +"\\"+ subImage
	referenceImgPathed = path +"\\"+ pathimage  +"\\"+referenceImageFilename


	
	'''
	start = time.clock()
	print "> Start Time: %s" % start
	'''
	
	referenceImgSikuli = Finder(referenceImgPathed)
	subImgSikuli = referenceImgSikuli.find(subImgPathed)
	
	if referenceImgSikuli.hasNext():	# time elapse 46ms to find the url box-star
		subImgLocation = referenceImgSikuli.next() # Format: 'Match[420,71 17x18 score=1.00 target=center]'
		
		return True, subImgLocation.getX(), subImgLocation.getY()
		
	else:								# time elase 100ms to not find the url box-star
		return False, 0, 0 
		
	'''
	elapse = (time.clock() - start)
	print "> Elapse time: %s " % elapse
	'''	

def compareImgsSikuli(referenceImg,capturedImg): # reference img has to be bigger than captured img
	'''
	NOTE from SIkuli: 	The default minimum similarity is 0.7.  when using hasNext() or Next()
						To compare at a lower score use:
						f.find(client-image, 0.3)
						so even "very" different images might match and you can decide further using the above score.
	'''
	path = os.getcwd()
	referenceImgPathed = path + "\\" + pathimage + "\\" + referenceImg
	capturedImgPathed = path + "\\" + pathimage + "\\" + capturedImg
	
	
	refImg = Finder(referenceImgPathed)
	refImg.find(capturedImgPathed)
	if refImg.hasNext():
		score = refImg.next().getScore()
		return score
	else:
		#print "didn't find it"
		return 0
	

	

def ScreenCaptureDevice(filename, device):
    
    path=os.getcwd()
    pathfilename=path+"\\"+pathimage+"\\"+filename

    #print "> Capturing image: %s" % pathfilename
    result=device.takeSnapshot()
    MonkeyRunner.sleep(3)
    result.writeToFile(pathfilename,'png')
    MonkeyRunner.sleep(2)

def InstallQuick(apkpathed, device):
	#NOTE:  App won't start,  a reboot or usb cable connection will start the service.  Then the icon will need.
	#		no be pressed in order to get the phone verification and finished installation.
	#		
	print "------- Quick Install ---------"
	if not isArbAppInstalled(device):
		responseinstall = device.installPackage(apkpathed)
		if not responseinstall:
			print"> ERROR:  quick install"
		else:
			print"> Quick Install:  successful"
	else:
		print ">  INFO: Appis already installed"	

def StartActivity(componentstring,device): 		# 1/25/13 doesn't work.


	print "--------- Start Activity ----------"
	if(isArbAppInstalled(device)):
		device.startActivity(component=componentstring)
		print"> Start Activity:  successful"
	else:
		print ">  INFO: Acivity is not installed"

def isScreenOn(device):

	response = device.shell('dumpsys power')
	
	powerstate = re.search(r'.*mPowerState=([0-9]+).*', response)
	if powerstate and int(powerstate.group(1)) == 0:
		#print "Screen is Off"
		return 0
		
	if int(powerstate.group(1)) > 0:
		#print "Screen is On"
		return 1

def getScreenState(device):			# returns 0=screen off; 1=screen on and locked/keyguard; 2=screen on and unlocked
	screenState = isScreenOn(device)
	
	if screenState:
		if isKeyguardDisplayed(device):
			#print "Screen On and lock"
			return 1
		else:
			z#print "Screen On and unlock"
			return 2
		
	elif(screenState == 0):
		#print "Screen Off"
		return 0
			
def isKeyguardDisplayed(device): 	# returns foreground app. Same as getDisplayFocusedApp but 'keyguard' is return when screen locked.
	response = device.shell('dumpsys window')
	#m = re.search(r'.*mCurrentFocus=([a-zA-Z]+).*', response)
	#print " getDisplayForeground= %s" % m.group(0)
		
	responseSplitted = response.split('\n')
	for line in responseSplitted:
		if 'mCurrentFocus=' in line:
			currentDisplay = line.split()[1]
			if 'Keyguard' in currentDisplay:
				return 1
			else:
				return 0
	
def getDisplayFocusedApp(device): 	# returns package name of app in foreground (launcher = home screen) even when screen is locked or screen off
	response = device.shell('dumpsys window')
	responseSplitted = response.split('\n')
	for line in responseSplitted:
		if 'mFocusedApp=' in line:
			focusedApp = line.split()[2]
			#print "Focused App =  " + focusedApp
			return focusedApp

def UnlockPhone(id, device): 			# 'id' required becuase 'id' can't be retrieve from all phones.  Droid21c

	droid21c = "0123456789ABCDEF"
	droid10a = "02885005431fc557"
	droid14e = "HT17KV800328"
	droid14d = "SH1ART501305"
	droid2b  = "04037D0F1001A009"
	droid13a = "HT176HL09379"
	droid13b = 'HT188HL04500'
	
	h,w = FindScreenSize(id)
	h = int(float(h))
	w = int(float(w))

	
	if len(id) == 0:
		print "ERROR: Phone serial number is not 16 digits"
		sys.exit(0)
		
	elif droid21c in id:
		#droid21C H=480 W=320
		wstart = int(w/8)
		hstart = int(h/2)
		wend = int(w*0.8)
		hend = int(h/2)
		device.drag((wstart,hstart),(wend, hend),1.0,10)
	
	#elif droid10a in id:
	#	device.drag((50, 600), (230, 600), 1.0, 10)
	
	#elif (droid10a in id) or (droid2b in id):
	elif droid10a in id or droid2b in id:
		wstart = int(w/8)
		hstart = int(h*0.75)
		wend = int(w*0.8)
		hend = int(h*0.75)
		device.drag((wstart,hstart),(wend, hend),1.0,10)
		
	elif (droid13a in id) or (droid13b in id):
		wstart = int(w/2)
		hstart = int(h*0.7)
		wend = int(w/2)
		hend = int(h*0.95)
		device.drag((wstart,hstart),(wend, hend),0.5,10)
	
	elif droid14e in id or droid14d in id:
		
		wstart = int(w/2)
		hstart = int(h*0.9)
		wend = int(w/2)
		hend = int(h*0.4)
		device.drag((wstart,hstart),(wend, hend),0.5,9)
	else:
		#print "ERROR:  unlocking phone. Can't find device ID."
		logit.error(id+" - ERROR: unlocking phone.  Can't find device ID in source code")

def Connect2Device():
	device = MonkeyRunner.waitForConnection()
	if device:
		return 1
	else:
		return 0

def AlertDialog(msg):
	if msg:
		print"> ERROR: " + msg + " \n Exiting..."
		MonkeyRunner.alert(msg)
		sys.exit(1)
	else:
		print">ERROR: empty message"
		sys.exit(1)

def goHomeScreen(device):
    #print "> Home button pressed..."
    device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)
  
def OpenBrowser(device):
	#device.shell('am start -a android.intent.action.VIEW -d http:')	
	device.shell('am start -a android.intent.action.MAIN -n com.android.browser/.BrowserActivity')
	MonkeyRunner.sleep(5)
	
def OpenFirefoxBrowser(device):
	device.shell('am start -a android.intent.action.MAIN -n org.mozilla.firefox/.App')

def getDeviceMft(device):
	mft = device.shell('getprop ro.product.manufacturer')
	return mft
	
def OpenNotification(device):
    
    mft = device.shell('getprop ro.product.manufacturer')
    
    
    #if mft.strip() == "HTC":
    if 'HTC' or 'samsung' or 'Sony' in mft:
        h,w = FindScreenSize(device)
        h = int(float(h))
        w = int(float(w))

        wstart = int(w/2)
        hstart = 0
        wend = int(w/2)
        hend = h
        device.drag((wstart,hstart),(wend,hend), 1.0, 10)

    else:
        device.press('KEYCODE_NOTIFICATION', MonkeyDevice.DOWN_AND_UP)
    
    MonkeyRunner.sleep(2)

def MenuButton(device):
    #print "> Menu button pressed..."
    device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(2)

def OpenManageApplication(device):
	print "> Opening Manage Application..."
	device.shell('am start -a android.itent.action.MAIN -n com.android.settings/.ManageApplications')
	MonkeyRunner.sleep(5)
	
def OpenSettings(device): 
    print "> Opening Settings..."
    #cmd = "adb -s " + id + " shell am start -a android.intent.action.MAIN -n com.android.settings/.Settings"
    #p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE)
    device.shell('am start -a android.intent.action.MAIN -n com.android.settings/.Settings')
    MonkeyRunner.sleep(5)

def getAndroidVersion(deviceOrID):
	
	typedeviceorid = type(deviceOrID)
	
	if typedeviceorid is str:
		cmd = "adb -s " + deviceOrID + " shell getprop ro.build.version.release"
		p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE)
		i = 0
		
		while True:
			lineread = p.stdout.readline()
			if lineread != "":
				return lineread.strip()
			else:
				return 0
		
	elif typedeviceorid ==  MonkeyDevice:
	
		cmd = "getprop ro.build.version.release"
		androidVersion = deviceOrID.shell(cmd)
		
		if androidVersion:
			androidVersion = androidVersion.strip()
			return androidVersion
		else:
			return 0
	else:
		return 0
	
def FindScreenSize(deviceOrID): 		# device or id.  Return: height, width

	DisplayWidth = "DisplayWidth"
	DisplayHeight = "DisplayHeight"
	Display = "Display:"
	height=''
	width=''
	
	androidVersion = getAndroidVersion(deviceOrID)
	
	typedeviceorid = type(deviceOrID)
	
	if typedeviceorid is str:
		cmd = "adb -s " + deviceOrID + " shell dumpsys window"
		p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE)
		i = 0
		
		while True:
			i += 1
			lineread = p.stdout.readline()

			if DisplayWidth in lineread:
				foundDisplaySize = lineread.split() 	# end up with two lines. with the height and width values
				break
			if "" == lineread:
				break
	
		for item in foundDisplaySize: 					# for each of those 2 lines
			#print item
			if DisplayWidth in item:
				width = item[-(len(item)-item.find('=')-1):]
			if DisplayHeight in item:
				height = item[-(len(item)-item.find('=')-1):]
	
		# returns in string format
		return height,width
		
		
		
	elif typedeviceorid ==  MonkeyDevice:
		dumpsysresponse = deviceOrID.shell ('dumpsys window')

		for line in dumpsysresponse.split('\n'):
			#print line
			if DisplayWidth in line:							
				for item in line.split(): 			# Split line in two (blank)...DisplayHeight and DisplayWidth are in the same line
					if DisplayWidth in item:
						width = item[-(len(item)-item.find('=')-1):]
	
					if DisplayHeight in item:
						height = item[-(len(item)-item.find('=')-1):]
				break								# stop looking for DisplahHeight, there may be more than 1 occurrences
		# returns in string format
		return height,width
		
	elif typedeviceorid == type(Struct1()): # 1/31/13 it dosen't work.
		print "device is a imageproccessresultstruct"
		
	else:
		print "ERROR: can't identify the parameter type - FindScreenSize()"
		return 0,0

def detectDevices(sn=None): 			# returns []
	devices=[]
	devicesready=[]
	devices = os.popen('adb devices').read().strip().split('\n')[1:]
	#print "> Length of array: %s" % len(devices)
	

	for id in devices:
		if 'device' in id:
			devicesready.append(id.split('\t')[0])

	if len(devicesready) < 1:
		print "> No Android devices detected"
		return devicesready
	
	elif sn is None: # return all devices ready when no serial number is present
		return devicesready
		
	elif sn in devicesready:
		print"> Found Serial Number in devices connected"
		return devicesready
		
	else:
		print "> Serial Number not found in devices connected"
		devicesready=[]
		return devicesready
		
def UninstallQuick(device):

	#logit.error(imgfile['id']+" - Uninstall App"
	if(isArbAppInstalled(device)):
		responseremove = device.removePackage(AppPackage)
		if not responseremove:
			#print"> ERROR:  quick uninstall"
			return 0
		else:
			#print"> Quick Uninstall:  successful"
			return 1
	else:
		#print ">  INFO: Appis already uninstalled"
		return 1

def isArbAppInstalled(device):
	#http://stackoverflow.com/questions/11785558/sending-logcat-input-into-monkeyrunner-through-eclipse-java-results-in-issues
	#p = subprocess.Popen(["adb", "shell", "pm list", "packages"], shell=False, stdout=subprocess.PIPE)
	
	cmd = "pm path "+ AppPackage 
	isLMinstalled = device.shell(cmd)
	
	if isLMinstalled.startswith('package:'):
		return 1
	else:
		return 0
		
def isAndroidAppInstalled(packageAppName, device):
	if "" != packageAppName:
		cmd = "pm path " + packageAppName
		isAppInstalled = device.shell(cmd)

		if isAppInstalled.startswith('package:'):
			return 1
		else:
			return 0
	else:
		print ">WARNING: isAndroidAppInstalled - empty package name"
		return 0

def isInternetOn(deviceOrID): 		
	# NO Internet connection PING response: "ping: unknown host www.google.com"
	# YES Internet connection PING resposne: "2 packets transmitted, 2 received, 0% packet loss, time 5030ms"
	# YES Internet connection but failed PING: "1 packets transmitted, 0 received, 100% packet loss, time 0ms"
	#-----------------------------------------------------------------------------------------------------------
	
	noInternet= "unknown host"
	yesInternet = "2 received"
	failInternet = "0 received"
	
	
	typedeviceorid = type(deviceOrID)
	
	if typedeviceorid == str:
		cmd = "adb -s " + deviceOrID + " shell ping -c2 www.google.com"
		p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE)
		#MonkeyRunner.sleep(2)
		
		# Julio - need to add how to handle istuation where adb response with other error device messages.
		while True:
			lineread = p.stdout.readline()
			#print "lineread %s " % lineread
			
			if yesInternet in  lineread:
				return 1
				break
			if noInternet in lineread:
				return 0
				break
			if "" == lineread:
				break
		print "ERROR:  invalid PING response - isInternetON(id)"
		return 0
	
	elif typedeviceorid == MonkeyDevice:
		cmd = "ping -c2 www.google.com"
		pingresponse = deviceOrID.shell(cmd)
		
		MonkeyRunner.sleep(5)
		#print pingresponse
		
		if not pingresponse:
			print "ping - empty or no response"
			return 0 
		elif yesInternet in pingresponse:
			return 1
		elif noInternet in pingresponse:
			return 0
		else:
			"ERROR:  invalid PING response - isInternetON()"
			return 0
	else:
		print "ERROR: can't identify the parameter type - isInternetON(device)"
		return -1
	
def isAndroidServiceRunning(ProcessName,device):
	# This will first list all Process running.  On the phone, if you go to Settings->Application->Running Services
	#  you can find all services running with it's corresponding Process. and process name
	# "adb shell service list" could also be used to list all services at boot up.  
	#-----------------------------------------------------------------------------------------
	
	cmd = "ps" #+ ProcessName
	ArbProcess = device.shell(cmd)
	#print ArbProcess
	if ProcessName in ArbProcess:
		return 1
	else:
		return 0

def isExistLMAPK(device): # Returns filename of last modified apk file
	apks=[]
	response = device.shell('ls /mnt/sdcard/download').split('\n')

	for index, apkfilename in enumerate(response):

		if 'ArbitronAndroid' in apkfilename.strip():
			#print apkfilename
			apks.append(apkfilename.strip())

	if apks:
		return apks.pop()
	else:
		return 0
		
def pullFileDeviceADB(apkName, destinationpath, deviceID):
	
	#cmd = "adb pull " + filenamePath
	cmd = "adb -s " + deviceID + " pull /mnt/sdcard/download/" + apkName + " "+ destinationpath
	procs = subprocess.Popen(cmd, stderr=subprocess.PIPE)
	
	while True:
		lineread = procs.stderr.readline() # 3002 KB/s (402785 bytes in 0.131s)
		if lineread !='':
			lineread = re.split(r'[ ()]+',lineread)
			#print lineread
			if 0 < float(lineread[2]):
				return 1
			else:
				return 0
		else:
			break

def turnScreenOff(device):
	device.press('KEYCODE_POWER', MonkeyDevice.DOWN_AND_UP)

def switchApp(device):
	device.press('KEYCODE_HOME', MonkeyDevice.DOWN)
	MonkeyRunner.sleep(2)
	device.press('KEYCODE_HOME', MonkeyDevice.UP)

def ScrollUp(device):
	
	droid21c = "0123456789ABCDEF"
	droid10a = "02885005431fc557"
	#print "> Scrolling up "
	
	h,w = FindScreenSize(device)
	h = int(float(h))
	w = int(float(w))
	
	xstart = int(w/2)
	ystart = int(h*0.2)
	xend   = int(w/2)
	yend   = int(h*0.9)
	
	device.drag((xstart,ystart),(xend,yend),0.2,10)
	MonkeyRunner.sleep(3)

def ScrollDown(device):
	h,w = FindScreenSize(device)
	h = int(float(h))
	w = int(float(w))
	
	xstart = int(w/2)
	ystart = int(h*0.8)
	xend   = int(w/2)
	yend   = int(h*0.2)
	
	device.drag((xstart,ystart),(xend,yend),0.2,10)
	MonkeyRunner.sleep(3)

def extractConfigFile(apkNamepathed):
	#NOTE - Need root access
	#.............................
	pass
	
def typeString(text2type, device):
	if "" != text2type:
		for c in text2type:
			device.type(c)
	else:
		pass

def getIMEI(device): #returns 0 if no device id present
	
	response = device.shell('dumpsys iphonesubinfo')
	if response.startswith('Phone Subscriber Info'):
		response = response.split('=')
		imei = response[2]
		return imei
	else:
		return 0
		
def getSerialNo(device): # 
	serialno = device.shell('getprop ro.serialno')
	if serialno:
		return str(serialno.strip())

def enum(**enums):
	return type('Enum',(),enums)
	
	