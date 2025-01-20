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

    def get(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def put(self,sql):
        self.cursor.execute(sql)
        self.cnx.commit()

