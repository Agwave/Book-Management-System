import pymysql

class ConnetMysql:

    def __init__(self):
        self.conn = None

    def get_conn(self):
        try:
            if self.conn is None:
                self.conn = pymysql.connect(host="127.0.0.1",
                                            user="root",
                                            password="mysqlfgh.00",
                                            db="book_management_system",
                                            port=3306,
                                            charset="utf8")
        except Exception as e:
            print("Error: {}".format(e))

    def insert(self, sql, params=None):
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            if params is not None:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self.conn.commit()
            self.cut_conn()
            print("insert successfuly")
        except Exception as e:
            print("Error: {}".format(e))
            print("Error: {}".format(sql))

    def delete(self, sql, params=None):
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            if params is not None:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self.conn.commit()
            self.cut_conn()
            print("delete successfuly")
        except Exception as e:
            print("Error: {}".format(e))
            print("Error: {}".format(sql))

    def search(self, sql, params=None):
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            if params is not None:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            result = cursor.fetchall()
            self.cut_conn()
            return result
        except Exception as e:
            print("Error: {}".format(e))
            print("Error: {}".format(sql))
            return None

    def update(self, sql, params=None):
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            if params is not None:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self.conn.commit()
            self.cut_conn()
            print("update successfuly")
        except Exception as e:
            print("Error: {}".format(e))
            print("Error: {}".format(sql))

    def create_table(self, sql, params=None):
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            if params is not None:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self.cut_conn()
            print("create table successfully")
        except Exception as e:
            print("Error: {}".format(e))
            print("Error: {}".format(sql))

    def cut_conn(self):
        try:
            self.conn.close()
            self.conn = None
        except Exception as e:
            print("Error: {}".format(e))