import wx
from views.xmain import XMain

if __name__ == '__main__':
    app = wx.App(False)

    frame = XMain(None, wx.ID_ANY, "xtoolite", size=(800, 600))

    menu = wx.MenuBar()

    frame.SetMenuBar(menu)


    app.MainLoop()
