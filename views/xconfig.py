import os
import wx
from shared.cnx import Cnx


class XConfig(wx.Panel):

    __layout: wx.BoxSizer
    __cnx: Cnx
    __txt_conn: wx.FilePickerCtrl
    __update_status_fn: wx.StaticText
    __lbl_name: wx.StaticText

    def __init__(self, cnx=None, update_status=any, *args, **kw):
        super().__init__(*args, **kw)

        self.__cnx = cnx
        self.__update_status_fn = update_status

        self.__layout = wx.BoxSizer(wx.VERTICAL)

        self.connection_name_level()
        self.new_connection()

        self.SetSizer(self.__layout)

    def self_add(self, item, *args):
        self.__layout.Add(item, flag=wx.EXPAND | wx.ALL, border=10, *args)

    def connection_name_level(self,) -> None:
        layout = wx.BoxSizer(wx.HORIZONTAL)
        self.conf_status_cnx()
        self.__lbl_name = wx.StaticText(self, label=self.conf_status_cnx(),
                                        style=wx.ALIGN_LEFT | wx.ST_ELLIPSIZE_END)
        layout.Add(self.__lbl_name, proportion=1, flag=wx.EXPAND)
        self.self_add(layout)

    def new_connection(self,):
        layout = wx.BoxSizer(wx.VERTICAL)
        layout_ctrl = wx.BoxSizer(wx.HORIZONTAL)

        self.__txt_conn = wx.FilePickerCtrl(self,)
        btn_search = wx.Button(self, label="connect")
        btn_create = wx.Button(self, label="create")

        self.Bind(wx.EVT_BUTTON,
                  handler=lambda _: self.create_db_file(), source=btn_create)
        self.Bind(wx.EVT_BUTTON, self.set_cnx, btn_search)

        layout_ctrl.AddMany(
            [(btn_search, 0, wx.LEFT | wx.RIGHT, 10), (btn_create, 0, wx.LEFT | wx.RIGHT, 10)])

        layout.AddMany([(self.__txt_conn, 0,
                         wx.EXPAND | wx.ALL, 10), (layout_ctrl, 0, wx.EXPAND | wx.ALL, 10)])

        self.self_add(layout)

    def create_db_file(self, ):
        try:
            file_path = wx.SaveFileSelector("sqlite database", "db", "db")
            if (os.path.exists(file_path)):
                raise Exception("file already exists")
            with open(file_path, "+a"):
                pass
            self.__update_status_fn("DB file created")
        except Exception as e:
            self.__update_status_fn(e.__str__())

    def set_cnx(self, _) -> None:
        file_path = self.__txt_conn.GetPath()
        self.__lbl_name.SetLabel(self.conf_status_cnx())
        self.__cnx.setCnx(file_path)

    def conf_status_cnx(self,):
        ini_status = "No connected"
        if self.__cnx and self.__cnx.cnx_str():
            ini_status = f"Current connection: {self.__cnx.cnx_str()}"
        self.__update_status_fn(ini_status)
        return ini_status