import psycopg2
import configparser

def drop_tables(cur, conn):
    # Define your drop tables SQL statements and execute them here
    pass

def create_tables(cur, conn):
    # Define your create tables SQL statements and execute them here
    pass

def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    # Modify the connection string to include the client_encoding parameter
    conn_str = "host={host} dbname={dbname} user={user} password={password} port={port} client_encoding=utf-8".format(
        host=config['CLUSTER']['HOST'],          # Use uppercase key 'HOST'
        dbname=config['CLUSTER']['DB_NAME'],     # Use uppercase key 'DB_NAME'
        user=config['CLUSTER']['DB_USER'],       # Use uppercase key 'DB_USER'
        password=config['CLUSTER']['DB_PASSWORD'],   # Use uppercase key 'DB_PASSWORD'
        port=config['CLUSTER']['DB_PORT']        # Use uppercase key 'DB_PORT'
    )

    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()
