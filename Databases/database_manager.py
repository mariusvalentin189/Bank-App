import mysql.connector

class DatabaseManager:
    def __init__(self):
        content = ""
        with open('Credentials/data.txt', 'r') as file:
            content = file.read()

        # Connect to the database
        self.__conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=content,
            database="users_database"
        )
        self.__cursor = self.__conn.cursor()

    def insert_user_data(self, user_data):
        self.__start_connection()

        # Create an INSERT query
        sql = "INSERT INTO users (user_id, first_name, last_name, pin, phone_number, email, user_password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (int(user_data[0]), str(user_data[1]), str(user_data[2]), str(user_data[3]), str(user_data[4]), str(user_data[5]), str(user_data[6]))

        # Execute the query
        self.__cursor.execute(sql, values)

        # Commit the transaction
        self.__conn.commit()

        self.__close_connection()

    def already_registered_user(self, email):
        self.__start_connection()
        self.__cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = self.__cursor.fetchall()
        self.__close_connection()

        return len(user_data) > 0

    def check_user_data(self, email, password):
        self.__start_connection()
        self.__cursor.execute("SELECT user_password FROM users WHERE email = %s", (email,))
        found_user = self.__cursor.fetchone()
        print(found_user)

        self.__close_connection()
    
    def __close_connection(self):
        # Close connection
        self.__cursor.close()
        self.__conn.close()

    def __start_connection(self):
        # Start connection
        self.__conn._open_connection()
        self.__cursor = self.__conn.cursor()

        