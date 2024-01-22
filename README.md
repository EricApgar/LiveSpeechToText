# LiveSpeechToText
Live speech to text transcription. Ambient sound is analyzed and parsed into sections of words that are streamed to a voice model that prints to the screen the text for the detected speech. Works completely offline - no streaming to a service or external connections to websites or 3rd party services needed.

There is a rudimentary (but adjustable) system for determining whether or not to send sound bytes to the text prediction model. If the sound level is over a certain (adjustable) threshold then a clip is passed to the model. The individual clip stops recording and gets passed to the model after it detects a lull in sound (adjustable time period) signifying the end of a word or sentence. 

# Requirements:

## Requires Python 3.7.8 to work. 

### See [here](https://www.python.org/downloads/release/python-378/) for python package download.

Virtual environment can be created based off of "requirements.txt".

## Linux:
On linux (RPi), you might have to run:
```
sudo apt install portaudio19-dev python3-pyaudio
```

This should fix an error when installing from requirements.txt that yells about portaudio installing when trying to install "PyAudio" which is a library in requirements.txt that is needed.

---

Make sure that some sort of recording capable device is connected. 

# Methods:

## 1. Stream sound samples to model (RECOMMENDED)

### **Associated file:** model_streaming.py

Summary: This is by far the best method. Run this file to start the program. Adjust the parameters at the bottom of the file to change the time it will run for.

* Record super short samples of sound (~.1 seconds in length).
* Analyze each sample for exceeding a sound threshold above an adjustable limit.
* Continuously build a buffer of sound samples that contain sound above the threshold.
* Once you have a sample where the threshold is NOT exceeded, assume that this is the end of the phrase or word and stop building the buffer.
* Send the whole buffer to the model directly to be transcribed into text.
* Go back to listening for sound.

## 2. Record a series of .wav clips to pass to the model.

### **Associated file:** cycle_wav.py

Summary: This samples super short clips of sound (n-seconds) and connects them together to create a single coherent audio sample. That single sample is then fed to the model.

* Super janky method.  
* Start recording n-second samples.  
* After every n seconds, save the audio as a .wav file.  
* Send that audio to the model to translate to text.  
* Delete the audio file.  
* Repeat.  

