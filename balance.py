import pymysql

from config import host,user, password, bdname

class Balance:



    def findclient(self,numbercard):
        client_id = ""
        try:
            connection_db = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=bdname,
                cursorclass=pymysql.cursors.DictCursor
            )
            print('connection successful')

            try:
                cursor = connection_db.cursor()
                print('cuesor successful')
                qry = "SELECT cards.client_id FROM cards WHERE cards.card_id = '"+numbercard+"';"
                try:
                    cursor.execute(qry)
                    row = cursor.fetchone()
                    client_id = row['client_id']
                except Exception as ex:
                    print('query error')
                    print(ex)
            except Exception as ex:
                print('cursor error')
                print(ex)

        except Exception as ex:
            print('connection not ok')
            print(ex)
        finally:
            connection_db.close()
        return client_id

    def get_balance(self,client_str):
        balance_num = 0
        try:
            connection_db = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=bdname,
                cursorclass=pymysql.cursors.DictCursor
            )
            print('connection successful')

            try:
                cursor = connection_db.cursor()
                print('cuesor successful')
                qry = "SELECT balances.amount FROM balances WHERE balances.client_id = '"+client_str+"';"
                print(qry)
                try:
                    cursor.execute(qry)
                    row = cursor.fetchone()
                    balance_num = row['amount']
                except Exception as ex:
                    print('query error')
                    print(ex)
            except Exception as ex:
                print('cursor error')
                print(ex)

        except Exception as ex:
            print('connection not ok')
            print(ex)
        finally:
            connection_db.close()
        return balance_num
