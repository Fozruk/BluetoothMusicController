import time
import dbus
import sys
from os.path import expanduser

"""
Initializes the dbus session. This needs to be the systembus because the session bus
requires a X11 desktop for some reason
"""
def initdbus():
	dbusSession = dbus.SystemBus()
	#bluezManager = busSession.get_object("org.bluez","/org/bluez/hci0/dev_CC_29_F5_A5_C9_4A/player1")
	#playerevent = dbus.Interface(meem,'org.bluez.MediaPlayer1')
	player = getCurrentPlayer(dbusSession)
	print sys.argv
	command = sys.argv[1]
	sendcommand(player,command)

"""
Gets the current player which currently plays music on the device
Dbus needs the mac address of the phone, store it here:
~/.config/.bluetoothplayer.conf
"""
def getCurrentPlayer(dbusSession):
	mac_address = open(expanduser("~")+"/.config/.bluetoothplayer.conf").read().replace(":","_").replace("\n","")
	#print mac_address
	players = ['player1','player2'] #player1= iOS Player, player2 = Spotify or 3rd party player
	for player in players:
		player_proxy = dbusSession.get_object("org.bluez","/org/bluez/hci0/dev_{}/{}".format(mac_address,player)) 
		playercontrol = dbus.Interface(player_proxy,'org.bluez.MediaPlayer1')
		if checkPlayerAvail(player_proxy):
			print "Found Player - {}".format(getTrackInfo(player_proxy))
			return playercontrol

"""
Gets the infos for the current track
"""
def getTrackInfo(player_proxy):
	prop_mang = dbus.Interface(player_proxy,'org.freedesktop.DBus.Properties')
	return prop_mang.Get('org.bluez.MediaPlayer1','Track')

"""
Checks if the passed player currently played music. On iOS every player seems to have
a different dbus address (f.e. stock ios player has "player1" and spotify has "player2")
This method tries to get a track info from the passed player. If the player is not currently
used dbus will throw an exception.
"""
def checkPlayerAvail(player_proxy):
	try:
		prop_mang = dbus.Interface(player_proxy,'org.freedesktop.DBus.Properties')
		str = prop_mang.Get('org.bluez.MediaPlayer1','Track')
	except dbus.exceptions.DBusException:
		print "DBusException, wrong player"
		return False
	return True

"""
The commands that can be issued to the player
"""
def sendcommand(playercontrol,command):
	if command == 'play':
		playercontrol.Play()
	elif command == 'pause':
		playercontrol.Pause()
	elif command == 'next':
		playercontrol.Next()
	elif command == 'previous':
		playercontrol.Previous()
	else:
		print "wtf"

def main():
	initdbus()

if __name__ == "__main__": main()
