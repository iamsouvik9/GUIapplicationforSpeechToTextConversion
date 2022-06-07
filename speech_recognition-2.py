# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 09:23:46 2022

@author: SOUVIK
"""

from tkinter import *
from tkinter import filedialog
import speech_recognition as sr
import moviepy.editor
from scipy.io import wavfile
import numpy as np

import soundfile as sf
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer


class MyMenuDemo:
    def __init__(self,root):
        
        #Frame 1
        
        self.f1=Frame(root,width=800,height=100,bg='aquamarine')
        self.f1.propagate(0)
        self.f1.pack()
        
        self.lbl1=Label(self.f1,text="Upload Audio file:").place(x=20,y=35)
        self.b1=Button(self.f1,text="Upload",bg='gold',fg='black',command=self.open_file).place(x=300,y=35)
        
        
        #Frame 2
        self.f2=Frame(root,width=800,height=650,bg='beige')
        self.f2.propagate(0)
        self.f2.pack()
        
        self.lbl2=Label(self.f2,text="The Transcribed text is:").place(x=20,y=70)
        
    
    def open_file(self):
        self.filename=filedialog.askopenfilename(parent=root,title='Select a file',filetypes=(("Python","*.py"),("All files","*.*")))
        if self.filename != None:
            file1=self.filename
            ind=file1.rfind('/')
            name=file1[ind:]
            self.lb1=Label(self.f1,text='The choosen file is '+name).place(x=300,y=75)
            self.b2=Button(self.f1,text='Transcribe',bg='gold',command=self.click).place(x=580,y=35)
            
            
    
    def click(self):
        #The videofile that was uploaded by the user
        file=self.filename
        #Converting the video to digital audio file .wav 
        video=moviepy.editor.VideoFileClip(file)
        audio=video.audio
        audio.write_audiofile("video_audio.wav")
        
        """Loading the converted audio file"""
        file1="video_audio.wav"
        data=wavfile.read(file1)
        framerate=data[0]
        sounddata=data[1]
        time=np.arange(0,len(sounddata))/framerate
        #print('Sample Rate: ',framerate,'Hz')
        #print('Total Time: ',(len(sounddata)/framerate),'s')
        
        """Importing the wav2vec2 pretrained model"""
        tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
        model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")   
        
        """
        The Wav2Vec2 pretrained model is trained at a sample rate of 16000kHz, so the converted audio file is 
        resampled to the sample rate of 16000kHz.
        Loading the audio file using the librosa library and mentioning my audio clip size is 16000 Hz. 
        It converts the audio clip into an array and is stored into the ‘audio’ variable.
        """
        audio,samplerate=librosa.load(file1,sr=16000)
        
        
        """
        The next step is taking the input values, passing the audio (array) into 
        tokenizer and we want our tensors in PyTorch format instead of Python integers. 
        return_tensors = “pt” which is nothing more than PyTorch format
        """
        
        input_values=tokenizer(audio,return_tensors='pt').input_values
        
        """ Storing logits (non-normalized prediction values)"""
        
        logits=model(input_values).logits
        
        """Passing the logit values to softmax to get the predicted values"""
        predicted_ids=torch.argmax(logits,dim=-1)
        
        
        
        transcription=tokenizer.batch_decode(predicted_ids)[0]
        
        m=Message(self.f2,text=transcription,width=700,font=('Roman',13,'bold italic'),fg='dark goldenrod').place(x=10,y=150)
        
        
root=Tk()
root.title('Speech to Text Translator')
obj=MyMenuDemo(root)
root.geometry('800x800')
root.mainloop()