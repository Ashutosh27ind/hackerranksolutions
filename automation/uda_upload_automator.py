import xlrd
import os
import cx_Oracle
import re
import sys
import logging

# Set logging level and config.

logging.basicConfig(filename='uda_upload_automator.log', format='%(asctime)s-%(message)s', level=logging.INFO)


# Make custom user defined exception


class InvalidBrand(Exception):
    """Raised when Brand input in Invalid"""
    pass


class InvalidFormat(Exception):
    """Raised when columns numbers are not 2 or 3"""
    pass


def readexcel():
    base_location = "C:\\Users\\alaskar\\Documents\\Python Scripts\\uda_upload"
    logging.info("Current working directory {0}".format(os.getcwd()))
    if os.getcwd() != base_location:
        os.chdir(base_location)
    logging.info("Working directory changed to {0}".format(os.getcwd()))
    # declare separate arrays for lb and ca
    lb_rows = []
    ca_rows = []
    for f in os.listdir(os.curdir):
        if f.endswith('xlsx') or f.endswith('xls'):
            try:
                workbook = xlrd.open_workbook(f)
            except FileNotFoundError as fnf:
                logging.error("File {0} not found inside working directory {1} ".format(f, os.getcwd()))
                quit(255)
            except Exception as e:
                logging.error(e)
                quit(255)
            # nsheet = workbook.nsheets
            logging.info('Number of Sheets in the excel {0} is {1}'.format(f, workbook.nsheets))
            # 2 lists for storing records of different brands
            for c in range(workbook.nsheets):
                worksheet = workbook.sheet_by_index(c)
                # print worksheet name
                # logging.INFO('Starting to process sheet {0}'.format(worksheet.name))
                # print(worksheet.name)
                # Get the UDA from sheet name
                try:
                    if worksheet.name.count('LB') != 0:
                        logging.info("LB Sheet Found, Processing {0}".format(worksheet.name))
                        # print(worksheet.name)
                        uda_id = int(re.findall('[0-9]+', worksheet.name).pop(0))
                        # logging.INFO('UDA ID:{0}'.format(uda_id))
                        # logging.INFO('Number of columns in the sheet is {0}'.format(worksheet.ncols))
                        # Iterate through columns and rows
                        for r in range(1, worksheet.nrows):
                            sku = int(worksheet.cell(r, 0).value)
                            if worksheet.ncols == 2:
                                color = None
                                val = int(worksheet.cell(r, 1).value)
                                itemtype = 'S'
                            elif worksheet.ncols == 3:
                                color = int(worksheet.cell(r, 1).value)
                                val = int(worksheet.cell(r, 2).value)
                                itemtype = 'STY'
                            else:
                                raise InvalidFormat
                            lb_rows.append((sku, itemtype, color, val, uda_id))
                    elif worksheet.name.count('CA') != 0:
                        logging.info("CA Sheet Found, Processing {0}".format(worksheet.name))
                        uda_id = int(re.findall('[0-9]+', worksheet.name).pop(0))
                        # logging.INFO('UDA ID:{0}'.format(uda_id))
                        # logging.INFO('Number of columns in the sheet is {0}'.format(worksheet.ncols))
                        # Iterate through columns and rows
                        for r in range(1, worksheet.nrows):
                            sku = int(worksheet.cell(r, 0).value)
                            if worksheet.ncols == 2:
                                color = None
                                val = int(worksheet.cell(r, 1).value)
                                itemtype = 'S'
                            elif worksheet.ncols == 3:
                                color = int(worksheet.cell(r, 1).value)
                                val = int(worksheet.cell(r, 2).value)
                                itemtype = 'STY'
                            else:
                                raise InvalidFormat
                            ca_rows.append((sku, itemtype, color, val, uda_id))
                    else:
                        logging.warning(
                            "Sheet <{0}> Without Brand Identifier Found, Please Investigate".format(worksheet.name))
                except InvalidFormat:
                    logging.warning(
                        'Data in sheet {0} is not in proper format. Moving to next sheet.'.format(worksheet.name))
                    # changed the file extension sop that it's not picked up
                    os.rename(f, f + '.ERROR')
                    continue
                except Exception as e:
                    os.rename(f, f + '.ERROR')
                    logging.error(e)
                    continue

    return lb_rows, ca_rows


def perform_database_operations(conn, row, usr):
    # logging.INFO('Opening a cursor object.')
    cursor = conn.cursor()
    # Clean up the tables
    logging.info('Cursor Opened. Now proceeding to truncate the staging table.')
    statment = """TRUNCATE TABLE {0}.uda_upload_stage""".format(usr)
    if append_data == 'N':
        cursor.execute(statment)
        logging.info("{0}.uda_upload_stage Truncated".format(usr))
    else:
        pass
    # logging.INFO('staging table truncated.')
    cursor.bindarraysize = 10000
    cursor.setinputsizes(25, 2, 5, 5, int)
    statment = """INSERT INTO {0}.uda_upload_stage VALUES (:1,:2,:3,:4,:5)""".format(usr)
    cursor.executemany(statment, row)
    logging.info("Number of rows inserted {0}".format(cursor.rowcount))
    # logging.INFO('Successfully inserted the rows into database.')
    logging.info("Proceeding to delete duplicate records in {0}.uda_upload_stage".format(usr))
    # Remove duplicates
    statment = """
			DELETE FROM {0}.uda_upload_stage a 
			 WHERE	a.ROWID > (SELECT Min(b.ROWID) 
								 FROM	{0}.uda_upload_stage b 
								WHERE  a.item = b.item 
								  AND a.uda_id = b.uda_id 
								  AND a.uda_value = b.uda_value) 
			   AND item_type = 'S'	 
	""".format(usr)
    cursor.execute(statment)
    logging.info(statment)
    logging.info("{0} duplicate SKU records are deleted".format(cursor.rowcount))
    statement = """
			DELETE FROM {0}.uda_upload_stage a 
			 WHERE	a.ROWID > (SELECT Min(b.ROWID) 
								 FROM	{0}.uda_upload_stage b 
								WHERE  a.item = b.item 
								  AND a.uda_id = b.uda_id 
								  AND a.uda_value = b.uda_value 
								  AND a.color_code = b.color_code) 
			  AND item_type = 'STY'
	""".format(usr)
    logging.info(statment)
    cursor.execute(statment)
    logging.info("{0} duplicate Style records are deleted".format(cursor.rowcount))
    conn.commit()
    logging.info('Committed')


if __name__ == '__main__':

    # Get the file location.
    user = sys.argv[1]
    password = sys.argv[2]
    brand = sys.argv[3]
    file = sys.argv[4]
    append_data = sys.argv[5]

    # Make connection to Oracle
    LB_dsnString = cx_Oracle.makedsn('l00coelbrmsdb01.corp.local', '1521', 'rmscoe')
    CA_dsnString = cx_Oracle.makedsn('l00coecarmsdb01.corp.local', '1521', 'RMSCECA')

    rows_lb, rows_ca = readexcel()
    # print(rows)
    try:
        if not rows_lb:
            connect_lb = cx_Oracle.connect(user, password, LB_dsnString)
            # Make connection to LB database.
            perform_database_operations(connect_lb, rows_lb, user)
        if not rows_ca:
            connect_ca = cx_Oracle.connect(user, password, CA_dsnString)
            perform_database_operations(connect_ca, rows_ca, user)
    except Exception as e:
        print(e)
        quit(255)
    quit(0)
