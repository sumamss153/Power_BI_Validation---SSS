import pandas as pd
import pyodbc as pc
import psycopg2 as mc
import numpy as np
import openpyxl
import os

file_location = "C:\\Users\\Sumam.Selvin\\Downloads"
input_loc = file_location + "\\" + "Python_Input.txt"

def getinputdata():
    mydict = {}
    print(input_loc)
    with open(input_loc, 'rt') as myfile:
    #with open('C:\\Users\\ZP912JM\\Downloads\\Python_Input.txt', 'rt') as myfile:
        for myline in myfile:
            k, v = myline.strip().split('= ')
            mydict[k.strip()] = v.strip()

    databasetype = mydict['databasetype']
    hostname = mydict['hostname']
    print('hostname ', hostname)
    port = mydict['port']
    # print('port ', port)
    username = mydict['username']
    password = mydict['password']
    database = mydict['database']
    database = database.replace('"', '')
    datasourcetype = mydict['datasourcetype']
    return  databasetype, hostname, port, username, password, database, datasourcetype

def readcsv(file_location, file_name):##Read the csv/xlsx file from the location and return it as a dataframe.

    # file_location, file_name , _,_,_,_,_,_,_ = getinputdata()
    if str(file_name).lower().endswith('.xlsx'):
        #return pd.read_excel((str(file_location) + "\\" + str(file_name)), header = [2], dtype = "str", engine = 'openpyxl').fillna('')
        #return c
        wb = openpyxl.load_workbook((str(file_location) + "\\" + str(file_name)))
        sheet = wb['Sheet1']
        #sheet.delete_rows(0, 2)
        wb.save((str(file_location) + "\\" + str(file_name)))
        c = pd.read_excel((str(file_location) + "\\" + str(file_name)), header=[0], dtype="str", engine='openpyxl').fillna('')
        print(c)
        return c
    elif str(file_name).lower().endswith('.csv'):
        return pd.read_csv((str(file_location) + "\\" + str(file_name)),header = [0], dtype = "str").fillna('')
    else:
        raise Exception("FileFormat not supported")

def testdatabaseconnection(databasetype, hostname, port, username, password, database):


    if (databasetype == 'sqlserver'):
        if database == "":
            connstring = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + str(hostname) + ';PORT=' + str(port) + ';UID=' + str(username) + ';PWD=' + str(
                password) + ';Trusted_Connection=No;MARS_Connection=Yes'
        else:
            connstring = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + str(hostname) + ';PORT=' + str(port) + ';UID=' + str(
                username) + ';PWD=' + str(password) + ';DATABASE=' + database + ';Trusted_Connection=No;MARS_Connection=Yes'
        try:
            conn = pc.connect(connstring)
            return True, conn

        except Exception as e:
            print(str(e))
            return False, str(e)

    elif (databasetype == 'postgres'):
        try:
            if database == '':
                conn = mc.connect(
                    user=username, password=password, host=hostname, port=port)
            else:
                conn = mc.connect(database=database, user=username,
                                  password=password, host=hostname, port=port)

            return True, conn
        except mc.Error as er:
            print(str(er))
            return False, str(er)
    elif (databasetype == 'MySQL'):
        try:
            if database == '':
                conn = mysql.connector.connect(user=username, password=password, host=hostname, port=port)
            else:
                conn = mysql.connector.connect(database=database,user=username, password=password, host=hostname, port=port)
            return True, conn
        except mc.Error as er:
            print(str(er))
            return False, str(er)
    elif (databasetype == 'hive'):
        # TODO DO configuration for Hive
        return False, 'Hive database currently not supported'
    elif (databasetype == 'oracle'):
        # TODO DO configuration for Hive
        return False, 'Oracle database currently not supported'
    elif (databasetype == 'sybase'):
        # TODO DO configuration for Sybase
        return False, 'Sybase database currently not supported'

    elif (databasetype == 'deltalake'):
        try:
            jarpath = os.path.join(
                settings.BASE_DIR, 'jars') + "/SparkJDBC42.jar"
            print(jarpath)
            url = "jdbc:spark://" + hostname + ":" + str(
                port) + "/default;transportMode=http;ssl=1;httpPath=" + username + ";AuthMech=3;UID=token;PWD=" + password
            conn = jaydebeapi.connect(
                "com.simba.spark.jdbc.Driver", url, [], jarpath)
            return True, conn
        except Exception as e:
            return False, str(e)

