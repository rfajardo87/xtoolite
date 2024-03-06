import sqlite3 as sql
from functools import reduce


class Cnx:
    __cnxStr: str
    __update_status: any

    def __init__(self, cnxStr: str | None = None, update_status=any):
        self.__cnxStr = cnxStr
        self.__update_status = update_status
        self.setCnx(cnxStr)

    def setCnx(self, cnxStr=None) -> None:
        try:
            if not cnxStr:
                raise Exception("No db selected")
            self.__cnxStr = cnxStr
            self.__cnx = sql.connect(self.__cnxStr)
            self.__cnx.row_factory = sql.Row
        except Exception as e:
            self.__update_status(e.__str__())

    def getCnx(self) -> sql.connect:
        return self.__cnx

    def runQuery(self, query: str, update_status=any) -> list[sql.Row]:
        try:
            cur = self.__cnx.cursor()
            cur.execute(query)
            all_data = cur.fetchall()
            row_num = self.is_dml(query, cur, len(all_data), update_status)
            header_columns = all_data[0].keys() if len(all_data) else []
            return all_data, header_columns, row_num
        except Exception as e:
            self.__update_status(e.__str__())

    def is_dml(self, query='', cur={}, lst=0, update_status=any):
        if reduce(lambda x, y: x or y.upper() in query.upper(), ["insert", "update", "delete", "create"], False):
            counter = cur.rowcount
            self.__cnx.commit()
            update_status(
                f'OK query\t {counter} {"rows"if counter >1 else "row"} affected')
            return counter if counter >= 0 else 0
        update_status(
            f'OK query\t {lst} {"rows"if lst >1 else "row"} selected')
        return lst

    def cnx_str(self) -> str:
        return self.__cnxStr
