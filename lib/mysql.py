import mysql.connector


class TMySql:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self._connect()
        self._getcursor()

    def _connect(self):
        self.cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)

    def _getcursor(self):
        self.cursor = self.cnx.cursor()

    def get(self, sql):
        self.cursor.execute(sql)
        output = self.cursor.fetchall()
        self.cnx.commit()
        return output

    def put(self, sql):
        self.cursor.execute(sql)
        self.cnx.commit()

    def __del__(self):
        self.cursor.close()
        self.cnx.close()
