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
	#lprint mac_address
	#players = ['player1','player2'] #player1= iOS Player, player2 = Spotify or 3rd party player
	for player in range(99):
		current_player = dbusSession.get_object("org.bluez","/org/bluez/hci0/dev_{}/player{}".format(mac_address,player)) 
		print "Check Player {}".format(player)	
		playercontrol = getPlayer(current_player)
		if checkPlayerAvail(current_player):
			print "Found Player - {}".format(getTrackInfo(current_player))
			return current_player

def getPlayer(player_proxy):
	return dbus.Interface(player_proxy,'org.bluez.MediaPlayer1')

"""
Gets the infos for the current track
"""
def getTrackInfo(player_proxy):
	prop_mang = dbus.Interface(player_proxy,'org.freedesktop.DBus.Properties')
	return prop_mang.Get('org.bluez.MediaPlayer1','Track')

def getPlayerState(player_proxy):
	prop_mang = dbus.Interface(player_proxy,'org.freedesktop.DBus.Properties')
	return prop_mang.Get('org.bluez.MediaPlayer1','Status')

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
Executes passed args
"""
def sendcommand(player_proxy,command):
	playstring = getPlayerState(player_proxy)
	playercontrol = getPlayer(player_proxy)
	if command == 'play' or command == 'pause':
		if playstring == 'playing':
			playercontrol.Pause()
		else:
			playercontrol.Play()
	elif command == 'next':
		playercontrol.Next()
	elif command == 'previous':
		playercontrol.Previous()
	time.sleep(2)
	str = getTrackInfo(player_proxy)
	print str['Title'],"-",str['Artist'],"-",str['Album'] 
def main():
	initdbus()

if __name__ == "__main__": main()

