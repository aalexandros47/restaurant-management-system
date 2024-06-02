import mysql.connector

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234", 
            database="RestaurantDB",
            port = 3306
        )
        self.cursor = self.conn.cursor()
        self.reset_table_reservations()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()
        
    def reset_table_reservations(self):
        self.execute_query("UPDATE tables SET is_reserved = FALSE")
    
db = Database()
