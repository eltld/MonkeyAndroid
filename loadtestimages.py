import sys
import os
import time
import subprocess
import re
import os.path

'''
droids = {'02885005431fc557': 'droid10A_browser_urlbox.png', 'droid10A_Click_NotifyDownloadComplete.png', \
'droid10A_Click_Install_01.png','droid10A_Click_Install_02.png','droid10A_Click_PhoneVerification.png', \
'droid10A_Click_PhoneVerificationPage_PhoneNumberReady_OK.png','droid10A_install_landingpage.png'}

droid10 = {'id': '02885005431fc557','imgInstall_01':'droid10A_browser_urlbox.png', 'droid10A_Click_NotifyDownloadComplete.png', \
'droid10A_Click_Install_01.png','droid10A_Click_Install_02.png','droid10A_Click_PhoneVerification.png', \
'droid10A_Click_PhoneVerificationPage_PhoneNumberReady_OK.png','droid10A_install_landingpage.png'}
'''
droid10a = {}
droid10a['id'] 			 		= '02885005431fc557'
droid10a['imgfoldername'] 		= 'droid10a'
droid10a['urltextbox'] 			= 'droid10a\droid10A_browser_urlbox.png'
droid10a['dlcompletenotify']	= 'droid10a\droid10A_Click_NotifyDownloadComplete.png'
droid10a['securitywarning'] 	= 'droid10a\droid10A_Click_Install_01.png'
droid10a['installed'] 			= 'droid10a\droid10A_Click_Install_02.png'
droid10a['phoneverify'] 		= 'droid10a\droid10A_Click_PhoneVerification.png'
droid10a['phoneOKbutton'] 		= 'droid10a\droid10A_Click_PhoneVerificationPage_PhoneNumberReady_OK.png'
droid10a['landingpage'] 		= 'droid10a\droid10A_install_landingpage.png'
droid10a['sdcardpath']			= 'mnt/sdcard/'

#-- droid 21c not tested ----
droid21c = {}
droid21c['id'] 			 		= '0123456789ABCDEF'
droid21c['imgfoldername'] 		= 'droid21c'
droid21c['urltextbox'] 			= 'droid21c\droid21C_browser_urlbox.png'
droid21c['dlcompletenotify']	= 'droid21c\droid21C_Click_NotifyDownloadComplete.png'
droid21c['securitywarning'] 	= 'droid21c\droid21C_Click_Install_01.png'
droid21c['installed'] 			= 'droid21c\droid21C_Click_Install_02.png'
droid21c['phoneverify'] 		= 'droid21c\droid21C_Click_PhoneNumberVerification.png'
droid21c['phoneOKbutton'] 		= 'droid21c\droid21c_Click_PhoneVerificationPage_PhoneNumberReady_OK.png'
droid21c['landingpage'] 		= 'droid21c\droid21c_install_landingpage.png'

#-- droid 14d not tested ----
droid14d = {}
droid14d['id'] 			 		= 'SH1ART501305'
droid14d['imgfoldername'] 		= 'droid14d'
droid14d['urltextbox'] 			= 'droid14d\droid14d_browser_urlbox.png'
droid14d['dlcompletenotify']	= 'droid14d\droid14d_Click_NotifyDownloadComplete.png'
droid14d['securitywarning'] 	= 'droid10a\droid10A_Click_Install_01.png'#'droid14d\droid14d_Click_Install_01.png'
droid14d['installed'] 			= 'droid10a\droid10A_Click_Install_02.png'#'droid14d\droid14d_Click_Install_02.png'
droid14d['phoneverify'] 		= 'droid10a\droid10A_Click_PhoneVerification.png'#'droid14d\droid14d_Click_PhoneNumberVerification.png'
droid14d['phoneOKbutton'] 		= 'droid10a\droid10A_Click_PhoneVerificationPage_PhoneNumberReady_OK.png'#'droid14d\droid14d_Click_PhoneVerificationPage_PhoneNumberReady_OK.png'
droid14d['landingpage'] 		= 'droid14d\droid14d_install_landingpage.png'
droid14d['sdcardpath']			= 'mnt/sdcard/'


#-- droid 13a not tested ----
droid13a = {}
droid13a['id'] 			 		= 'HT176HL09379'
droid13a['imgfoldername'] 		= 'droid13a'
droid13a['urltextbox'] 			= 'droid13a\droid13a_browser_urlbox.png'
droid13a['dlcompletenotify']	= 'droid13a\droid13a_Click_NotifyDownloadComplete.png'
droid13a['securitywarning'] 	= 'droid13a\droid13a_Click_Install_01.png'#'droid13a\droid13a_Click_Install_01.png'
droid13a['installed'] 			= 'droid13a\droid13a_Click_Install_02.png'#'droid13a\droid13a_Click_Install_02.png'
droid13a['phoneverify'] 		= 'droid13a\droid13a_Click_PhoneVerification.png'#'droid13a\droid13a_Click_PhoneNumberVerification.png'
droid13a['phoneOKbutton'] 		= 'droid13a\droid13a_Click_PhoneVerificationPage_PhoneNumberReady_OK_big.png'#'droid13a\droid13a_Click_PhoneVerificationPage_PhoneNumberReady_OK.png'
droid13a['phoneOKbutton2'] 		= 'droid13a\droid13a_Click_PhoneVerificationPage_PhoneNumberReady_OK_small.png'#'droid13a\droid13a_Click_PhoneVerificationPage_PhoneNumberReady_OK.png'
droid13a['landingpage'] 		= 'droid13a\droid13a_install_landingpage.png'

