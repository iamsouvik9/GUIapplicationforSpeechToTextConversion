from tkinter import *
from tkinter import filedialog
import speech_recognition as sr


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
        file=self.filename
        r=sr.Recognizer()
        with sr.AudioFile(file) as source:
            audio=r.record(source)
            tt=r.recognize_google(audio)
        
        m=Message(self.f2,text=tt,width=700,font=('Roman',13,'bold italic'),fg='dark goldenrod').place(x=10,y=150)
        
        
root=Tk()
root.title('Speech to Text Translator')
obj=MyMenuDemo(root)
root.geometry('800x800')
root.mainloop()
    
    