def getquerydata(query,datasourcetype,databasetype, hostname, port, username, password, database): # to get the table data

    if datasourcetype == 'database':
        # databasetype = connection.values('databasetype').get()['databasetype']
        # hostname = connection.values('hostname').get()['hostname']
        # username = connection.values('username').get()['username']
        # port = connection.values('port').get()['port']
        # password = connection.values('password').get()['password']
        # databasename = connection.values('databasename').get()['databasename']

        # if databasename is None:
        #     databasename = ''
        status, conn = testdatabaseconnection(
            databasetype, hostname, port, username, password, database)
        # print(status)
        if status:

            df1 = pd.read_sql(query, conn)
            return True, df1.applymap(str), list(df1.columns)
        else:
            return False, conn, conn

def validatepandadataset(src_data, trg_data,file_name):
    # execstarttime = datetime.datetime.now()

    print("************************ Raw Data ************************")
    print("src_data ", src_data)
    print("trg_data ", trg_data)
    print("************************ Data Treated after replacing Nan to NULL ************************")
    trg_data = trg_data.replace('NULL', '', regex=True) ## Now with the new code , we want to make the NULL to spaces in Target to match to SRC
    print("src_data ", src_data)
    print("trg_data ", trg_data)
    print(src_data.dtypes)
    print(trg_data.dtypes)

    print("************************ Both the data is been converted to string ************************")
    src_data = src_data.applymap(str)
    trg_data = trg_data.applymap(str)
    print(src_data.dtypes)
    print(trg_data.dtypes)
    print("src_data ", src_data)
    print("TRg data ", trg_data)
    try:
        print("*****Try*****")
        source_record_count = None
        target_record_count = None
        status_count = 'error'

        # source_duplicate_status = 'error'
        # df_source_duplicates = None
        # source_duplicatecount = None
        # target_duplicate_status = 'error'
        # df_target_duplicates = None
        # target_duplicatecount = None

        matched_row_status = 'error'
        count_match = None
        unmatched_row_status = 'error'
        df_unmatch = None
        count_unmatch = None

        source_unique_status = 'error'
        df_src_unique = None
        source_unique_count = None
        target_unique_status = 'error'
        df_trg_unique = None
        target_unique_count = None


        source_record_count = len(src_data)
        target_record_count = len(trg_data)
        print("source_record_count ",source_record_count)
        print("target_record_count ",target_record_count)

        cnt_flag = 1
        if (source_record_count == target_record_count):
            status_count = True
        else:
            status_count = False
        print("status_count ", status_count)
        src_data = src_data.set_axis(trg_data.columns.values, axis=1, inplace=False)
        print("axissrcdata ", src_data)

        #the src and tgt unique column values.
        src_unique = list(src_data.columns.values)
        print("src_unique -->", src_unique)
        src_unique = src_unique[0]
        print(src_unique)
        trg_unique = list(trg_data.columns.values)
        print("trg_unique -->", trg_unique)
        trg_unique = trg_unique[0]
        print("trg_unique -->", trg_unique)

        src_data = src_data.set_axis(trg_data.columns.values, axis=1, inplace=False)
        src_unique = list(src_data.columns.values)
        #print("src_unique ", src_unique)
        trg_unique = list(trg_data.columns.values)
        #print("trg_unique ", trg_unique)
        src = src_data.nunique(axis=0)
        source_record_count = len(src_data)
        print("rc  ", src, type(src))
        for sr in src_unique:
            if (src[sr] == len(src_data)):
                src_unique = sr
                print(src_unique)
                break
            else:
                print("not sucess")
        print("src_unique ", src_unique)
        trg_unique = src_unique
        print("src_unique ", src_unique)
        print("trg_unique ", trg_unique)

        # src_unique = trg_unique

        # find and remove source Duplicates
        # src_datax = src_data.duplicated(subset=src_unique, keep='first')
        # df_source_duplicates = src_data.loc[src_datax == True]
        # src_data = src_data.loc[src_datax == False]
        # del src_datax

        # find and remove target Duplicates
        # trg_datax = trg_data.duplicated(subset=trg_unique, keep='first')
        # df_target_duplicates = trg_data.loc[trg_datax == True]
        # trg_data = trg_data.loc[trg_datax == False]
        # del trg_datax


        # sort the source and target data based on PK
        # print(src_data)
        src_data = src_data.sort_values(src_unique).reset_index(drop=True)
        print("sorteds ", src_data)
        trg_data = trg_data.sort_values(trg_unique).reset_index(drop=True)
        print("sortedt ", trg_data)

        # Get all records of source which are not in target to df_src
        src_datanot = pd.concat([src_data, trg_data]).drop_duplicates(subset=src_unique, keep=False)
        print("src_datanot ", src_datanot)
        df_src_unique = pd.merge(src_data, src_datanot, how='inner')
        print("df_src_unique ", df_src_unique) #extra record
        df_copy = pd.DataFrame().reindex_like(df_src_unique)
        print("df_copy ", df_copy)
        src_extra = pd.concat([df_src_unique, df_copy], axis='columns', keys=['Source','Target'])
        print("src_extra ", src_extra)


        # Get all recors of target which are not in Source to df_trg
        df_trg_unique = pd.merge(trg_data, src_datanot, how='inner')
        print("df_trg_unique ", df_trg_unique)

        tgt_extra = pd.concat([df_copy, df_trg_unique], axis='columns', keys=['Source','Target'])
        print("tgt_extra ", tgt_extra)  # extra record in tgt
        extra_res = pd.concat([src_extra, tgt_extra], axis=0)
        extra_res = extra_res.reset_index(drop=True)
        print("extra_res ",extra_res)
        e_df_final = extra_res.swaplevel(axis='columns')[src_data.columns[0:]]
        print("e_df_final ", e_df_final)
        e_df_unmatch = e_df_final.stack().drop_duplicates(subset=None, keep=False)
        print("e_df_unmatch ", e_df_unmatch)

        # Remove the data not present in each other
        src_data1 = pd.concat([src_data, df_src_unique]).drop_duplicates(keep=False).reset_index(drop=True)
        print("src_data1 ", src_data1)
        trg_data1 = pd.concat([trg_data, df_trg_unique]).drop_duplicates(keep=False).reset_index(drop=True)
        print("trg_data1 ", trg_data1)

        # match
        df_match = pd.concat([src_data1, trg_data1]).duplicated(subset=None, keep='first')
        print("df_match ", df_match)
        df_match = pd.concat([src_data1, trg_data1]).loc[df_match == True]
        print("df_match ", df_match)
        # Unmatched rows
        df_all = pd.concat([src_data1, trg_data1],axis='columns', keys=['Source', 'Target'])
        print("df_all ",df_all)
        df_final = df_all.swaplevel(axis='columns')[src_data.columns[0:]]
        print("df_final ", df_final)
        df_unmatch = df_final.stack().drop_duplicates(subset=None, keep=False)
        print("df_unmatch ", df_unmatch)
        count_unmatch = int(len(df_unmatch) / 2)
        count_match = len(df_match)
        # print("count_match/un   ",count_match, count_unmatch, type(count_unmatch))

        fin_res = pd.concat([df_unmatch, e_df_unmatch ], axis=0)
        print("fin_res ", fin_res)

        #fin_res.to_excel(r'C:\\Users\\ZP912JM\\Downloads\\fin_res_final.xlsx', index=True, header=True)
        # df_final.to_excel(r'C:\\Users\\ZP912JM\\Downloads\\df_final.xlsx', index=True, header=True)
        # df_unmatch.to_excel(r'C:\\Users\\ZP912JM\\Downloads\\df_unmatch.xlsx', index=True, header=True)


        if count_unmatch == 0:
            matched_row_status = True
            unmatched_row_status = True
        else:
            matched_row_status = False
            unmatched_row_status = False


        source_unique_count = len(df_src_unique)
        print(source_unique_count)
        target_unique_count = len(df_trg_unique)
        print(target_unique_count)

        if source_unique_count == 0:
            source_unique_status = True
        else:
            source_unique_status = False
        if target_unique_count == 0:
            target_unique_status = True
        else:
            target_unique_status = False

        if ((target_unique_status == False) or (source_unique_status == False) or (matched_row_status == False) or (unmatched_row_status == False)):
            file_name1 = "Mismatch_" + str(file_name)
            print(file_name1)
            # file_n = 'C:\\Users\\ZP912JM\\Downloads\\' + str(file_name1)
            file_n = file_location + "\\" + str(file_name1)
            # filename ='file_n'
            print(file_n)
            if str(file_n).lower().endswith('.xlsx'):
                fin_res.to_excel(file_n, index=True, header=True)
            else:
                fin_res.to_csv(file_n, index=True, header=True)


        # ststuses = [status_count, target_duplicate_status, unmatched_row_status, source_unique_status,
        #             target_unique_status]
        ststuses = [status_count,   unmatched_row_status, source_unique_status, target_unique_status]

        x = all(ststuses)

        if not x:
            execstatus = False
        else:
            execstatus = True
        # execendtime = datetime.datetime.now()
        data = {"execstatus": execstatus,
                # "execstarttime": execstarttime,
                # "execendtime": execendtime,
                "source_record_count": source_record_count, "target_record_count": target_record_count,
                "record_count_status": status_count,
                # "source_duplicate_status": source_duplicate_status, "source_duplicaterows": df_source_duplicates,
                # "source_duplicatecount": source_duplicatecount,
                # "target_duplicate_status": target_duplicate_status, "target_duplicaterows": df_target_duplicates,
                # "target_duplicatecount": target_duplicatecount,
                "matched_row_status": matched_row_status, "matched_row_count": count_match,
                "unmatched_row_status": unmatched_row_status, "unmatched_rows": df_unmatch,
                "unmatched_row_count": count_unmatch, "uniquesource_row_status": source_unique_status,
                "uniquesource_rows": df_src_unique, "uniquesource_row_count": source_unique_count,
                "uniquetarget_row_status": target_unique_status, "uniquetarget_rows": df_trg_unique,
                "uniquetarget_row_count": target_unique_count, "errmsg": ''
                }
        return True, data
    except Exception as e:
        print("Except")
        # execendtime = datetime.datetime.now()
        execstatus = None
        if status_count == 'error':
            Error_message = "Failed at Record count Validation. Error: " + str(e)
        # elif source_duplicate_status == 'error':
        #     Error_message = "Failed at Source Duplicate Validation. Error: " + str(e)
        # elif target_duplicate_status == 'error':
        #     Error_message = "Failed at Target Duplicate Validation. Error: " + str(e)
        elif matched_row_status == 'error':
            Error_message = "Failed at Matched records Validation. Error: " + str(e)
        elif unmatched_row_status == 'error':
            Error_message = "Failed at Mis match records Validation. Error: " + str(e)
        elif source_unique_status == 'error':
            Error_message = "Failed at Source unique validation. Error: " + str(e)
        elif target_unique_status == 'error':
            Error_message = "Failed at Target unique validation. Error: " + str(e)
        else:
            Error_message = "Failed with error" + str(e)
        print(Error_message)

        data = {"execstatus": execstatus,
                # "execstarttime": execstarttime,
                # "execendtime": execendtime,
                "source_record_count": source_record_count, "target_record_count": target_record_count,
                "record_count_status": status_count,
                # "source_duplicate_status": source_duplicate_status, "source_duplicaterows": df_source_duplicates,
                # "source_duplicatecount": source_duplicatecount,
                # "target_duplicate_status": target_duplicate_status, "target_duplicaterows": df_target_duplicates,
                # "target_duplicatecount": target_duplicatecount,
                "matched_row_status": matched_row_status, "matched_row_count": count_match,
                "unmatched_row_status": unmatched_row_status, "unmatched_rows": df_unmatch,
                "unmatched_row_count": count_unmatch,
                "uniquesource_row_status": source_unique_status, "uniquesource_rows": df_src_unique,
                "uniquesource_row_count": source_unique_count,
                "uniquetarget_row_status": target_unique_status, "uniquetarget_rows": df_trg_unique,
                "uniquetarget_row_count": target_unique_count,
                "errmsg": Error_message
                }

        return execstatus, data

