#!/usr/bin/env python3

'''
Python script for mfcc generation 
'''
	
#import pyaudio
import wave
import numpy as np
import os
import math
import MelBank
from scipy.fftpack import dct

np.set_printoptions(threshold=np.nan)

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
			m=MelBank.MelBank()

			 
			# use a Blackman window
			window = np.blackman(chunk)

			data = wf.readframes(chunk)
			# play stream and find the frequency of each chunk
			while (len(data) == chunk*swidth):
				# unpack the data and times by the hamming window
				indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),data))*window

				# Take the fft and square each value
				fftData=abs(np.fft.rfft(indata))**2
				#print(fftData)
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

				fbank= m.computeBank(len(fftData),RATE)

				energy = np.sum(pspec,1) # this stores the total energy in each frame
				energy = np.where(energy == 0,numpy.finfo(float).eps,energy) 
				feat = np.dot(fftData,fbank.T) # compute the filterbank energies
				feat = np.where(feat == 0,np.finfo(float).eps,feat)
				feat = np.log(feat)
				
				feat = dct(feat, type=2, axis=1, norm='ortho')[:,:26]
				
				feat = m.lifter(feat,22)
				print(feat)
				# read some more data
				data = wf.readframes(chunk)


