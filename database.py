import datetime
import os
import sqlite3
from enum import Enum

from submodule.Xu3.utils import getLogger


class DataBase:
    class SortType(Enum):
        A2Z = "ASC"
        Z2A = "DESC "

    def __init__(self, db_name, folder="data",
                 logger_dir="database", logger_name=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")):
        """
        NULL	值是一個 NULL 值。
        INTEGER	值是一個帶符號的整數，根據值的大小存儲在 1、2、3、4、6 或 8 字節中。
        REAL	值是一個浮點值，存儲為 8 字節的 IEEE 浮點數字。
        TEXT	值是一個文本字符串，使用數據庫編碼（UTF-8、UTF-16BE 或 UTF-16LE）存儲。
        BLOB	值是一個 blob 數據，完全根據它的輸入存儲。二進位大型物件，在資料庫管理系統中，將二進位資料儲存為一個單一個體的集合。
                Blob 通常是影像、聲音或多媒體檔案。
        SQLite 沒有單獨的 Boolean 存儲類。相反，布爾值被存儲為整數 0（false）和 1（true）。

        SQLite 沒有一個單獨的用於存儲日期和/或時間的存儲類，但 SQLite 能夠把日期和時間存儲為 TEXT、REAL 或 INTEGER 值。
        TEXT	格式為 "YYYY-MM-DD HH:MM:SS.SSS" 的日期。
        REAL	從公元前 4714 年 11 月 24 日格林尼治時間的正午開始算起的天數。
        INTEGER	從 1970-01-01 00:00:00 UTC 算起的秒數。
        """
        if not os.path.exists(folder):
            os.makedirs(folder)

        path = os.path.join(folder, f"{db_name}.db")
        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()
        self.table_name = None
        self.primary_key = []

        self.logger_dir = logger_dir
        self.logger_name = logger_name
        self.extra = {"className": self.__class__.__name__}
        self.logger = getLogger(logger_name=self.logger_name,
                                to_file=True,
                                time_file=False,
                                file_dir=self.logger_dir,
                                instance=True)

    def __del__(self):
        self.close(auto_commit=True)

    @staticmethod
    def sqlAnd(*sql_querys):
        return " AND ".join(sql_querys)

    @staticmethod
    def sqlOr(*sql_querys):
        return " OR ".join(sql_querys)

    @staticmethod
    def sqlGt(key, value):
        return f"{key} > {value}"

    @staticmethod
    def sqlGe(key, value):
        return f"{key} >= {value}"

    @staticmethod
    def sqlEq(key, value):
        return f"{key} = {value}"

    @staticmethod
    def sqlNe(key, value):
        return f"{key} != {value}"

    @staticmethod
    def sqlLe(key, value):
        return f"{key} <= {value}"

    @staticmethod
    def sqlLt(key, value):
        return f"{key} < {value}"

    def execute(self, sql, commit=False):
        result = self.cursor.execute(sql)

        if commit:
            self.commit()

        return result

    # region Create
    def getTable(self, table_name, table_definition):
        """
        保存 self.table_name 方便後續的使用，若該表格不存在，則建立表格

        :param table_name: 表格名稱
        :param table_definition: 表格定義
        :return:
        """
        self.table_name = table_name
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} ({table_definition});""")
        self.commit()

    def add(self, table_name=None, values: list = None, primary_column: str = ""):
        if values is None or len(values) == 0:
            return

        if primary_column != "":
            adding_values = self.additionFilter(primary_column=primary_column, values=values)
        else:
            adding_values = values

        n_column = len(adding_values[0])
        default_values = "?"

        if n_column == 0:
            return
        else:
            for _ in range(n_column - 1):
                default_values += ", ?"

        if table_name is None:
            table_name = self.table_name

        sql = f"INSERT OR IGNORE INTO {table_name} VALUES ({default_values});"
        # self.logger.info(f"sql: {sql} | {values}", extra=self.extra)
        self.cursor.executemany(sql, adding_values)

    def additionFilter(self, primary_column: str = "*", values: list = None):
        # 取得原有 primary_key，過濾已添加數據，避免重複存取
        if len(self.primary_key) == 0:
            result = self.select(columns=[primary_column])

            if result is not None:
                # 檢查返回值是否為空
                res = result.fetchone()
                # self.logger.info(f"res: {res}")
                while res is not None:
                    # self.logger.debug(f"res: {res}")
                    self.primary_key.append(res[0])
                    res = result.fetchone()
            else:
                self.logger.error("result is None.", extra=self.extra)

        if len(self.primary_key) != 0:
            filtered_values = []

            for value in values:
                primary_key = value[0]

                if primary_key not in self.primary_key:
                    # 隨著數據增加，更新 primary_key
                    self.primary_key.append(primary_key)

                    # 保留新的數據
                    filtered_values.append(value)
        else:
            filtered_values = values

        return filtered_values

    # endregion

    # region Read
    @staticmethod
    def formatColumns(columns: list = None):
        if columns is None or len(columns) == 0:
            columns_name = "*"
        elif len(columns) == 1:
            # ['*'] 也會被歸到這裡
            columns_name = columns[0]
        else:
            columns_name = ",".join(columns)

        return columns_name

    def select(self, table_name: str = None, columns: list = None, where: str = None,
               sort_by: str = None, sort_type: SortType = SortType.A2Z,
               limit: int = None, offset: int = 0):
        """
        將 table_name 結果按 column_name [ 升序 | 降序 ] 排序
        SELECT *
        FROM table_name
        WHERE [ conditions1 AND conditions2 ]
        ORDER BY column_name [ASC | DESC];

        :param table_name: 表格名稱
        :param columns: 欄位名稱
        :param where: 篩選條件
        :param sort_by: 排須依據哪些欄位
        :param sort_type: 升序(ASC) | 降序(DESC)
        :param limit: 限制從表格中提取的行數
        :param offset: 從第幾筆數據開始呈現(從 0 開始數)
        :return:
        """
        columns_name = self.formatColumns(columns=columns)

        if table_name is None:
            table_name = self.table_name

        sql = f"""SELECT {columns_name} FROM {table_name}"""

        if where is not None:
            # 不要預設為 AND，這樣會限制了彈性
            # where_condition = " AND ".join(where)
            sql += f" WHERE {where}"

        if sort_by is not None:
            sql += f" ORDER BY {sort_by} {sort_type.value}"

        if limit is not None:
            sql += f" LIMIT {limit} OFFSET {offset}"

        result = self.execute(sql)
        self.logger.debug(f"sql: {sql}, result: {result}", extra=self.extra)

        return result

    def head(self, table_name: str = None, columns: list = None, sort_by: str = None, n_data: int = 5, offset: int = 0):
        result = self.select(table_name=table_name,
                             columns=columns,
                             sort_by=sort_by,
                             sort_type=DataBase.SortType.A2Z,
                             limit=n_data,
                             offset=offset)

        result_list = list(result)
        return result_list

    def tail(self, table_name: str = None, columns: list = None, sort_by: str = None, n_data: int = 5, offset: int = 0):
        result = self.select(table_name=table_name,
                             columns=columns,
                             sort_by=sort_by,
                             sort_type=DataBase.SortType.Z2A,
                             limit=n_data,
                             offset=offset)

        result_list = list(result)
        result_list.reverse()

        return result_list

    def groupBy(self, table_name=None, columns=None,
                where=None, group_by=None,
                sort_by=None, sort_type: SortType = SortType.A2Z):
        """
        對相同的數據進行分組。
        在 SELECT 語句中，GROUP BY 子句放在 WHERE 子句之後，放在 ORDER BY 子句之前。
        SELECT column-list
        FROM table_name
        WHERE [ conditions ]
        GROUP BY column1, column2....columnN
        ORDER BY column1, column2....columnN

        參考網站: https://www.w3school.com.cn/sql/sql_groupby.asp
        :return:
        """
        if table_name is None:
            table_name = self.table_name

        columns_name = self.formatColumns(columns=columns)
        group_column = self.formatColumns(group_by)
        sql = f"SELECT {columns_name} FROM {table_name}"

        if where is not None:
            sql += f" WHERE {where}"

        sql += f" GROUP BY {group_column}"

        if sort_by is not None:
            sql += f" ORDER BY {sort_by} {sort_type.value}"

        result = self.cursor.execute(sql)
        self.commit()

        return result

    # endregion

    # region Update
    def update(self, table_name=None, new_content=None, condition=None, auto_commit=True):
        """
        UPDATE "表格"
        SET "欄位 1" = [值1], "欄位2" = [值2]
        WHERE "條件";

        :param table_name:
        :param new_content:
        :param condition:
        :param auto_commit:
        :return:
        """
        if table_name is None:
            table_name = self.table_name

        self.cursor.execute(f"""UPDATE {table_name} SET {new_content} WHERE {condition}""")

        if auto_commit:
            self.commit()

    # endregion

    # region Delete
    def delete(self, table_name=None, condition=None):
        """"""
        if table_name is None:
            table_name = self.table_name

        self.cursor.execute(f"""DELETE FROM {table_name} WHERE {condition};""")
        self.commit()

    def deleteTable(self, table_name=None):
        """
        删除表
        DROP TABLE table_name;

        :param table_name: 表格名稱
        :return:
        """
        if table_name is None:
            table_name = self.table_name

        self.cursor.execute(f"""DROP TABLE {table_name}""")
        self.commit()

    # endregion

    def commit(self):
        self.db.commit()

    def close(self, auto_commit=True):
        if auto_commit:
            self.commit()

        self.db.close()

    # region Database
    def getDatabaseInfo(self):
        sql = "SELECT * FROM sqlite_master;"
        result = self.execute(sql)

        return result.fetchall()

    def getAllTableName(self, ordered=True):
        """
        sqlite_master (
            type TEXT,          # 類型: table
            name TEXT,          # 表格名稱(Index or table name)
            tbl_name TEXT,      # Name of the table
            rootpage INTEGER,   # 欄位數量
            sql TEXT            # 表格建立時所使用的指令
        );

        :param ordered: 是否依名稱來排序
        :return: 所有資料表名稱
        """
        sql = "SELECT name FROM sqlite_master WHERE type='table'"

        if ordered:
            sql += " order by name"

        result = self.execute(sql)

        return result.fetchall()

    # endregion

    # region Table
    def isTableExists(self, table_name):
        """
        檢查該表格是否存在於此資料庫當中

        :param table_name: 表格名稱
        :return:
        """
        if table_name is None:
            table_name = self.table_name

        sql = f"""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'"""
        self.cursor.execute(sql)

        return self.cursor.fetchone()[0] == 1

    def isTableEmpty(self, table_name):
        sql = f"SELECT * FROM {table_name}"
        result = self.execute(sql=sql)

        return result.fetchone() is None

    def getTableInfo(self, table_name=None):
        if table_name is None:
            table_name = self.table_name

        result = self.cursor.execute(f"""PRAGMA table_info({table_name})""")
        return result.fetchall()

    # endregion

    def isDataExists(self, primary_key: str, key_value, table_name=None):
        if table_name is None:
            table_name = self.table_name

        sql = f"SELECT * FROM {table_name} WHERE {primary_key.upper()}={key_value}"
        result = self.execute(sql)
        entry = result.fetchone()

        return entry is not None