#-- droid 13b not tested ----
droid13b = {}
droid13b['id'] 			 		= 'HT188HL04500'
droid13b['imgfoldername'] 		= 'droid13a'
droid13b['urltextbox'] 			= 'droid13a\droid13a_browser_urlbox.png'
droid13b['dlcompletenotify']	= 'droid13a\droid13a_Click_NotifyDownloadComplete.png'
droid13b['securitywarning'] 	= 'droid13a\droid13a_Click_Install_01.png'#'droid13a\droid13a_Click_Install_01.png'
droid13b['installed'] 			= 'droid13a\droid13a_Click_Install_02.png'#'droid13a\droid13a_Click_Install_02.png'
droid13b['phoneverify'] 		= 'droid13a\droid13a_Click_PhoneVerification.png'#'droid13a\droid13a_Click_PhoneNumberVerification.png'
droid13b['phoneOKbutton'] 		= 'droid13a\droid13a_Click_PhoneVerificationPage_PhoneNumberReady_OK_big.png'#'droid13a\droid13a_Click_PhoneVerificationPage_PhoneNumberReady_OK.png'
droid13b['phoneOKbutton2'] 		= 'droid13a\droid13a_Click_PhoneVerificationPage_PhoneNumberReady_OK_small.png'#'droid13a\droid13a_Click_PhoneVerificationPage_PhoneNumberReady_OK.png'
droid13b['landingpage'] 		= 'droid13a\droid13a_install_landingpage.png'

#-- droid 14E not tested ----
droid14e = {}
droid14e['id'] 			 		= 'HT17KV800328'
droid14e['imgfoldername'] 		= 'droid14e'
droid14e['urltextbox'] 			= 'droid14e\droid14e_browser_urlbox.png'
droid14e['dlcompletenotify']	= 'droid14e\droid14e_Click_NotifyDownloadComplete.png'
droid14e['securitywarning'] 	= 'droid10a\droid10A_Click_Install_01.png'#'droid14e\droid14e_Click_Install_01.png'
droid14e['installed'] 			= 'droid10a\droid10A_Click_Install_02.png'#'droid14e\droid14e_Click_Install_02.png'
droid14e['phoneverify'] 		= 'droid10a\droid10A_Click_PhoneVerification.png'#'droid14e\droid14e_Click_PhoneNumberVerification.png'
droid14e['phoneOKbutton'] 		= 'droid10a\droid10A_Click_PhoneVerificationPage_PhoneNumberReady_OK.png'#'droid14e\droid14e_Click_PhoneVerificationPage_PhoneNumberReady_OK.png'
droid14e['landingpage'] 		= 'droid14e\droid14e_install_landingpage.png'

#-- droid 40 not tested Samsung S3----
droid40 = {}
droid40['id'] 			 		= '91894a49'
droid40['imgfoldername'] 		= 'droid40'
droid40['urltextbox'] 			= 'droid40\droid40_browser_urlbox.png'
droid40['dlcompletenotify']		= 'droid40\droid40_Click_NotifyDownloadComplete.png'
droid40['securitywarning'] 		= 'droid10a\droid10A_Click_Install_01.png'#'droid40\droid40_Click_Install_01.png'
droid40['installed'] 			= 'droid10a\droid10A_Click_Install_02.png'#'droid40\droid40_Click_Install_02.png'
droid40['phoneverify'] 			= 'droid10a\droid10A_Click_PhoneVerification.png'#'droid40\droid40_Click_PhoneNumberVerification.png'
droid40['phoneOKbutton'] 		= 'droid10a\droid10A_Click_PhoneVerificationPage_PhoneNumberReady_OK.png'#'droid40\droid40_Click_PhoneVerificationPage_PhoneNumberReady_OK.png'
droid40['landingpage'] 			= 'droid40\droid40_install_landingpage.png'
droid40['sdcardpath']			= 'storage/sdcard0/'



appTrackList={}
appTrackList['Facebook']	= ("com.facebook.katana","com.facebook.katana/.LoginActivity")
#appTrackList['AngryBirds']	= ("com.rovio.angrybirds","")
appTrackList['Pandora']		= ("com.pandora.android","com.pandora.android/.Main")
appTrackList['FruitNinja']	= ("com.halfbrick.fruitninjafree","com.halfbrick.fruitninjafree/com.halfbrick.fruitninja.FruitNinjaActivity")
appTrackList['Twitter']		= ("com.twitter.android","com.twitter.android/.StartActivity")
appTrackList['Instagram']	= ("com.instagram.android","com.instagram.android/.activity.MainTabActivity")
appTrackList['Gmail']		= ("com.google.android.gm","com.google.android.gm/.ConversationListActivityGmail")


