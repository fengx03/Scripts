"""Organize the photo folder with both JPG and NEF file

   - Xue Feng 06/2013
   
"""
import sys
import os
import Tkinter, tkFileDialog, tkMessageBox

class PhotoOrganize:
    
    def select_folder(self):
        """Returns the selected folder name."""

        root = Tkinter.Tk()
        root.withdraw()
        diroption = {}
        diroption['initialdir'] = '.'
        diroption['mustexist'] = False
        diroption['parent'] = root
        diroption['title'] = 'Select a directory to organize'
        return tkFileDialog.askdirectory(**diroption)
        root.destroy()

    def organize_folder(self, folder):
        """Organize the given folder.

        For any NEF file, if there is no corresponding JPG file, it will be removed.
        Otherwise it will be moved to a separate folder named 'raw'.
        """

        # checking whether folder exist
        if not os.path.exists(folder):
            sys.exit()

        # splitting name and extension
        photo_to_keep = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                name = file.split('.')
                if name[1] in ('jpg', 'JPG'):
                    photo_to_keep.append(name[0])
        for root, dirs, files in os.walk(folder):
            for file in files:
                name = file.split('.')
                if name[1] in ('nef', 'NEF'):
                    if name[0] in photo_to_keep:
                        # if we are under raw folder, do nothing
                        if os.pathname.basename != 'raw':
                            rawfolder = '%s/raw' % root
                            try:
                                os.mkdir(rawfolder)
                            except OSError:
                                # if raw folder is already present, use it
                                pass
                            if os.path.exists(os.path.join(rawfolder, file)):
                                os.remove(os.path.join(root, file))
                            else:
                                os.rename(os.path.join(root, file),
                                          os.path.join(rawfolder, file))
                    else:
                        os.remove(os.path.join(root, file))

# organize the folder
app = PhotoOrganize()
dirname = app.select_folder()
app.organize_folder(dirname)
tkMessageBox.showinfo('Finished job',
                      'Finished organizing the folder %s' % dirname)
