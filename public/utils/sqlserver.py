<<<<<<< HEAD
from django.db import connection


=======
from django.db import connection, ConnectionHandler

# ConnectionHandler().create_connection('default')
>>>>>>> master
class SqlServerObject:
    """数据库链接操作类"""
    def __init__(self):
        try:
            self._conn = connection
<<<<<<< HEAD
=======
            print(self._conn)
>>>>>>> master
            self._cursor = self._conn.cursor()
        except Exception as e:
            raise Exception('数据连接错误', e)

    # 查询字段
    def query_table_field_sql(self, sql):
        self._cursor.execute(sql)
        return [table_field for table_field in self._cursor]

    # 查询数据
    def query_data(self, sql):
        self._cursor.execute(sql)
        cols = self._cursor.description  # 获取列名
        column_list = []
        for column in cols:
            column_list.append(column[0])
        result = self._cursor.fetchall()  # fetchall 获取数据   list[tuple、tuple、tuple]
        return result, column_list

    # 插入数据
    def insert_data(self, sql):
        try:
            self._cursor.execute(sql)
        except Exception as e:
            # traceback.print_exc()
            self._conn.rollback()
            raise Exception(e)

    # 关闭数据库连接
    def close_db(self):
        self._cursor.close()
        # self._conn.close()
        print("关闭数据库游标")

    # 析构，关闭数据库连接
    def __del__(self):
        try:
            self.close_db()
        except Exception as e:
<<<<<<< HEAD
            print('关闭连接', e)
=======
            print('关闭连接', e)


>>>>>>> master
