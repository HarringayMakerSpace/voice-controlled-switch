import time
import os
import argparse
import sys
import datetime
import platform
from subprocess import call

from multi_detector import MultiDetector
from record import AudiostreamSource
	
lib = "/home/pi/voice-controlled-switch/lib/libnyumaya.so"
hotword_graph="/home/pi/voice-controlled-switch/marvin_sheila_small.tflite"
hotword_labels="/home/pi/voice-controlled-switch/marvin_sheila_labels.txt"

def light_on():
	call("sudo ifconfig wlan0 hw ether 36:01:22:33:44:01", shell=True)
	call("sudo iwlist wlan0 scan", shell=True)
	print("Turning light on")

def light_off():
	call("sudo ifconfig wlan0 hw ether 36:01:22:33:44:02", shell=True)
	call("sudo iwlist wlan0 scan", shell=True)
	print("Turning light off")

def label_stream():
	
	mDetector = MultiDetector(lib,timeout=20)
	
	mDetector.add_detector(hotword_graph, hotword_labels, 0.8)
	
	mDetector.SetGain(14)
	mDetector.RemoveDC(True)
	
	mDetector.add_command("marvin", light_on)
	mDetector.add_command("sheila", light_off)

	bufsize = mDetector.GetInputDataSize()
	audio_stream = AudiostreamSource()
	audio_stream.start()

	try:
		while(True):
			frame = audio_stream.read(bufsize,bufsize)
 
			if(not frame):
				time.sleep(0.01)
				continue

			mDetector.run_frame(frame)

	except KeyboardInterrupt:
		print("Terminating")
		audio_stream.stop()
		sys.exit(0)


if __name__ == '__main__':
	label_stream()

