import psycopg2

# NOTE: before running this program, you must create the database named below from
# the command-line (i.e. outside of Python or psql).
# E.g. for the values of the constants below, you'd type:
#     createdb -U postgres mydb1
# and give the password: wombat

PG_USER = "postgres"
PG_USER_PASS = "wombat"
PG_DATABASE = "mydb1"
PG_HOST_INFO = ""#" host=/tmp/" # use "" for OS X or Windows

# Connect to an existing database
conn = psycopg2.connect("dbname=" + PG_DATABASE + " user=" + PG_USER + " password=" + PG_USER_PASS + PG_HOST_INFO)
print("** Connected to database.")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table, but first removes it if it's there already
cur.execute("DROP TABLE IF EXISTS test;")
cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
print("** Created table.")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
print("** Exectuted SQL INSERT into database.")

# Query the database and obtain data as Python objects
cur.execute("SELECT * FROM test;")
print("** Output from SQL SELECT: ", cur.fetchone())

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()
print("** Closed connection and database.  Bye!.")