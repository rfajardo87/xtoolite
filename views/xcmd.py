import wx
import wx.grid
from shared.cnx import Cnx


class XCmd(wx.Panel):
    __cnx: Cnx | None = None
    __txt_cmd: wx.TextCtrl | None = None
    __grd_rslt: wx.grid.Grid | None = None
    __update_status: any

    def __init__(self, cnx, update_status=any, *args, **kw):
        super().__init__(*args, **kw)

        self.__cnx = cnx
        self.__update_status = update_status
        layout = wx.BoxSizer(wx.VERTICAL)

        self.__txt_cmd = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        btn_run = wx.Button(self, label="Run")
        btn_run.SetToolTip("cmd + R")
        self.__grd_rslt = wx.grid.Grid(self,)
        self.__grd_rslt.CreateGrid(0, 0)

        layout.Add(self.__txt_cmd, proportion=1, flag=wx.EXPAND)
        layout.Add(btn_run, proportion=0,
                   flag=wx.ALIGN_LEFT | wx.ALL, border=10)
        layout.Add(self.__grd_rslt, proportion=2, flag=wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.query_data, btn_run)

        shortcut_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.query_data, id=shortcut_id)
        accel_tbl = wx.AcceleratorTable(
            [(wx.ACCEL_CMD, ord('R'), shortcut_id)])
        self.SetAcceleratorTable(accel_tbl)
        self.SetSizer(layout)

    def query_data(self, _) -> None:
        try:
            cmd = self.__txt_cmd.GetValue()
            rslt, hdrs = self.__cnx.runQuery(cmd)
            rslt_counter = len(rslt)
            self.update_grid(len(hdrs), rslt_counter)

            for i, h in enumerate(hdrs):
                self.__grd_rslt.SetColLabelValue(i, h)

            for i, row in enumerate(rslt):
                for j, cell in enumerate(row):
                    self.__grd_rslt.SetCellValue(i, j, f'{cell}')
            self.__update_status(f"OK query\t {rslt_counter} records")
        except Exception as e:
            self.__update_status(f'{e.__str__()}')

    def update_grid(self, ncols, nrows) -> None:
        col_num = self.__grd_rslt.GetNumberCols()
        row_num = self.__grd_rslt.GetNumberRows()
        if (col_num > 0):
            self.__grd_rslt.DeleteCols(0, col_num)
        if (row_num > 0):
            self.__grd_rslt.DeleteRows(0, row_num)
        self.__grd_rslt.AppendCols(ncols)
        self.__grd_rslt.AppendRows(nrows)
