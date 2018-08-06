import wx

class MyForm(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial", size=(500,500))

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)

        SAVE_FILE_ID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.saveFile, id=SAVE_FILE_ID)

        LOAD_FILE_ID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.loadFile, id=LOAD_FILE_ID)

        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('O'), LOAD_FILE_ID ),
                                         (wx.ACCEL_CTRL,  ord('S'), SAVE_FILE_ID )]
                                        )
        self.SetAcceleratorTable(accel_tbl)

    #----------------------------------------------------------------------
    def loadFile(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", 
                                       "Python files (*.py)|*.py", 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        openFileDialog.GetPath()
        openFileDialog.Destroy()

    #----------------------------------------------------------------------
    def saveFile(self, event):
        saveFileDialog = wx.FileDialog(self, "Save As", "", "", 
                                       "Python files (*.py)|*.py", 
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        saveFileDialog.ShowModal()
        saveFileDialog.GetPath()
        saveFileDialog.Destroy()

# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()

