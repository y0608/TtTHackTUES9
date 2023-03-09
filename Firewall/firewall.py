import mysql.connector

db_user = ''
db_password = ''

tdb_host = ''
tdb_database = ''

wldb_host = ''
wldb_database = ''

def get_source_and_destination(input):
    pass

    connection = mysql.connector.connect(
    tdb_host, tdb_database, db_user, db_password)

    sql_select_Query = "select * from Laptop"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)

    records = cursor.fetchall()

    # return both
    return source, destination

def get_invalid_ips(ip):
    # get ips from the blacklist database
    pass

    connection = mysql.connector.connect(
    wldb_host, wldb_database, db_user, db_password)

    sql_select_Query = "select * from Laptop"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)

    records = cursor.fetchall()

def get_valid_ips(ip):
    # get ips from the whitelist database
    pass

    connection = mysql.connector.connect(
    wldb_host, wldb_database, db_user, db_password)

    sql_select_Query = "select * from Laptop"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)

    records = cursor.fetchall()

def unblock_ip(ip):
    # unblock ip
    # remove from blacklist database if exists
    whitelist_ip(ip)
    pass

def block_ip(ip):
    # block ip
    # remove from whitelist database if exists
    blacklist_ip(ip)
    pass

def whitelist_ip(ip):
    # add ip to the whitelist database
    pass

    connection = mysql.connector.connect(
    wldb_host, wldb_database, db_user, db_password)

    #Creating a cursor object using the cursor() method
    cursor = connection.cursor()

    # Preparing SQL query to INSERT a record into the database.
    sql = """INSERT INTO EMPLOYEE(
    FIRST_NAME, LAST_NAME, AGE, SEX, INCOME)
    VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""

    # Executing the SQL command
    cursor.execute(sql)

    # Commit your changes in the database
    connection.commit()    

def blacklist_ip(ip):
    # add ip to the blacklist database
    pass

    connection = mysql.connector.connect(
    wldb_host, wldb_database, db_user, db_password)

    #Creating a cursor object using the cursor() method
    cursor = connection.cursor()

    # Preparing SQL query to INSERT a record into the database.
    sql = """INSERT INTO EMPLOYEE(
    FIRST_NAME, LAST_NAME, AGE, SEX, INCOME)
    VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""

    # Executing the SQL command
    cursor.execute(sql)

    # Commit your changes in the database
    connection.commit()

def IoT_to_Internet(source, destination):
    valid_ips = get_valid_ips(source)

    if 2 > valid_ips.len():
        whitelist_ip(destination)
        return

    if 1 > valid_ips.count(destination):
        block_ip(source)
        return

def Internet_to_IoT(source, destination):
    pass


        ##DATABASE##    
##############################
connection = mysql.connector.connect(
    tdb_host, tdb_database, db_user, db_password)

sql_select_Query = "select * from Laptop"
cursor = connection.cursor()
cursor.execute(sql_select_Query)

# get all records
records = cursor.fetchall()

for row in records:
    print("Id = ", row[0], )
    print("Name = ", row[1])
    print("Price  = ", row[2])
    print("Purchase date  = ", row[3], "\n")

    # check for each row 
    source, destination = get_source_and_destination(row)

    IoT_to_Internet(source, destination)
    Internet_to_IoT(source, destination)

############################
