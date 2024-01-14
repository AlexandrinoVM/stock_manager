import mysql.connector


class banco():
    
    connection = mysql.connector.connect(
            #you have to put the name of the host
            host = 'localhost',
            #here you have to put the user
            user = 'root',
            #if the databsae have password you should put here the password
            password = '',
            #this is the name of the database data gonna be conected(preferably not change)
            database = 'estoque',
        )
    @staticmethod
    def check(cursor):

        #create a table in the database if arlready not exists
        cursor.execute('CREATE TABLE IF NOT EXISTS produtos( id int primary key not null auto_increment, produto varchar(40),preco int,quantidade int);')

    
    cursor = connection.cursor()
