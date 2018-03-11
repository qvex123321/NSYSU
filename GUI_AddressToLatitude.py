# -*- coding: utf-8 -*-

#from Tkinter import *   #for 2.7 version
from tkinter import *   #for 3.6 version
import geocoder
import time,os

class GUIDemo(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
 
    def createWidgets(self):
        self.lbl_adr=Label(self,text="Your address:")
        self.lbl_adr.grid(column=0,row=0)
        self.ent_adr=Entry(self,width=60)
        self.ent_adr.grid(column=0,row=1,columnspan=20)
        self.ent_adr.focus_set()
        self.lbl_lat=Label(self,text="Your latitude:")
        self.lbl_lat.grid(column=0,row=2)
        self.ent_lat=Entry(self,width=60,state='readonly')
        self.ent_lat.grid(column=0,row=3,columnspan=20)
        self.lbl_adr=Label(self,text="")
        self.lbl_adr.grid(column=2,row=4)
        self.btn_convert=Button(self,width=20,text="Convert")
        self.btn_convert.grid(column=15,row=2)
        self.btn_convert["command"]=self.btnConvert

    def btnConvert(self):
        try:
            if(self.ent_adr.get()!=""):
                self.ent_lat.configure(state='normal')
                g = geocoder.google(self.ent_adr.get())
                self.ent_lat.delete(0,200)
                lat="".join(str(g.latlng))
                self.ent_lat.insert(0,lat[1:-1])
                self.ent_lat.configure(state='readonly')
                self.lbl_adr["text"]=""
            else:
                self.lbl_adr["text"]="Please enter a legal address!"
        except:
            self.lbl_adr["text"]="Please enter a legal address!"

if __name__ == '__main__':

    root = Tk()
    root.title("AddressToLatitude")
    root.minsize(width=425, height=100)
    app = GUIDemo(master=root)
    app.mainloop()
