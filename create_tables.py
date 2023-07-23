import psycopg2
import configparser


def drop_tables(cur, conn):
    """
    Drops all the tables in the Sparkify database.
    
    Args:
        cur: Cursor object to execute SQL statements.
        conn: Connection object to the database.
    """
    
    # Define the drop table SQL statements
    drop_table_queries = [
        "DROP TABLE IF EXISTS staging_events;",
        "DROP TABLE IF EXISTS staging_songs;",
        "DROP TABLE IF EXISTS songplays;",
        "DROP TABLE IF EXISTS users;",
        "DROP TABLE IF EXISTS songs;",
        "DROP TABLE IF EXISTS artists;",
        "DROP TABLE IF EXISTS time;"
    ]
    
    # Execute the drop table SQL statements
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates all the tables in the Sparkify database.
    
    Args:
        cur: Cursor object to execute SQL statements.
        conn: Connection object to the database.
    """
    
    # Define the create table SQL statements
    create_table_queries = [
        """
        CREATE TABLE IF NOT EXISTS staging_events (
            artist_name VARCHAR(255),
            auth VARCHAR(50),
            user_first_name VARCHAR(255),
            user_gender VARCHAR(1),
            item_in_session INT,
            user_last_name VARCHAR(255),
            song_length DOUBLE PRECISION,
            user_level VARCHAR(50),
            location VARCHAR(255),
            method VARCHAR(25),
            page VARCHAR(35),
            registration VARCHAR(50),
            session_id BIGINT,
            song_title VARCHAR(255),
            status INT,
            ts VARCHAR(50),
            user_agent TEXT,
            user_id VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS staging_songs (
            song_id VARCHAR(100),
            num_songs INTEGER,
            artist_id VARCHAR(100),
            artist_latitude DOUBLE PRECISION,
            artist_longitude DOUBLE PRECISION,
            artist_location VARCHAR(255),
            artist_name VARCHAR(255),
            title VARCHAR(255),
            duration DOUBLE PRECISION,
            year INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS songplays (
            songplay_id INT IDENTITY(0,1) PRIMARY KEY,
            start_time TIMESTAMP NOT NULL,
            user_id VARCHAR(50)NOT NULL,
            level VARCHAR(50),
            song_id VARCHAR(100),
            artist_id VARCHAR(100),
            session_id BIGINT,
            location VARCHAR(255),
            user_agent TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR PRIMARY KEY,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            gender CHAR(1),
            level VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS songs (
            song_id VARCHAR PRIMARY KEY,
            title VARCHAR,
            artist_id VARCHAR,
            year INT,
            duration FLOAT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS artists (
            artist_id VARCHAR(100) PRIMARY KEY,
            name VARCHAR(255),
            location VARCHAR(255),
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS time (
            start_time TIMESTAMP PRIMARY KEY,
            hour INT,
            day INT,
            week INT,
            month INT,
            year INT,
            weekday INT
        );
        """
    ]
    
    # Execute the create table SQL statements
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
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