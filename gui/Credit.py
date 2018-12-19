
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
from os import path, pardir
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir          = path.join(main_dir, "icons")
icon_disabled_dir = path.join(icon_dir, "Disabled")
plugins_dir = path.join(main_dir, "plugins")
sys.path.append(plugins_dir)
sys.path.append(os.path.join(main_dir, "filesystem"))
sys.path.append(os.path.join(main_dir, "gui"))



class Credit():
    def Credit(self):
        #QMessageBox.setIcon(QMessageBox.Information)
        msg = QMessageBox(QMessageBox.Information, "About Dojo",
                          "<h1>Dojo standalone Ver1.0</h1><BR>"
                          "(C) 2018 Hidetoshi Urakubo in Ishii Lab<BR>"
                          "<a href=\"http://www.rhoana.org/dojo/\">Dojo Web Site</a><BR> "
                          "Powered by <a href=\"http://doc.qt.digia.com/4.5/stylesheet.html\">Qt</a><BR>"
                          )
        msg.setIconPixmap(QPixmap(path.join(icon_dir, "Mojo2_128.png")))
        exe = msg.exec_()



