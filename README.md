# voice-controlled-switch

<img src="images/pizerospeach1.jpg" alt="Pi Zero Switch" width="500">

## Make your own voice controlled light switch - that really works!

Once you've had a Google Home or Alexa for a while you realise voice control is the future, but don't you just hate the way these current products have to send your voice off over the Internet to their big brother servers just to switch your local lights on, not to mention the annoying way they always give the unnecessary verbal confirmation - "Alright, switching off the bedroom light" - which you can see perfectly well already by the light having just gone off.

This shows you how to make your own voice controlled switch that avoids these problems, works well, and costs less than £20. It uses a Raspberry Pi Zero so is small and descrete, along with open source software based on Tensorflow machine learning. 

## Marvin and Sheila

To control your lights in an ideal world you would say something obvious like "lights on" and "lights off", however there are a couple of problems with those phrases.

One is "lights on" and "lights off" are very similar, both being mainly "lights o" and only differing by the end "n" and "ff", so using these gives annoying mis-detection errors.

Better could be something like "lamp on" and "lights off" but the problem with that is that there are no recordings of people saying "lamp" and we need recordings of actual speech to train the machine learning model with. Without thousands of samples to train the model it is unreliable and doesn't work for many different peoples voices. So, to have something that actually works well I've used the keywords "Marvin" and "Sheila" to switch the lights on and off. There are sample recordings of thousands of people saying these so the trained model is accurate and the phrases are quite different which minimises mis-triggering.

You'll think it sounds odd saying Marvin and Sheila to control your lights, but it doesn't have all the "hey google" cruft or violate your privacy while bringing the benefits of voice control so you quickly get used to it.

## What you need:

- Raspberry Pi Zero (non-Wifi version is fine)
- I2S Microphone, eg SPH0645
- 433MHz transmitter module
- 433MHz remote control mains socket
- Pi Zero case to make it look nice

## Steps:

### Setup the Raspberry Pi Zero

Using the non-Wifi version of the Pi Zero its easiest to set it up for access from a PC over a USB cable. Install a fresh copy of [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) onto an SD Card. Configure it for USB access following [this guide](https://gist.github.com/gbaman/975e2db164b3ca2b51ae11e45e8fd40a). 

All that done, connect the Pi to your PC with a USB cable, wait 90 seconds for it to boot up (you should see the green LED on the Pi flashing a bit as it boots) and then you should be able to logon to the Pi from your PC with ```ssh pi@raspberrypi.local``` and the password ```raspberry```. 

You can also copy files from you PC to the Pi Zero with: ```scp /path/to/file pi@raspberrypi.local:~```

<img src="images/fritzing.png" alt="Fritzing Diagram" width="500">

<img src="images/pizerospeach2.jpg" alt="Pi Zero inside 1" width="500">

<img src="images/pizerospeach3.jpg" alt="Pi Zero inside 2" width="500">

