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

class wxExecutes():

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------

    def Execute3DDisconnector(self, event):
        if not self.UserInfo.mojo_files_found:
            print('Mojo files are not validated.')
            print('Select Mojo files folder.')
            return False
        print('Create ID tables for 3D disconnect...')

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
        Disconnect3D.main(DisconnectIDs, self.u_info)

    def Execute3DMerger(self, event):
        if not self.UserInfo.mojo_files_found:
            print('Mojo files are not validated.')
            print('Select Mojo files folder.')
            return False
        print('Create ID tables for 3D merge...')
        ncol = self.grid1.GetNumberCols()
        nrow = self.grid1.GetNumberRows()
        MergeIDs = []
        for col in range(ncol):
            TargetColVals = [self.grid1.GetCellValue(row, col).encode("UTF-8") for row in range(nrow)]
            TargetColVals = [i for i in TargetColVals if i is not '']
            TargetColVals = [int(i) for i in TargetColVals]
            if TargetColVals != []:
                MergeIDs.append(np.array(TargetColVals, dtype='uint32'))
        print(MergeIDs)

        #
        if MergeIDs == []:
            print('No ID is specified.')
            return False
        #
        tmp1 = list(chain.from_iterable(MergeIDs))
        tmp2 = list(set(tmp1))
        if len(tmp1) != len(tmp2):
            print('Each ID can appear only once.')
            return False
        #
        if self.checkbox_1.GetValue():
            Merge3D_Smart.main(MergeIDs, self.UserInfo)
        else:
            Merge3D_Simple.main(MergeIDs, self.UserInfo)

    #  ----------------------------------------------------------------------
    # I want to move the AppendRowsCols1 to wxDialog.py
    #  ----------------------------------------------------------------------

    def AppendRowsCols1(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.OnPopupOne1, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo1, id=self.popupID2)
        menu = wx.Menu()
        menu.Append(self.popupID1, "Add Row")
        menu.Append(self.popupID2, "Add Col")
        self.PopupMenu(menu)  ###
        menu.Destroy()


    def OnPopupOne1(self, event):
        self.grid1.AppendRows(1)


    def OnPopupTwo1(self, event):
        self.grid1.AppendCols(1)
        n = self.grid1.GetNumberCols()
        self.grid1.SetColLabelValue(n - 1, "Conn" + str(n))


    def Execute1_3DMerge(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        wxDialogs.Execute3DMerger(self, event)


    def Clear1_3DMerge(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        self.grid1.ClearGrid()

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

    def AppendRowsCols3(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        print("Event handler 'AppendRowsCols3' not implemented!")
        event.Skip()

    def Execute3_2Disconnect(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        print("Event handler 'Execute3_2Disconnect' not implemented!")
        event.Skip()

    def Clear3_2Disconnect(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        self.grid3.ClearGrid()

    def AppendRowsCols4(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        print("Event handler 'AppendRowsCols4' not implemented!")
        event.Skip()

    def Execute4_3DReplace(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        print("Event handler 'Execute4_3DReplace' not implemented!")
        event.Skip()

    def Clear4_3DReplace(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        self.grid4.ClearGrid()

    def AppendRowsCols5(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        print("Event handler 'AppendRowsCols5' not implemented!")
        event.Skip()

    def Execute5_2DReplace(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        print("Event handler 'Execute5_2DReplace' not implemented!")
        event.Skip()

    def Clear5_2DReplace(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        self.grid5.ClearGrid()



def AppendRowsCols1(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'AppendRowsCols1' not implemented!")
    event.Skip()


def Execute1_3DMerge(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'Execute1_3DMerge' not implemented!")
    event.Skip()


def Clear1_3DMerge(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'Clear1_3DMerge' not implemented!")
    event.Skip()


def AppendRowsCols2(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'AppendRowsCols2' not implemented!")
    event.Skip()


def Execute2_3Disconnect(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'Execute2_3Disconnect' not implemented!")
    event.Skip()


def Clear2_3Disconnect(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'Clear2_3Disconnect' not implemented!")
    event.Skip()


def AppendRowsCols3(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'AppendRowsCols3' not implemented!")
    event.Skip()


def Execute3_2Disconnect(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'Execute3_2Disconnect' not implemented!")
    event.Skip()


def Clear3_2Disconnect(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'Clear3_2Disconnect' not implemented!")
    event.Skip()


def AppendRowsCols4(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'AppendRowsCols4' not implemented!")
    event.Skip()


def Execute4_3DReplace(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'Execute4_3DReplace' not implemented!")
    event.Skip()


def Clear4_3DReplace(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'Clear4_3DReplace' not implemented!")
    event.Skip()


def AppendRowsCols5(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'AppendRowsCols5' not implemented!")
    event.Skip()


def Execute5_2DReplace(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'Execute5_2DReplace' not implemented!")
    event.Skip()


def Clear5_2DReplace(self, event):  # wxGlade: ControlPanel.<event_handler>
    print("Event handler 'Clear5_2DReplace' not implemented!")
    event.Skip()

