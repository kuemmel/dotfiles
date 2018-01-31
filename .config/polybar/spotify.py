import dbus
import subprocess

COLOR_PRIMARY = "%{F#ffb52a}"
COLOR_SECONDARY = "%{F#e60053}"
COLOR_ALT = "%{F#0a81f5}"
COLOR_CLOSE = "%{F-}"

# A small script that returns the status of a running music player and tries to parse artist, album and title strings and return them to STDOUT. Returns "Nothing Playing" if no player is found.
def getCurrentPlayerStatusFromSpotify():
    bus = dbus.SessionBus()
    try:
        player = bus.get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
        properties = dbus.Interface(player, dbus_interface='org.freedesktop.DBus.Properties')

        return properties.GetAll('org.mpris.MediaPlayer2.Player')
    except dbus.exceptions.DBusException:
        return None

def getCurrentPlayerStatusFromCMus():
    status = {}
    try:
        playerStatus = subprocess.check_output(["cmus-remote", "-Q"], stderr=subprocess.STDOUT).split("\n")
        if playerStatus[0] == 'status playing':
            status['PlaybackStatus'] = 'Playing'
            metadata = {}
            status['Metadata'] = metadata
            metadata['xesam:artist'] = playerStatus[4][11::]
            metadata['xesam:album'] = playerStatus[5][10::]
            metadata['xesam:title'] = playerStatus[6][10::]
        elif playerStatus[0] == 'status paused':
            status['PlaybackStatus'] = 'Paused'
        else:
            status['PlaybackStatus'] = 'Not Running'
    except subprocess.CalledProcessError, e:
        status['PlaybackStatus'] = 'Not Running'

    return status

def displayStatus(playerStatus):
    metadata = playerStatus['Metadata']
    title = metadata['xesam:title']
    album = metadata['xesam:album']
    if type(metadata['xesam:artist']) is not str:
        artist = metadata['xesam:artist'][0]
    else:
        artist = metadata['xesam:artist']

    print("{}{}{} (by {}{}{}) (album {}{}{})"
          .format(COLOR_PRIMARY, title, COLOR_CLOSE, COLOR_SECONDARY,
                  artist, COLOR_CLOSE, COLOR_ALT, album, COLOR_CLOSE))

playerStatus = getCurrentPlayerStatusFromSpotify() or getCurrentPlayerStatusFromCMus()
if playerStatus['PlaybackStatus'] == 'Playing':
    print(displayStatus(playerStatus))
elif playerStatus['PlaybackStatus'] == 'Paused':
    print("Playback paused")
else:
    print("No Playback")

