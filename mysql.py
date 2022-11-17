import pymysql

from config import host,user, password, bdname

class Mysql:

    connection_db = None
    cursor = None

    def create_connectio_mysql_db(self):
        try:
            self.connection_db = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=bdname,
                cursorclass=pymysql.cursors.DictCursor
            )
            print('connection successful')
        except Exception as ex:
            print('connection not ok')
            print(ex)

    def create_cursor_mysql_db(self):
        try:
            self.cursor =  self.connection_db.cursor()
            print('cuesor successful')
        except Exception as ex:
            print('cursor error')
            print(ex)


    def close(self):
        self.cursor.close()
        self.connection_db.close()

