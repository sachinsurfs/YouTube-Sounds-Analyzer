#!/usr/bin/env python3

'''
Python script for analyzing audios and separting gun sounds. 

'''

import pyaudio
import wave
import numpy as np
import os
import math
for file in os.listdir("./noise"):
    if file.endswith(".wav"):
            #Affects quality. Can be increased for better quality
            chunk = 2048
            count = 0

            # open up a wav
            wf = wave.open('noise/'+file, 'rb')
            CHANNELS = wf.getnchannels()
            RATE = wf.getframerate()
            swidth = wf.getsampwidth()

            #write a new file with 1 sec of sample.
            def writeSound(start,cnt):
                wf1= wave.open('noise/sample/'+file.replace(".wav","")+'_test'+str(cnt)+'.wav','wb')
                wf1.setnchannels(wf.getnchannels())
                wf1.setframerate(RATE)
                wf1.setsampwidth(wf.getsampwidth())
                
                #Shift to start position and write 1 sec data
                wf.setpos(start)
                data1 = wf.readframes(RATE)
                wf1.writeframes(data1)
                wf1.close()
             
            # use a Blackman window
            window = np.blackman(chunk)
            # open stream
            p = pyaudio.PyAudio()
            stream = p.open(format =
                            p.get_format_from_width(swidth),
                            channels = CHANNELS,
                            rate = RATE,
                            output = True)

            # read some data
            data = wf.readframes(chunk)
            # play stream and find the frequency of each chunk
            while (len(data) == chunk*swidth):
                # write data out to the audio stream
                stream.write(data)
                # unpack the data and times by the hamming window
                indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                                     data))*window
                # Take the fft and square each value
                fftData=abs(np.fft.rfft(indata))**2
                # find the maximum
                which = fftData[1:].argmax() + 1
                # use quadratic interpolation around the max
                if which != len(fftData)-1:
                    y0,y1,y2 = np.log(fftData[which-1:which+2:])
                    x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                    # find the frequency and output it
                    thefreq = (which+x1)*RATE/chunk
                    #When low audio/glitches
                    if(math.isnan(thefreq) or thefreq<0):
                        thefreq=0
                    print ("The freq is %f Hz." % (thefreq))
                    
                else:
                    thefreq = which*RATE/chunk
                    print ("The freq is %f Hz." % (thefreq))
                #"Gunshot" Signature test goes here. Currently, we are identifying it with an unusual difference in freq. 
                # As planned we shall replace with complete signature by next week 
                if(thefreq> 500 ):
                    writeSound(wf.tell(),count)
                    count+=1
                # read some more data
                data = wf.readframes(chunk)
            if data:
                stream.write(data)
            #Close necessary files 
            stream.close()
            p.terminate()

