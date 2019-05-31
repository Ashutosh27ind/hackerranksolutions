import xlrd
import os
import cx_Oracle
import re
import sys
import logging


"""
Program: UDA_UPLOAD_AUTOMATOR.py
Puspose: This program is used to load data from excel file to database. 
Author: Asfakul Laskar

--Change Log:
001 added change to handle multile file at once.
002 made change to ignore hidden sheets
003 if successfully processed, file will be marked as .DONE
004 modified logging to include complete stack trace of exception.
005 

"""


# Set logging level and config.

logging.basicConfig(filename='uda_upload_automator.log', filemode='w', format='%(asctime)s- %(levelname)s- %(message)s',
                    level=logging.INFO)


class InvalidFormat(Exception):
    """Raised when columns numbers are not 2 or 3"""
    pass


# Variable to hold successfully processed files name
processedFiles = []


def readexcel():
    base_location = 'C:\\Users\\alaskar\\Documents\\Python Scripts\\uda_upload'
    logging.info('Current working directory {0}'.format(os.getcwd()))
    if os.getcwd() != base_location:
        os.chdir(base_location)
    logging.info('Working directory changed to {0}'.format(os.getcwd()))
    # declare separate arrays for lb and ca
    lb_rows = []
    ca_rows = []
    for f in os.listdir(os.curdir):
        # if len(fnmatch.filter(os.listdir('.'), '*.xlsx')) == 0:
        #     logging.warning('Number of files to process is 0, Program will exit now!')
        #     quit(0)
        # logging.info('Number Of Files Found {0}'.format(len(fnmatch.filter(os.listdir('.'), '*.xlsx'))))
        if f.endswith('xlsx') or f.endswith('xls'):
            try:
                logging.info('Proceessing File {0}'.format(f))
                workbook = xlrd.open_workbook(f)
                logging.info('Number of Sheets in the excel {0} is {1}'.format(f, workbook.nsheets))
                for c in range(workbook.nsheets):
                    worksheet = workbook.sheet_by_index(c)
                    isHidden = worksheet.visibility
                    # If sheet is Hidden
                    if isHidden == 1:
                        logging.warning('{0} is marked as hidden, Ignoring the hidden sheet.'.format(worksheet.name))
                        continue
                    if worksheet.ncols not in (2, 3):
                        raise InvalidFormat
                    if worksheet.name.count('LB') != 0:
                        logging.info("LB Sheet Found, Processing {0}".format(worksheet.name))
                        uda_id = int(re.findall('[0-9]+', worksheet.name).pop(0))
                        for r in range(1, worksheet.nrows):
                            sku = int(worksheet.cell(r, 0).value)
                            if worksheet.ncols == 2:
                                color = 0
                                val = worksheet.cell(r, 1).value
                                itemtype = 'S'
                            elif worksheet.ncols == 3:
                                color = int(worksheet.cell(r, 1).value)
                                val = worksheet.cell(r, 2).value
                                itemtype = 'STY'
                            lb_rows.append((sku, itemtype, color, val, uda_id))
                    elif worksheet.name.count('CA') != 0:
                        logging.info("CA Sheet Found, Processing {0}".format(worksheet.name))
                        uda_id = int(re.findall('[0-9]+', worksheet.name).pop(0))
                        for r in range(1, worksheet.nrows):
                            sku = int(worksheet.cell(r, 0).value)
                            if worksheet.ncols == 2:
                                color = 0
                                val = worksheet.cell(r, 1).value
                                itemtype = 'S'
                            elif worksheet.ncols == 3:
                                color = int(worksheet.cell(r, 1).value)
                                val = worksheet.cell(r, 2).value
                                itemtype = 'STY'
                            ca_rows.append((sku, itemtype, color, val, uda_id))
                    else:
                        logging.warning(
                            "Sheet <{0}> Without Brand Identifier Found, Please Investigate".format(worksheet.name))
                        continue
            except InvalidFormat:
                logging.warning('Sheet {0} is not in standard format, a sheet must have eiher 2 or 3 columns.'
                                'Skipping to next sheet.'.format(worksheet.name))
                continue
            except Exception:
                logging.error('Exception Occured during excel file reading.', exc_info=True)
                logging.warning('Skipping to next sheet.')
                continue
            else:
                processedFiles.append(f)

    return lb_rows, ca_rows


def perform_database_operations(conn, row, usr):
    try:
        cursor = conn.cursor()
        # Clean up the tables
        statement = """TRUNCATE TABLE {0}.uda_upload_stage""".format(usr)
        if append_data == 'N':
            logging.info('Now proceeding to truncate the staging table.')
            cursor.execute(statement)
            logging.info('{0}.uda_upload_stage Truncated.'.format(usr))
        else:
            logging.info('Data will be apended.')
        cursor.bindarraysize = 10000
        cursor.setinputsizes(25, 3, 5, 3, 2)
        statement = """INSERT INTO {0}.uda_upload_stage VALUES (:1,:2,:3,:4,:5)""".format(usr)
        cursor.executemany(statement, row)
        logging.info("Number of rows inserted {0}".format(cursor.rowcount))
        logging.info("Proceeding to delete duplicate records in {0}.uda_upload_stage".format(usr))
        # Remove duplicates
        statement = """
            DELETE FROM {0}.uda_upload_stage a 
            WHERE   a.ROWID > (SELECT Min(b.ROWID) 
                                FROM	{0}.uda_upload_stage b 
                                WHERE  a.item = b.item 
                                AND a.uda_id = b.uda_id 
                                AND a.uda_value = b.uda_value) 
            AND item_type = 'S'	 
            """.format(usr)
        cursor.execute(statement)
        logging.info(statement)
        logging.info('{0} duplicate SKU records are deleted'.format(cursor.rowcount))
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
        logging.info(statement)
        cursor.execute(statement)
        logging.info('{0} duplicate Style records are deleted'.format(cursor.rowcount))
        # Removing Invalid items

        statement = """
                    DELETE FROM {0}.uda_upload_stage
                    WHERE item NOT IN (SELECT item from item_master where status = 'A')
        """.format(usr)
        logging.info(statement)
        cursor.execute(statement)
        logging.info('{0} Invalid items have been removed.'.format(cursor.rowcount))
        conn.commit()
        logging.info('Committed')
        print('Successfully Executed')
    except Exception as e:
        logging.error('Error during performing database operation', exc_info=True)
        print('Failed!')
        quit(1)


if __name__ == '__main__':

    user = sys.argv[1]
    password = sys.argv[2]
    append_data = sys.argv[3]

    # Make connection to Oracle
    LB_dsnString = cx_Oracle.makedsn('l00coelbrmsdb01.corp.local', '1521', 'rmscoe')
    CA_dsnString = cx_Oracle.makedsn('l00coecarmsdb01.corp.local', '1521', 'RMSCECA')

    rows_lb, rows_ca = readexcel()
    # print(rows)
    try:
        if rows_lb:
            connect_lb = cx_Oracle.connect(user, password, LB_dsnString)
            # Make connection to LB database.
            perform_database_operations(connect_lb, rows_lb, user)
        if rows_ca:
            connect_ca = cx_Oracle.connect(user, password, CA_dsnString)
            perform_database_operations(connect_ca, rows_ca, user)
    except Exception as e:
        logging.error('Error During validations in main block', exc_info=True)
        quit(1)
    else:
        for file in set(processedFiles):
            os.rename(file, file + '.DONE')
    quit(0)
