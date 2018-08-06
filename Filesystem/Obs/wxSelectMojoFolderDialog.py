import wx
class wxDialogs(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        selectFileDialog = wx.DirDialog(self, "Select Mojo files folder", "",
                                       wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        selectFileDialog.ShowModal()
        dir = selectFileDialog.GetPath()
        selectFileDialog.Destroy()

    #----------------------------------------------------------------------
    def loadFile(self, event):
        openFileDialog = wx.DirDialog(self, "Select Mojo files folder", "", 
                                       wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        openFileDialog.ShowModal()
        openFileDialog.GetPath()
        openFileDialog.Destroy()

# (None, "Choose input directory", "",
#                     wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)


# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()

