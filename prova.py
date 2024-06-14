import vlc
import time
import socket
import pam
import threading

player = vlc.MediaPlayer("test.mp4")

player.play()

time.sleep(10)

player.stop()