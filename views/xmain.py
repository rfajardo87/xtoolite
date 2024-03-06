import wx
from views.xnotebook import XNotebook
from views.xstatus import XStatus


class XMain(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        panel = wx.Panel(self)

        layout_main = wx.BoxSizer(wx.VERTICAL)

        xstatus = XStatus(self)
        xnotebook = XNotebook(
            parent=panel, update_status=xstatus.PushStatusText)

        layout_main.Add(xnotebook, proportion=1,
                        flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(layout_main)
        self.SetStatusBar(xstatus)

        self.Show()
