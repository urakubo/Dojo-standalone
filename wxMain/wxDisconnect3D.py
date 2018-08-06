###
###
###

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import wx
import os
import os.path
import sys
import numpy as np

class wxDisconnect3D():

    # ----------------------------------------------------------------------

    def Execute2_3Disconnect(self, event):
        if not self.UserInfo.mojo_files_found:
            print('Dojo files have not been validated.')
            print('Select Dojo files folder.')
            return False
        print('Create ID tables for 3D disconnect..')

        ncol = self.grid2.GetNumberCols()
        nrow = self.grid2.GetNumberRows()
        DisconnectIDs = []
        for col in range(ncol):
            TargetColVals = [self.grid2.GetCellValue(row, col).encode("UTF-8") for row in range(nrow)]
            TargetColVals = [i for i in TargetColVals if i is not '']
            TargetColVals = [int(i) for i in TargetColVals]
            if TargetColVals != []:
                DisconnectIDs.append(np.array(TargetColVals, dtype='uint32'))
        print(DisconnectIDs)

        #
        if DisconnectIDs == []:
            print('No ID is specified.')
            return False
        #
        tmp1 = list(chain.from_iterable(DisconnectIDs))
        tmp2 = list(set(tmp1))
        if len(tmp1) != len(tmp2):
            print('Each ID can appear only once.')
            return False
        #
        Disconnect3D.main(DisconnectIDs, self.UserInfo)

        #  ----------------------------------------------------------------------
        # I want to move the AppendRowsCols2 to wxDialog.py
        #  ----------------------------------------------------------------------


    def AppendRowsCols2(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        if not hasattr(self, "popupID01"):
            self.popupID21 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.OnPopupOne21, id=self.popupID21)
        menu = wx.Menu()
        menu.Append(self.popupID21, "Add Row")
        self.PopupMenu(menu)  ###
        menu.Destroy()

    def OnPopupOne21(self, event):
        self.grid2.AppendRows(1)
        #  ----------------------------------------------------------------------

    def Execute2_3Disconnect(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        wxDialogs.Execute3DDisconnector(self, event)

    def Clear2_3Disconnect(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        self.grid2.ClearGrid()

