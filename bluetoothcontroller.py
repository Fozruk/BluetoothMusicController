import time
import dbus
import sys
from os.path import expanduser

def initdbus():
	dbusSession = dbus.SystemBus()
	#bluezManager = busSession.get_object("org.bluez","/org/bluez/hci0/dev_CC_29_F5_A5_C9_4A/player1")
	#playerevent = dbus.Interface(meem,'org.bluez.MediaPlayer1')
	player = getCurrentPlayer(dbusSession)
	print sys.argv
	command = sys.argv[1]
	sendcommand(player,command)

def getCurrentPlayer(dbusSession):
	mac_address = open(expanduser("~")+"/.config/.bluetoothplayer.conf").read().replace(":","_").replace("\n","")
	#lprint mac_address
	players = ['player1','player2'] #player1= iOS Player, player2 = Spotify or 3rd party player
	for player in players:
		current_player = dbusSession.get_object("org.bluez","/org/bluez/hci0/dev_{}/{}".format(mac_address,player)) 
		playercontrol = getPlayer(current_player)
		if checkPlayerAvail(current_player):
			print "Found Player - {}".format(getTrackInfo(current_player))
			return current_player

def getPlayer(player_proxy):
	return dbus.Interface(player_proxy,'org.bluez.MediaPlayer1')

def getTrackInfo(player_proxy):
	prop_mang = dbus.Interface(player_proxy,'org.freedesktop.DBus.Properties')
	return prop_mang.Get('org.bluez.MediaPlayer1','Track')

def getPlayerState(player_proxy):
	prop_mang = dbus.Interface(player_proxy,'org.freedesktop.DBus.Properties')
	return prop_mang.Get('org.bluez.MediaPlayer1','Status')

def checkPlayerAvail(player_proxy):
	try:
		prop_mang = dbus.Interface(player_proxy,'org.freedesktop.DBus.Properties')
		str = prop_mang.Get('org.bluez.MediaPlayer1','Track')
	except dbus.exceptions.DBusException:
		print "DBusException, wrong player"
		return False
	return True

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
	else:
		print "wtf"

def main():
	initdbus()

if __name__ == "__main__": main()
