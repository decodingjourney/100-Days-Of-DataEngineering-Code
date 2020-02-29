import psycopg2
from connectiondb import config
import os
import csv
proj_dir = os.path.dirname(os.path.abspath(__file__))
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = [
        """
        CREATE TABLE ckclighting
(
    light_parentdomain character varying(100),
    light_devicestate_connstate_connected character varying(100),
    light_devicestate_connstate_since character varying(100),
    light_state_reliability character varying(100),
    light_tenantid character varying(100),
    light_locationid_2 character varying(100),
    light_geocoordinates_longitude character varying(100),
    light_lastupdated character varying(100),
    light_sid character varying(100),
    light_geohash character varying(100),
    light_private_lamp_status character varying(100),
    light_state_powerconsumption character varying(100),
    light_createtime character varying(100),
    light_isvalid character varying(100),
    light_powermeter character varying(100),
    light_locationname_0 character varying(100),
    light_state_intensitylevel_request_value character varying(100),
    light_applicabledomain_0 character varying(100),
    light_status character varying(100),
    light_state_intensitylevel_lastknownvalue character varying(100),
    light_locationid_1 character varying(100),
    light_locationid_0 character varying(100),
    light_mode_0 character varying(100),
    light_locationid_3 character varying(100),
    light_thirdpartyid character varying(100),
    light_providerdetails_provider character varying(100),
    light_isindependent character varying(100),
    light_label character varying(100),
    light_geocoordinates_latitude character varying(100)
);
        """]
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_vender(vender_name):
    ''' This method gets the vender name as a parameter which is to be inserted into the databases.'''

    sql_statement = 'INSERT INTO VENDORS(vendor_name) VALUES(%s) returning vendor_id;'
    conn = None
    vendor_id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql_statement, (vender_name,))
        vendor_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return vendor_id


def insert_vendor_list(vendor_list):
    ''' This method insert vender list into the table '''

    sql_statement = 'INSERT INTO VENDORS(vendor_name) VALUES(%s)'
    conn = None
    try:

        param = config()

        conn = psycopg2.connect(**param)
        cur = conn.cursor()
        cur.executemany(sql_statement, vendor_list)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_csv_to_table():
    ''' This Method is used to read the csv file and load it to the database'''

    conn = None
    params = config()
    try:
        ''' Returning the Connection instances'''
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        with open(proj_dir + '/lighting_data_db.csv') as csv_file:
            reader = csv.reader(csv_file)
            # next(csv_file)
            # cur.copy_from(csv_file, 'ckclighting', sep=',')
            for row in reader:
                # for i in range(len(row) - 1):
                #     print(str(row[i]))
                    cur.execute('INSERT INTO ckclighting VALUES (%s)', row)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def update_table(vendor_id, vendor_name):
    ''' This Method is updating the column values '''
    sql_statement = ''' UPDATE vendors
                        SET vendor_name = %s
                        WHERE vendor_id = %s
                        '''
    conn = None
    count = 0

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql_statement, (vendor_name, vendor_id))
        count = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return count


def fetch_records():
    conn = None
    sql_statement = ''' SELECT part_name, vendor_name
            FROM parts
            INNER JOIN vendor_parts ON vendor_parts.part_id = parts.part_id
            INNER JOIN vendors ON vendors.vendor_id = vendor_parts.vendor_id
            ORDER BY part_name;
            '''
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql_statement)
        print('Total records are {}'.format(cur.rowcount))
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()









if __name__ == '__main__':
    create_tables()
    insert_vender('Pepsi_coca')
    create_tables()
    insert_vendor_list([
        ('AKM Semiconductor Inc.',),
        ('Asahi Glass Co Ltd.',),
        ('Daikin Industries Ltd.',),
        ('Dynacast International Inc.',),
        ('Foster Electric Co. Ltd.',),
        ('Murata Manufacturing Co. Ltd.',)
    ])
    insert_csv_to_table()
    rowcount = update_table(1, 'anand.co.in')
    print('Total {} columns are modified'.format(rowcount))
    fetch_records()
