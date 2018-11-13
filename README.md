# Make your own voice controlled light switch - that really works!

<img src="images/pizerospeach1.jpg" alt="Pi Zero Switch" width="500">

Once you've had a Google Home or Alexa for a while you realise voice control is the future, but don't you just hate the way these current products have to send your voice off over the Internet to their big brother servers just to switch your local lights on, not to mention the annoying way they always give the unnecessary verbal confirmation - "Alright, switching off the bedroom light" - which you can already see perfectly well by the light having just gone off.

This shows you how to make your own voice controlled switch that avoids these problems, works well, and costs less than £20. It uses a Raspberry Pi Zero so is small and descrete, along with open source software based on Tensorflow machine learning. 

## Marvin and Sheila

To control your lights in an ideal world you would say something obvious like "lights on" and "lights off", however there are a couple of problems with those phrases.

One is "lights on" and "lights off" are very similar, both being mainly "lights o" and only differing by the end "n" and "ff", so using these gives annoying mis-detection errors.

Better could be something like "lamp on" and "lights off" but the problem with that is that there are no recordings of people saying "lamp" and we need lots of recordings of actual speech to train the machine learning neural network with. Without thousands of samples to train the model it is unreliable and doesn't work very well with different peoples voices. So, to have something that actually works well this uses the keywords "Marvin" and "Sheila" to switch the lights on and off. There are sample recordings of thousands of people saying these (see [Google's Speech Commands Dataset](https://ai.googleblog.com/2017/08/launching-speech-commands-dataset.html)) so the trained model is accurate and the phrases are quite different which minimises mis-triggering.

You'll probably think its odd saying Marvin and Sheila to control your lights, but it doesn't have all the "hey google" cruft or privacy violoations, so you quickly get used to and even prefer it.

## What you need:

- Raspberry Pi Zero (non-Wifi version is fine)
- micro SD Card (8GB is fine) 
- I2S Microphone, eg SPH0645
- 433MHz transmitter module
- 433MHz remote control mains socket
- Pi Zero case to make it look nice

## Steps:

### Setup the Raspberry Pi Zero

Using the non-Wifi version of the Pi Zero its easiest to set it up for access from a PC over a USB cable. 

**1.** Flash Raspbian Stretch Lite [onto the SD card](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).    
**2.** Once Raspbian is flashed, open up the boot partition (in Windows Explorer, Finder etc) and add to the bottom of the ```config.txt``` file ```dtoverlay=dwc2``` on a new line, then save the file.    
**3.** Now create a new file simply called ```ssh``` in the SD card as well. By default SSH is disabled so this is required to enable it. **Remember** - Make sure your file doesn't have an extension (like .txt etc)!    
**4.** Finally, open up the ```cmdline.txt```. Be careful with this file, it is very picky with its formatting! Each parameter is seperated by a single space (it does not use newlines). Insert ```modules-load=dwc2,g_ether``` after ```rootwait```. To compare, an edited version of the ```cmdline.txt``` file at the time of writing, can be found [here](http://pastebin.com/WygSaptQ).    

(See [this guide](https://gist.github.com/gbaman/975e2db164b3ca2b51ae11e45e8fd40a) for full details.) 

All that done, connect the Pi to your PC with a USB cable, wait 90 seconds for it to boot up (you should see the green LED on the Pi flashing a bit as it boots) and then you should be able to logon to the Pi from your PC with ```ssh pi@raspberrypi.local``` and the password ```raspberry```. 

Along with logging on with SSH you can also copy files from your PC to the Pi Zero with: ```scp /path/to/file pi@raspberrypi.local:~``` and copy files from the Pi to your PC with: ```scp  pi@raspberrypi.local:/path/to/file .``` 

### Connect up the I2S mic and 433MHz transmitter modules

<img src="images/fritzing.png" alt="Fritzing Diagram" width="500">

### Configure Raspbian for the I2S Microphone

Raspbian Stretch doesn't come with default support for the SPH0645 I2S microphone so you need to tweak the config for it. Edit the Pi's ```/boot/config.txt``` file to comment out the line ```dtparam=audio=on``` and to add the line ```dtoverlay=googlevoicehat-soundcard```. So the result looks like:
```
# Enable audio (loads snd_bcm2835)
# dtparam=audio=on
dtoverlay=googlevoicehat-soundcard
```
and then reboot the Pi with ```sudo reboot```

Once rebooted ssh back in and verify that the mic is now available with the ```arecord -l``` command:
```
pi@raspberrypi:~ $ arecord -l
**** List of CAPTURE Hardware Devices ****
card 0: sndrpigooglevoi [snd_rpi_googlevoicehat_soundcar], device 0: Google voiceHAT SoundCard HiFi voicehat-hifi-0 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

You should now be able to record audio with the mic. To test that enter the command ```arecord -D plughw:0 -c1 -r 16000 -f S16_LE -t wav -V mono -v file.wav```, near the mic say something or make some noise, and then hit ctrl-c to stop the recording. Now transfer the recording to your PC so you can play it to confirm it is capturing sound - from the PC enter ```scp  pi@raspberrypi.local:file.wav .``` and now play the file, for example, on a Mac ```play file.wav```. You should hear the sounds you made when recording, it may be quite quiet but thats ok.

### The code

The code is a Python script which uses the [Nyumaya Audio Recognition](https://github.com/nyumaya/nyumaya_audio_recognition) project to do the speech recognition and [rpi-rf](https://github.com/milaq/rpi-rf) for the remote control mains switch. 

There are a few options for doing speech recognition on a Pi Zero. One is [Snowboy](https://snowboy.kitt.ai/) which has some nice features but it doesn't seem as accurate as Nyumaya. Another is [Porcupine](https://github.com/Picovoice/Porcupine) which is able to create models from English text so doesn't need all the audio samples, however its aimed at comercial customers and without a license you can't create custom models for the Pi and he wouldn't give me a personal license even when offering to pay. Finaly there is the completely DIY approach which is where I started - Google's open source machine learning project TensorFlow has a [speech recognition example](https://www.tensorflow.org/tutorials/sequences/audio_recognition) which is based on the research paper [Convolutional Neural Networks for Small-footprint Keyword Spotting](https://www.isca-speech.org/archive/interspeech_2015/papers/i15_1478.pdf). That is improved on by a later paper at the end of 2017, [Honk: A PyTorch Reimplementation of Convolutional
Neural Networks for Keyword Spoting](https://arxiv.org/pdf/1710.06554.pdf) with an associated open source project, [Honk](https://github.com/castorini/honk). I found the code in Honk hard to make sense of and then I came across Nyumaya which I understand is based on the Honk model with some further improvements and its much easier to use. Nyumaya unfortunately hasn't open sourced the model generation code yet, but the guy behind Nyumaya is incredibly responsive and helpful so thats what this is using presently.     

Anyway, clone or download a zip of this repo to you PC and then copy it to the Pi Zero with ```scp -r path/to/voice-controlled-switch/ pi@raspberrypi.local:~/pi-voice-switch/```

So that this runs when the Pi Zero is booted edit the boot file ```xyz``` to include the line ```abc```. It should look like this:
```
```

There are two settings you can adjust to suit your environment. One is the volume level of the microphone and the other is the sensitivity of the speach recognition model. 

As you saw when doing the test recording from the mic its volume is quite low, so for your voice to be picked up from across the room you need to boost the volume. In my living room a value of 14 seems about right and lets me speak quite quietly across the room and still have the Marvin/Sheila picked up.

The sensitivity of the speech recognition adjusts how accurately it detects the hotwords. This ranges from 0.0 to 1.0 with a higher value meaning its more accurate. If you set this low then it will more often mis-trigger, especially from sounds from TV and music, setting it higher means you need to be more clearer speaking the Marvin/Sheila words.    

### Putting it all together

The official Rasperry Pi Zero case includes a camera cover which has a hole in the front perfect for the microphone and it also has inside some raised tags which are pefectly spaced to tightly hold the microphone in place behind the hole. Inside the case there is also just enough space for the 433 MHz transmitter module. I've put a square of plastic insulator (cut from the bag the I2S mic came in) on the back of the transmitter to avoid any shorts if it touches the Pi circuit board, and held it on just with a blob of blutack. There is not a lot of spare space inside the Pi Zero case so I've connected the parts up with 32 AWG servo wire, which is a bit thinner and flexible compared to standard breadboard jumber cable.

<img src="images/pizerospeach2.jpg" alt="Pi Zero inside 1" width="300"> <img src="images/pizerospeach3.jpg" alt="Pi Zero inside 2" width="300">