if __name__ == "__main__":
    class DataBaseTest(DataBase):
        def __init__(self):
            super().__init__(db_name="sqlite", folder="data", logger_dir="database", logger_name="DataBaseTest")

        def getTable(self, table_name, table_definition=None):
            table_definition = """ID INT PRIMARY KEY     NOT NULL,
                NAME           TEXT    NOT NULL,
                AGE            INT     NOT NULL,
                ADDRESS        CHAR(50),
                SALARY         REAL"""

            super().getTable(table_name=table_name, table_definition=table_definition)

        def getTableInfo(self, table_name=None):
            """
            (0, 'ID', 'INT', 1, None, 1)
            (1, 'NAME', 'TEXT', 1, None, 0)
            (2, 'AGE', 'INT', 1, None, 0)
            (3, 'ADDRESS', 'CHAR(50)', 0, None, 0)
            (4, 'SALARY', 'REAL', 0, None, 0)

            :param table_name: 表格名稱
            :return:
            """
            result = super().getTableInfo()

            for res in result:
                print(res)

        def add(self, table_name=None, values=None, primary_column=""):
            super().add(values=values, primary_column=primary_column)

        def display(self, table_name=None, columns=None,
                    sort_by=None, sort_type: DataBase.SortType = DataBase.SortType.A2Z,
                    limit: int = None, offset: int = 0):
            result = super().select(table_name=table_name, columns=columns,
                                    sort_by=sort_by, sort_type=sort_type,
                                    limit=limit, offset=offset)

            for res in result:
                print(res)

        def groupBy(self, table_name=None, columns=None,
                    where=None, group_by=None,
                    sort_by=None, sort_type: DataBase.SortType = DataBase.SortType.A2Z):
            result = super().groupBy(table_name=table_name, columns=columns,
                                     where=where, group_by=group_by,
                                     sort_by=sort_by, sort_type=sort_type)

            for res in result:
                print(res)

        def update(self, table_name=None, new_content=None, condition=None, auto_commit=True):
            """
            範例：UPDATE COMPANY set SALARY = 25000.00 where ID=1

            :param table_name: 表格名稱 COMPANY
            :param new_content: SALARY = 25000.00
            :param condition: ID=1
            :param auto_commit:
            :return:
            """
            super().update(new_content=new_content, condition=condition)

        def delete(self, table_name=None, condition=None):
            super().delete(condition=condition)


    db_test = DataBaseTest()
    db_test.getTable(table_name="Company")
    # db_test.getTableInfo()
    # db_test.add(values=[[0, "henry", 17, "address", 89]])
    # db_test.update(new_content="SALARY=103", condition="ID=0")
    db_test.display()
    db_test.close()
