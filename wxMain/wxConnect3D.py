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
import itertools

sys.path.append("./Filesystem")
sys.path.append("./../Filesystem")
from Params import Params
from Merge3DSimple import Merge3DSimple
#from Merge3D_Smart import Merge3D_Smart

class wxConnect3D():

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------

    def Execute1_3DMerge(self, event):
        if not self.u_info.files_found:
            print('Dojo files are not validated.')
            print('Select Dojo files folder.')
            return False
        print('Create ID tables for 3D merge..')
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
        tmp1 = list(itertools.chain.from_iterable(MergeIDs))
        tmp2 = list(set(tmp1))
        if len(tmp1) != len(tmp2):
            print('Each ID can appear only once.')
            return False
        #
        if self.checkbox_1.GetValue():
            print('No Merge3D_Smart')
            # Merge3D_Smart.main(MergeIDs, self.u_info)
        else:
            merge = Merge3DSimple()
            merge.run(MergeIDs, self.u_info)

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

    def Clear1_3DMerge(self, event):  # wxGlade: MojoControlPanel.<event_handler>
        self.grid1.ClearGrid()

