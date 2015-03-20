#!/usr/bin/env python3

'''
Class for generating MelBank Objects
'''

from numpy import *
from math import *

class MelBank:
	#The number of mfcc features required can be given here
	def __init__(self,melNo=26,minF=0,maxF=8000):
		self.melNo=melNo
		self.minF=minF
		self.maxF=maxF
		self.mFreqRange=[]
		self.freqRange=[]
		self.fftbin=[]
		self.mWidth=(self.melScale(maxF)-self.melScale(minF))/(self.melNo+1)
		
	
	def melScale(self,freq):
		return (1125*log(1+freq/700)) 

	def freqScale(self,mfreq):
		return 700*(exp(mfreq/1125)-1)
	
	def computeBank(self,fftsize,srate):
		i=self.melScale(self.minF)
		while(i<=self.melScale(self.maxF)):
			self.mFreqRange.append(i)
			self.freqRange.append(self.freqScale(i))
			self.fftbin.append(floor((fftsize+1)*self.freqScale(i)/srate))
			i=i+self.mWidth	

		fbin= asarray(self.fftbin)
		fbank = zeros([self.melNo,fftsize])
		for i in range(self.melNo):
			for j in range(int(fbin[i]),int(fbin[i+1])):
				fbank[i,j] = (j - fbin[i])/(fbin[i+1]-fbin[i])
			for j in range(int(fbin[i+1]),int(fbin[i+2])):
				fbank[i,j] = (fbin[i+2]-j)/(fbin[i+2]-fbin[i+1])
		return fbank

	def lifter(self,cepstra,L=22):
		if L > 0:
			nframes,ncoeff = numpy.shape(cepstra)
			n = numpy.arange(ncoeff)
			lift = 1+ (L/2)*numpy.sin(numpy.pi*n/L)
			return lift*cepstra
		else:
			return cepstra

	
