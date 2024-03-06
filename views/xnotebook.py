import wx
from views.xconfig import XConfig
from views.xcmd import XCmd
from shared.cnx import Cnx


class XNotebook(wx.Notebook):

    __cnx: Cnx

    def __init__(self, update_status, *args, **kw):
        super().__init__(*args, **kw)

        self.__cnx = Cnx(update_status=update_status)

        tab_cmd = XCmd(self.__cnx, parent=self, update_status=update_status)
        tab_cnf = XConfig(parent=self, cnx=self.__cnx,
                          update_status=update_status)

        self.AddPage(tab_cmd, "SQL")
        self.AddPage(tab_cnf, "Configuración")
