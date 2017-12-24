import dbus

# A small script that returns the status of a running music player and tries to parse artist, album and title strings and return them to STDOUT. Returns "Nothing Playing" if no player is found.
def getCurrentPlayerStatus():
    bus = dbus.SessionBus()
    try:
        player = bus.get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
        properties = dbus.Interface(player, dbus_interface='org.freedesktop.DBus.Properties')

        return properties.GetAll('org.mpris.MediaPlayer2.Player')
    except dbus.exceptions.DBusException:
        return None


playerStatus = getCurrentPlayerStatus()
if playerStatus and playerStatus['PlaybackStatus'] == 'Playing':
    metadata = playerStatus['Metadata']
    title = metadata['xesam:title']
    album = metadata['xesam:album']
    artist = metadata['xesam:artist'][0]

    print("{} - {}, from the Album: {}".format(artist, title, album))
else:
    print("Nothing playing")