def Comparison_PowerBI_with_DB(query, file_name):
    #file_location = "C:\\Users\\ZP912JM\\Downloads"
    file_name = file_name
    # file_location, file_name, databasetype, hostname, port, username, password, database, datasourcetype = getinputdata()
    databasetype, hostname, port, username, password, database, datasourcetype = getinputdata()
    # bi_data = pd.read_excel((str(file_location) + "\\" + str(file_name)), header = [2], dtype = "str").fillna('')
    bi_data = readcsv(file_location, file_name)
    status, con = testdatabaseconnection(databasetype, hostname, port, username, password, database)
    stat, dfdataset, trgt_colmn = getquerydata(query,datasourcetype,databasetype, hostname, port, username, password, database)
    status, dat = validatepandadataset(bi_data, dfdataset,file_name)
    print(status, dat)

#Comparison_PowerBI_with_DB("SELECT to_char(datum ,'YYYY-MM-DD 00:00:00') as datum, iphone_8, iphone_8_forecast , iphone_xr, iphone_xr_forecast , iphone_x, iphone_x_forecast FROM public.FORECAST_TMP", "Forecast of iOS Devices by Date.xlsx")
#Comparison_PowerBI_with_DB("select Devices, cast(Sum_of_iOS as DECIMAL) Sum_of_iOS from top_ios_device", "Top 3 iOS Devices.xlsx")

#getinputdata()

#python -m robot C:\PowerBI_Automation\development\Power_BI_Validation\Test\Scripts\BI_DB_Validation.robot

#readcsv("C:\\Users\\ZP912JM\\Downloads","Forecast of iOS Devices by Date.xlsx")

