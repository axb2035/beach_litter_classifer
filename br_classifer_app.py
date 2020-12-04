# -*- coding: utf-8 -*-
"""
Beach image classifier.

This app allows you to load an directory and go through the images manually
classifing them as Litter (1) or Not Litter (0). once complete then a csv
file is created. 

The intention is to build a rubbish classifer that can run on a Raspberry Pi
or other hardware. 

@author: Andrew Buttery
"""
import os

import wx
import csv

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, 
                         title='Beach Litter manual classifer', 
                         size=(1190, 780))

        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
       
        self.btn_get_file = wx.Button(panel, label='Unclassified image directory')
        self.btn_get_file.Bind(wx.EVT_BUTTON, self.on_open_folder)
        
        self.btn_ignore = wx.Button(panel, label='Ignore')
        self.btn_ignore.Bind(wx.EVT_BUTTON, self.on_ignore)                
        
        self.btn_is_litter = wx.Button(panel, label='Litter')
        self.btn_is_litter.Bind(wx.EVT_BUTTON, self.on_litter)
        
        self.btn_is_not_litter = wx.Button(panel, label='Not Litter')
        self.btn_is_not_litter.Bind(wx.EVT_BUTTON, self.on_not_litter)
        
        self.btn_flip_image = wx.Button(panel, label='Flip image')
        self.btn_flip_image.Bind(wx.EVT_BUTTON, self.on_flip)

        self.btn_save_and_quit = wx.Button(panel, label='Save and Quit')
        self.btn_save_and_quit.Bind(wx.EVT_BUTTON, self.on_save_and_quit)
        
        my_sizer.Add(self.btn_get_file, 0, wx.ALL | wx.ALIGN_LEFT, 20)
        my_sizer.Add(self.btn_ignore, 0, wx.ALL | wx.ALIGN_RIGHT, 20)
        my_sizer.Add(self.btn_is_litter, 0, wx.ALL | wx.ALIGN_RIGHT, 20)
        my_sizer.Add(self.btn_is_not_litter, 0, wx.ALL | wx.ALIGN_RIGHT, 20)
        my_sizer.Add(self.btn_flip_image, 0, wx.ALL | wx.ALIGN_RIGHT, 20)
        my_sizer.Add(self.btn_save_and_quit, 0, wx.ALL | wx.ALIGN_RIGHT, 20)
        panel.SetSizer(my_sizer)
        
        self.disable_buttons()
        
        self.classifications = list()
        self.unclassified_files = list()
        self.unclassified_files_list = list()
        
        self.Show()


    def show_next_image(self, pop_image=True):
        if len(self.unclassified_files_list) > 1 :
            if pop_image:
                self.unclassified_files.pop(0)
                self.unclassified_files_list.pop(0)
                self.beach_image.Destroy()
            bitmap = wx.Bitmap(self.unclassified_files_list[0])
            scaled = bitmap.ConvertToImage().Rescale(1024, 576)
            bitmap = wx.Bitmap(scaled)
            self.beach_image = wx.StaticBitmap(self, -1, bitmap, (20, 100))
        else:
            self.unclassified_files.pop(0)
            self.unclassified_files_list.pop(0)
            self.disable_buttons()
            self.beach_image.Destroy()


    def disable_buttons(self):
        self.btn_ignore.Disable()
        self.btn_is_litter.Disable()
        self.btn_is_not_litter.Disable()
        self.btn_flip_image.Disable()


    def enable_buttons(self):
        self.btn_ignore.Enable()
        self.btn_is_litter.Enable()
        self.btn_is_not_litter.Enable()
        self.btn_flip_image.Enable()


    def on_open_folder(self, event):
        title = "Choose a directory:"
        dlg = wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.text_ctrl.SetValue(dlg.GetPath())
            # Get list of jpg files in dir and feed into list.            
            self.unclassified_files += [each for each in os.listdir(dlg.GetPath()) if each.endswith('.jpg')]
            for files in self.unclassified_files:
                self.unclassified_files_list.append(str(dlg.GetPath() + "/" + files))
            
            self.show_next_image(pop_image=False)
            self.enable_buttons()            

        dlg.Destroy()

    
    def on_flip(self, event):
        flipped = self.beach_image.GetBitmap().ConvertToImage()
        flipped = flipped.Mirror(horizontally=False)
        self.beach_image.SetBitmap(wx.Bitmap(flipped))

    
    def on_ignore(self, event):
        print("Ignoring image.")
        self.show_next_image()

    
    def on_litter(self, event):
        print("Classify as litter.")
        self.classifications.append([self.unclassified_files[0], 1])
        self.show_next_image()


    def on_not_litter(self, event):
        print("Classify as not litter.")
        self.classifications.append([self.unclassified_files[0], 0])
        self.show_next_image()

    
    def on_save_and_quit(self, event):
        print("Writing classificaiton .csv.")
        file = open('image_classification.csv', 'w+', newline ='') 
        with file:
            write = csv.writer(file) 
            write.writerows(self.classifications)
        self.Close()

        
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Raise()
    app.MainLoop()
    