# Seeed Studio Microphone Hat Setup:
The Hin Tak repo seems to still be making current changes and support for the Respeaker Sound Cards (by Seeed Studio). I recommend the instructions on their [repo](https://github.com/HinTak/seeed-voicecard).

As a secondary, Adafruit has instructions for the sound card they sell which seems to be the same basic card (at least physically) and their [instructions](https://learn.adafruit.com/adafruit-voice-bonnet/audio-setup) also look the same (because I think it's the same drivers which supports the idea that the sound cards are the same).

[Instructions from Seeed](https://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT_Raspberry/) are the third resource for posterity and information but the last time their GitHub was updated was 2021 which is not encouraging.

Connect the HAT to the RPi. Make sure that the HAT is connected properly in orientation and that the pins are all lined up (it's suprisingly easy to be offset by a pin or two). **Make sure that the HAT is powered** (not from the RPi, but from another external power source, like where the RPi draws power from).

### Install the HAT drivers.
```
git clone https://github.com/HinTak/seeed-voicecard
cd seeed-voicecard
sudo ./install.sh
sudo reboot now
```

Once rebooted, check to make sure the HAT shows up. This should list all available sound recording devices.
```
arecord -l
```

You should see something like "seeed2micvoicec" listed under the recording devices.

# Notes:
**The preferred method is to create a python virtual environment using "venv" and the "requirements.txt" file.**

If you make an environment through Anaconda, you could get some other issues regarding a need for the "ffmpeg" library. When you run the first time you might get an error about "ffmpeg". This library is needed by the transformers library, but doesn't technically show up as a referenced library with the typical import.

I didn't get this error creating a venv so maybe just don't use Anaconda.

```
conda install ffmpeg
```

## Notes on Installing things in Linux:

Download the python tarball (.tar.xz file) from Python website:
```
$ wget https://www.python.org/ftp/python/3.7.8/Python-3.7.8.tar.xz
```
By default, this file is downloaded into the "/home/pi/" directory - I think because the default location for the command window is here, so unless you change that location when you open the command window, the tar file will download here.

Install python from the tarball file:
```
$ tar -xf Python-3.7.8.tar.xz
```
A folder called "Python-3.7.8" should now be created at the location of the tarball file. 

Change dir into the python folder and then "configure" the system. This configure step can take a while - 15 min?
```
$ cd Python-3.7.8
$ ./configure --enable-optimizations
```

Once it's configured, create an alternate install of python for the new version. This step can take a long time (>1 hour).
```
$ sudo make altinstall
```

Python 3.7.8 should now be available. Im still not clear on the intricacies of how the multiple python versions are accessed. For instance, the three related calls to python below correspond to running python==2.7, python==3.7.3, and python==3.7.8 respectively.
```
$ python
$ python3
$ python3.7
```
It has something to do with which versions are already installed, and the process that it goes through to run a specific version, but I don't know the specifics.

The actual executable for this new version of Python is located at "/usr/loca/bin/python3.7

## Changing what version of python activates in command window:

List the current alternatives for python. Since you likely have none, **this will likely result in an error**.
```
sudo update-alternatives --list python
```

So, let's actually update the list.
```
sudo update-alternatives --install "<full path to current python exe>" python "<full path to alternate python exe>" 1
```

Here's an example with actual information. In this case, we map (?) the current python executable (which is the default Python 2) to a new install of python that I did manually (Python 3.7.8):
```
sudo update-alternatives --install "/usr/bin/python" python "/usr/local/bin/python3.7" 1
```

## THE FOLLOWING INSTRUCTIONS DID NOT SEEM TO WORK (controlled for posterity):

Which version of python that is referenced when called in the command window can be changed by editing some file.

Open ~/.bashrc file using nano:
```
$ sudo nano ~/.bashrc
```

Add a new alias on the top of the file to change your default python executable:
```
alias python3='python3.7.8'
```
You could also change the alias to something else, like just "python" as opposed to "python3":
```
alias python='python3.7.8'. 
```

Once done, exit nano and source your .bashrc file:
```
. ~/.bashrc
```

## Other:
Need instructions on installing a new version of python in linux. How to add it to the path (so its startable from the command line), and how to specify location (and what location is preferrable if there is one).

It installed in /home/pi but I'm not sure if I set that or not.
 
Where to install virtualenv to. It doesnt automatically get added to the path either when you install which is maybe something you want.



# Future:
1. Detecting if a given clip had spoken voice in it as opposed to just a sound above the threshold.

# Problem Notes:

My stream of conscious notes on how to solve the problem.

* There's always a problem of cutting off a speaker mid-word if you sample audio at a set interval.
* You usually sample audio for x seconds (I've been doing x=1) and then pipe that sound to the model.
    * The problem is that the model takes about 1/5 of a second to run - longer for a longer segment. This delay isn't that long but by the time you predict and go back to sampling audio, you've lost a decent amount of time which could be in the middle of a word and that throws off all the predictions.
* If you wait to send audio to the model before you 
* Even if you don't sample at a set interval and you wait to detect a sound befor your ,

## Idea:
* Record audio for a very short amount of time (.2 seconds?) and immediately analyze the numpy array to see if the audio level has dropped to zero (or just a low number). This signals the end of a word. Make sure that the pause is long enough that its not just a pause in the middle of the word. If it's not the end, then keep reading audio samples into the array until you hit the dead zone.
    * Checking if the end of the array is a dead zone should be such a quick operation that the time away from recording audio should hopefully not cut out enough audio to mess with the sample. Have to check this though.
* Once the dead zone is confirmed, send the sample to the model.
* Repeat the process.
* This could be great for single words, but slurring words together or speaking quickly could be an issue. Getting the timing right between the words could be tricky.
    * At a certain point, there should be a timing cutoff to prevent a long string of unbroken speech for being too much for the model. At that point though, you likely didn't want to pass this to the model anyways.


# Notes

Check version of pip for specific python version:
```
pi@raspberrypi:~ $ python3.7 -m pip --version
```
