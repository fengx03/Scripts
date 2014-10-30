"""Downsample a JPG file

   - Xue Feng 06/2013

"""
import sys
import os
from Tkinter import *
import tkFileDialog, tkMessageBox
from PIL import Image

class Resize(Frame):

    def create_widgets(self, master):
        Label(master, text='Ratio').grid(row=0, sticky=W)
        self.e1 = Entry(master)
        self.e1.grid(row=0, column=1)
        self.e1.insert(END, '50')
        Label(master, text='Percent').grid(row=0, column=2, sticky=W)
        resizefile = Button(master, text='Resize file',
                            command=self.resize_file)
        resizefile.grid(row=1)
        resizefolder = Button(master, text='Resize folder',
                              command=self.resize_folder)
        resizefolder.grid(row=1, column=1)
        quitprogram = Button(master, text='QUIT', command=self.quit)
        quitprogram.grid(row=1, column=2)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.create_widgets(master)
        self.file_opt = options = {}
        options['filetypes'] = [('all files', '.*'), ('image files', '.JPG')]
        options['initialdir'] = '.'
        options['parent'] = root
        options['title'] = 'Select an image'
        self.folder_opt = options = {}
        options['initialdir'] = '.'
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'Select a folder'

    def validate_entry(self):
        """Validates the entry input."""
        
        try:
            ratio = int(self.e1.get())
        except ValueError:
            tkMessageBox.showwarning('Invalid input',
                                     'Please enter a valid number!')
            return False
        if ratio > 100 or ratio <= 0:
            tkMessageBox.showwarning('Invalid input',
                                     'Please enter a number between 0 and 100')
            return False
        self.resizeratio = int(self.e1.get())
        return True
                    

    def resize_file(self, imagefile=None, resizedfolder=None):
        """Resize the selected file."""

        if not self.validate_entry():
            return
        if imagefile is None:
            filename = tkFileDialog.askopenfilename(**self.file_opt)
        else:
            filename = imagefile
        if filename:
            try:
                im = Image.open(filename)
            except IOError:
                tkMessageBox.showwarning('IO Error',
                                         'Cannot open the image file')
                return
            originalsize = im.size
            newsize = tuple(x*self.resizeratio/100 for x in originalsize)
            im = im.resize(newsize, Image.ANTIALIAS)
            namelist = os.path.basename(filename).split('.')
            newname = (namelist[0] + '_' + str(self.resizeratio)
                       + '%.' + namelist[1])
            if resizedfolder is None:
                outfile = os.path.join(os.path.dirname(filename), newname)
            else:
                outfile = os.path.join(resizedfolder, newname)
            if os.path.exists(outfile):
                os.remove(outfile)
            try:
                im.save(outfile)
            except KeyError:
                tkMessageBox.showwarning('Error',
                                         'Unknown file extension')
        if resizedfolder is None:
            tkMessageBox.showinfo('Finished job',
                                  'Finished resizing the image')

    def resize_folder(self):
        """Resize the selected folder."""

        if not self.validate_entry():
            return
        foldername = tkFileDialog.askdirectory(**self.folder_opt)
        for root, dirs, files in os.walk(foldername):
            dirlist = root.split('\\')
            # do not resize the folder under resized and raw
            if dirlist[-1] not in ('resized', 'raw'):
                resizedfolder = '%s/resized' % root
                try:
                    os.mkdir(resizedfolder)
                except OSError:
                    # if compressed folder is already present, use it
                    pass
                for imagefile in files:
                    namelist = imagefile.split('.')
                    if namelist[1] in ('jpg', 'JPG'):
                        self.resize_file(os.path.join(root, imagefile),
                                         resizedfolder)        
        if foldername:
            tkMessageBox.showinfo('Finished job',
                                  'Finished resizing the folder %s'
                                  % foldername)

# implementation
root = Tk()
app = Resize(master=root)
app.mainloop()
root.destroy()
