import mysql.connector as conn
class mysql_conecton:
    message = ""
    try:
        @staticmethod
        def Conect():
            connection = conn.connect(
                host='localhost',
                user = 'root',
                password = '',
                database = 'taxi_booking'
            )
            if connection.is_connected():
                mysql_conecton.message = "Connected"

                return connection
            connection.close()
    except Exception as e:
        print(e)