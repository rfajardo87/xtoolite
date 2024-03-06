import sqlite3 as sql
from os.path import exists
from os import makedirs


class Cnx:
    __cnxStr: str
    __update_status: any

    def __init__(self, cnxStr: str | None = None, update_status=any):
        self.__cnxStr = cnxStr
        self.__update_status = update_status
        # self.init_db()
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

    def runQuery(self, query: str) -> list[sql.Row]:
        try:
            cur = self.__cnx.cursor()
            cur.execute(query)
            all_data = cur.fetchall()
            header_columns = all_data[0].keys() if len(all_data) else []
            return all_data, header_columns
        except Exception as e:
            self.__update_status(e.__str__())

    def cnx_str(self) -> str:
        return self.__cnxStr

    def init_db(self,) -> None:
        try:
            if not exists("./db"):
                makedirs("./db")

            with open(self.__cnxStr, "+a"):
                pass
        except Exception as e:
            self.__update_status(e.__str__())
