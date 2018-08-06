import wx
#import wxversion
#wxversion.select('3.0')
import os
# import wxExportTemplate

class Images():
    def __init__(self, *args, **kwds):
        title  = "Export Images"
        choice = ["PNG, 16bit, Grayscale", "PNG, 8bit, Grayscale", "TIFF, 16bit, Grayscale",
                   "TIFF, 8bit, Grayscale", "TIFF Stack, 16bit, Grayscale",
                   "TIFF Stack, 8bit, Grayscale", "NUMPY, 32bit, uint (npy)",
                   "NUMPY, 32bit, uint (npz)", "HDF, 64bit, int, 'stack'"]

        # super(Images, self).__init__(self, wx.ID_ANY, "")
        # wxExportTemplate.Template.__init__(self, wx.ID_ANY, "")

    def SpecifyDIR(self, event):  # wxGlade: TemplateExporter.<event_handler>
        ##
        dialog = wx.DirDialog(self, "Select Export Folder", self.u_info.files_path, wx.DD_DEFAULT_STYLE )
        try:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            dir = dialog.GetPath()
        except Exception:
            wx.LogError('Failed to open directory!')
            raise
        finally:
            dialog.Destroy()

        print('Filedir:    ', dir)
        print('Filename:   ', self.Filename.GetLineText() )
        print('Filetype:   ', self.Filetype,GetSelection() )
        print('Init ID:    ', self.StartID.GetValue() )
        print('Num Digits: ', self.NumDigits.GetValue() )
        # ExportImgSeg.images(self.u_info, export_path, filetype)
        return True

    def Cancel(self, event):  # wxGlade: TemplateExporter.<event_handler>
        self.Close()
        return False



class Ids(wxExportTemplate.Template):

    def __init__(self, *args, **kwds):
        title  = "Export Ids"
        choice = ["PNG, 16bit, Grayscale", "PNG, 8bit, Grayscale", "PNG, 8bit, Color",
                  "TIFF, 16bit, Grayscale", "TIFF, 8bit, Grayscale", "TIFF, 8bit, Color",
                  "TIFF Stack, 16bit, Grayscale", "TIFF Stack, 8bit, Grayscale", "TIFF Stack, 8bit, Color",
                  "NUMPY, 32bit, uint (npy)", "NUMPY, 32bit, uint (npz)",
                  "HDF, 64bit, int, 'stack'"]

        super().__init__(self, wx.ID_ANY, "")

