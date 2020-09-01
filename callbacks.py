# callbacks.py

import pandas as pd
import numpy as np
import pyodbc
import datetime

from dash.dependencies import Input, Output, State
import yaml
import json

from app import app
import models


# load app configuration!
# print('loading initial app configuration!!!!!')
config = yaml.safe_load(open("configuration.yaml", 'r'))

# for key, value in config.items():
#     print (key + " : " + str(value))

# global area - get live empower data
term = config['TERM']
update_interval_in_minutes = config['UPDATE_INTERVAL_IN_MINUTES']

empower = pyodbc.connect(dsn=config['DSN'])

# print("term = ", config['TERM'])
# print("dsn = ", config['DSN'])
# print("update_interval_in_minutes = ", config['UPDATE_INTERVAL_IN_MINUTES'])
# print('')


# CALLBACK functions
###############################################################################
@app.callback(Output('dashboard-datasets', 'children'),
              [Input('interval-component', 'n_intervals')])
def build_dashboard_datasets(n):
    # modified on 11/07/2019

    print('')
    print('UPDATING BASELINE DASHBOARD DATA!!!')
    print('')
    # print('inside build_dashboard_datasets!!!!!!')

    df1 = models.build_empower_dataset_1(empower, term)
    df2 = models.build_empower_dataset_2(empower, term)
    df3 = models.build_empower_dataset_3(empower, term)
    df4_p1 = models.build_empower_dataset_4_p1(empower, term)
    df4_p2 = models.build_empower_dataset_4_p2(empower, term)
    # df4b = models.build_empower_dataset_4b(empower, term)
    df5 = models.build_empower_dataset_5(empower, term)

    #create dataset for DateLastAttended - based off of df5
    df6 = df5[(df5['ATND_ID'] == 'P') | (df5['ATND_ID'] == 'VP') | (df5['ATND_ID'] == 'T')].copy()
    df6.sort_values(['LAST_NAME', 'FIRST_NAME', 'ATND_DATE'], ascending=[True, True, False], inplace=True)
    df_attend_first = df6.drop_duplicates(subset='DFLT_ID', keep='first', inplace=False)
    #merge df1 and df_attend_first
    df1 = pd.merge(df1, df_attend_first[['DFLT_ID', 'ATND_DATE']], on='DFLT_ID', how='left')
    # df_merged['DateLastAttended'] = df_merged['ATND_DATE'].dt.date
    # df_merged.drop(labels=['DATE_STUD_STATUS', 'College', 'ATND_DATE'], axis='columns', inplace=True)
    df1.rename(columns={'ATND_DATE': 'DateLastAttended'}, inplace=True)

    # print('')
    # print(df_attend_first.columns)
    # print(df6.head(10))
    # print('')
    # print('')
    # print(df_attend_first.head())
    # print('')
    # print(df_merged.columns)
    # print('')
    # print(df_merged.head())
    # print('')
    # print('')

    # print('')
    # print(df3.columns)
    # print('')
    # print('')
    # print('')
    # print(df4b.head())
    # print('')
    # print(df4b['TIME_START'].apply(type))
    # print(df4b['TIME_END'].apply(type))
    # print('')
    # print('')

    # modify d1 so can limit to TRAD students/majors only
    df1['IsTrad'] = (df1['PRGM_ID1'].str.find(sub='TR', start=0, end=2) == 0)
    # df1['IsTrad'] = (df1['PRGM_ID1'].str.startswith('TR'))

    # build df_trad dataframe/dataset
    #######################################################################################
    df_trad = df1[(df1['IsTrad'] == True)].copy()

    # df_trad['DFLT_ID'] = df_trad['DFLT_ID'].astype(str)
    # df_trad['DFLT_ID'] = df_trad['DFLT_ID'].apply(lambda row: row.zfill(9))

    df_trad['College'] = 'TRAD'
    df_trad['FtPtStatus'] = np.where(df_trad['TU_CREDIT_ENRL'] >= 12, 'FT', 'PT')

    df_trad['Programs'] = df_trad.apply(lambda row: models.lookup_academic_program(row['MAMI_ID_MJ1'], config['Programs']), axis=1)

    df_trad.sort_values(['LAST_NAME', 'FIRST_NAME'], ascending=[True, True], inplace=True)
    df_trad['DFLT_ID'] = df_trad['DFLT_ID'].astype(str)
    df_trad['DFLT_ID'] = df_trad['DFLT_ID'].apply(lambda row: row.zfill(9))
    #######################################################################################

    # Add df_trad['NumCcsjSports'] dataframe column
    ######################################################################
    for index, row in df_trad.iterrows():
        # get matching rows in df_2
        df_temp = df2[(df2['DFLT_ID'] == row['DFLT_ID'])].copy()
        df_trad.loc[index, 'NumCcsjSports'] = len(df_temp.index)

    # Add IsAthlete dataframe column to df_trad
    df_trad['IsAthlete'] = np.where(df_trad['NumCcsjSports'] > 0, True, False)
    # df_trad['IsAthlete'] = df_trad['IsAthlete'].astype('bool')
    df_trad['IsAthlete'] = df_trad['IsAthlete'].astype(str)

    # Add df_trad['AthleticTeamCodes'] dataframe column
    ######################################################################
    for index, row in df_trad.iterrows():
        # get matching rows in df_2
        df_temp = df2[(df2['DFLT_ID'] == row['DFLT_ID'])].copy()

        result = ''
        for index2, row2 in df_temp.iterrows():
            result += row2['ACTI_ID'] + ' '

        df_trad.loc[index, 'AthleticTeamCodes'] = result

    df_trad['AthleticTeamCodes'] = df_trad['AthleticTeamCodes'].str.strip()

    # Add TotalAs, TotalEs, TotalPs, TotalTs, TotalHs, TotalCcs, TotalRecs, TotalAbsents
    # dataframe columns to df_trad
    ######################################################################
    for index, row in df_trad.iterrows():
        # get matching rows in df_5
        df_temp = df5[(df5['DFLT_ID'] == row['DFLT_ID'])].copy()

        num_As = (df_temp['ATND_ID'] == 'A').sum()
        num_Es = (df_temp['ATND_ID'] == 'E').sum()
        num_Ps = (df_temp['ATND_ID'] == 'P').sum()
        num_Vps = (df_temp['ATND_ID'] == 'VP').sum()
        num_Ts = (df_temp['ATND_ID'] == 'T').sum()
        num_Hs = (df_temp['ATND_ID'] == 'H').sum()
        num_Ccs = (df_temp['ATND_ID'] == 'CC').sum()
        num_Nas = (df_temp['ATND_ID'] == 'NA').sum()

        num_absents = num_As + num_Es
        num_total_recs = num_As + num_Es + num_Ps + num_Vps + num_Ts + num_Hs + num_Ccs + num_Nas

        # if index < 10:
        #     print(index)
        #     print(df_temp)
        #     print(num_As)
        #     print('')

        df_trad.loc[index,'TotalAs'] = num_As
        df_trad.loc[index,'TotalEs'] = num_Es
        df_trad.loc[index,'TotalPs'] = num_Ps
        df_trad.loc[index,'TotalVps'] = num_Vps
        df_trad.loc[index,'TotalTs'] = num_Ts
        df_trad.loc[index,'TotalHs'] = num_Hs
        df_trad.loc[index, 'TotalCcs'] = num_Ccs
        df_trad.loc[index, 'TotalNas'] = num_Nas

        df_trad.loc[index, 'TotalRecs'] = num_total_recs
        df_trad.loc[index, 'TotalAbsents'] = num_absents

    # Add df_trad['AbsentRatio'] dataframe column
    ######################################################################
    df_trad['AbsentPercentage'] = df_trad.apply(lambda row: models.calculate_absent_percentage_for_majors_datatable(row), axis=1)

    # clean-up df3 DataFrame datatypes
    ############################################################################
    df3['DFLT_ID'] = df3['DFLT_ID'].astype(str)
    df3['DFLT_ID'] = df3['DFLT_ID'].apply(lambda row: row.zfill(9))

    df3.rename(columns={"MIDTERMGRADE": "MidTermGrade", 'LETTER_GRADE_FIN': "FinalGrade"}, inplace=True)

    # build df4b (courses with meet codes dataset)
    ################################################
    cols_to_keep = ['DEPT_ID', 'CRSE_ID', 'SECT_ID', 'MEET_ID', 'MEET_DAYS', 'TIME_START', 'TIME_END', 'DATE_FIRST', 'DATE_END']

    df4b_temp = pd.merge(df4_p1, df4_p2[cols_to_keep], on=['DEPT_ID', 'CRSE_ID', 'SECT_ID'], how='left')
    df4b_temp.drop_duplicates(subset=['DEPT_ID', 'CRSE_ID', 'SECT_ID'], keep='first', inplace=True)
    df4b = df4b_temp.copy()
    # Rename df4b columns to match what is needed in the dash datatable #2
    new_col_names_dict = {"MEET_DAYS": "MeetDays", 'TIME_START': "TimeStart", 'TIME_END': "TimeEnd",
                          'DATE_FIRST': "DateFirst", 'DATE_END': "DateEnd"}
    df4b.rename(columns=new_col_names_dict, inplace=True)

    # clean-up df5 DataFrame datatypes
    ############################################################################
    df5['DFLT_ID'] = df5['DFLT_ID'].astype(str)
    df5['DFLT_ID'] = df5['DFLT_ID'].apply(lambda row: row.zfill(9))

    #TODO:
    #FIX
    ############################################################################
    # df5['ATND_DATE'] = df5['ATND_DATE'].dt.date

    # df5['ATND_DATE'] = pd.to_datetime(df5['ATND_DATE'], format='%Y-%m-%d')
    # df5['ATND_DATE'] = df5['ATND_DATE'].apply(format_attendance_date)
    # df5['ATND_DATE'] = df5['ATND_DATE'].apply(lambda row: format_attendance_date(row))

    # print('')
    # print(df3.columns)
    # print('')
    # print('')
    # print(df5.head(10))
    # print('')
    # print(df5['ATND_DATE'].apply(type))
    # print('')
    # print('')

    # print('df4 info')
    # print(df4.columns)
    # print('')
    # print(df4.head(10))
    # print('')
    # print('df6 info')
    # print(df6.columns)
    # print('')
    # print(df6.head(10))
    # print('')
    # # print(df5['ATND_DATE'].apply(type))
    # print('')
    # print('')

    # print('')
    # print('')
    # print(df_trad.columns)
    # print('')
    # print('')
    # print(df_trad.head())
    # print('')
    # print('')

    # print('')
    # print('')
    # print(df_cwm.columns)
    # print('')
    # print('')
    # print(df_cwm.head(10))
    # print('')
    # print('')

    # print('')
    # print('df_trad data types')
    # print(df_trad.dtypes)
    # print('')

    # print('')
    # print('df3 data types')
    # print(df3.dtypes)
    # # print(df3.columns)
    # print('')
    # print('')
    # print('')
    # print('df5 data types')
    # print(df5.dtypes)
    # # print(df3.head())
    # print('')
    # print('')

    # print('')
    # print('')
    # print(df4b.columns)
    # print('')
    # print('')
    # # print(df4b.head())
    # print('')
    # print('')

    # print('')
    # print('')
    # print(df5.columns)
    # print('')
    # print('')
    # print(df5.head())
    # print('')
    # print('')

    # package dataframes as json
    datasets = {
         'df_trad': df_trad.to_json(orient='split'),
         'df2': df2.to_json(orient='split'),
         'df3': df3.to_json(orient='split'),
         'df4b': df4b.to_json(orient='split'),
         # 'df4b': df4b.to_json(orient='split'),
         # 'df_cwm': df_cwm.to_json(orient='split'),
         'df5': df5.to_json(orient='split'),
    }

    return json.dumps(datasets)


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_dashboard_date_time_stamp(n):
    # print('inside update_dashboard_date_time_stamp!!!!')
    # print('')
    message = build_dashboard_last_updated_message()
    # print('')
    # print(message)
    # print('')

    return message


@app.callback(Output('majors-datatable', 'data'),
              [Input('dashboard-datasets', 'children'),])
def update_majors_datatable(json_data):

    # print('inside update_dashboard_datatable_1!!!!!!')
    # builds dash datatable output from the dashboard-datasets hidden div
    # builds the required fields/columns in df_trad dataset to display in the dash
    # datatable 1 output

    datasets = json.loads(json_data)
    df_trad = pd.read_json(datasets['df_trad'], orient='split')
    df2 = pd.read_json(datasets['df2'], orient='split')
    df5 = pd.read_json(datasets['df5'], orient='split')

    df_trad['DFLT_ID'] = df_trad['DFLT_ID'].astype(str)
    df_trad['DFLT_ID'] = df_trad['DFLT_ID'].apply(lambda row: row.zfill(9))

    # df_trad = df_trad_temp.copy()

    # diagnostic prints
    ###################################
    # print('')
    # print(df_trad.columns)
    # print('')
    # print(df_trad.info())
    # print('')
    # print('')
    # print(df)
    # print('')

    data_df = convert_dataframe_to_datatable_list(df_trad)

    # print(data_df)
    # print('')

    return data_df

#TODO - swap the implementation here to use derived_virtual_data and selected_rows????
######################################################################################
@app.callback(Output('courses-datatable', 'data'),
             [Input('dashboard-datasets', 'children'),
              Input('majors-datatable', 'selected_rows')])
def update_courses_data_table(json_data, selected_rows):
    #TODO - Add code for the hidden fields in the dash datatable #2
    # 1) DateFirst, DateEnd, MidTermGrade, FinalGrade
    #############################################################

    # print('Inside update_courses_data_table!!!!!!')
    # print('')

    json_not_empty = (json_data is not None)
    row_not_selected = (selected_rows is not None)

    # print('Inside store_courses_data_in_div!!!!!!')
    # result = []
    # print(selected_rows)
    # print('')

    if json_not_empty and row_not_selected:

        datasets = json.loads(json_data)
        df_majors = pd.read_json(datasets['df_trad'], orient='split')
        # df_courses is really the student-course enrollments dataset instead!
        df_courses = pd.read_json(datasets['df3'], orient='split')
        df5 = pd.read_json(datasets['df5'], orient='split')

        df4b = pd.read_json(datasets['df4b'], orient='split')

        # print('df4b columns!')
        # print(df4b.columns)
        # print('')
        # print('')
        # print('df4b sample data!')
        # print(df4b.head())
        # # print(df4b['DFLT_ID'].apply(type))
        # print('BEFORE:')
        # print(df4b['TIME_START'].apply(type))
        # print(df4b['TIME_END'].apply(type))
        # print('')
        # print('')

        # print('AFTER:')
        # print(df4b['TIME_START'].apply(type))
        # print(df4b['TIME_END'].apply(type))
        # print('')
        # print('')
        # print('df4b sample data!')
        # print(df4b.head())
        # print('')
        # print('')

        # print('df5 types!!!!!')
        # print(df5['DFLT_ID'].apply(type))
        # print(df5['CRSE_ID'].apply(type))
        # print('')
        # print('')

        # # convert type to a string!
        df_courses['DFLT_ID'] = df_courses['DFLT_ID'].astype(str)
        df_courses['DFLT_ID'] = df_courses['DFLT_ID'].apply(lambda row: row.zfill(9))

        df5['DFLT_ID'] = df5['DFLT_ID'].astype(str)
        df5['CRSE_ID'] = df5['CRSE_ID'].astype(str)

        df4b['TimeStart'] = pd.to_datetime(df4b['TimeStart']).dt.time
        df4b['TimeEnd'] = pd.to_datetime(df4b['TimeEnd']).dt.time

        df4b['DateFirst'] = pd.to_datetime(df4b['DateFirst']).dt.date
        df4b['DateEnd'] = pd.to_datetime(df4b['DateEnd']).dt.date

        # print('df5 types!!!!!')
        # print(df5['DFLT_ID'].apply(type))
        # print(df5['CRSE_ID'].apply(type))
        # print('')
        # print('')

        # print(df_majors.head())
        # print('df_courses sample data!')
        # print(df_courses.head())
        # print(df_courses['DFLT_ID'].apply(type))
        # print('')
        # print('')
        # print('')
        # majors_columns = df_majors.columns
        # courses_columns = df_courses.columns

        # print('')
        # print(majors_columns)
        # print('')
        # columns = df.columns

        #works!!!!
        ############################
        # print(df.head(10))
        # print('')
        # print('DF_MAJORS')
        # print(df_majors.columns)
        # print(df_majors.head())
        # print('')
        # print('')

        # print('')
        # print('DF_COURSES')
        # print(df_courses.columns)
        # print(df_courses.head())
        # print('')
        # print('')

        for i in selected_rows:
            student_id = df_majors.iloc[i, 1]
            student_id = str(student_id).zfill(9)

            # student_id = df.iloc[i, 9]

        #works!!!!
        ############################
        # print('BEFORE:')
        # print('student_id=', student_id)
        # print('type(student_id)=', type(student_id))
        # print('')
        # print('')

        if (student_id is not None) and (student_id is not ''):
            # student_id = str(student_id).zfill(9)

            df_out = df_courses[(df_courses['DFLT_ID'] == student_id)].copy()

            # print('df_out types!!!!!')
            # print(df_out['DFLT_ID'].apply(type))
            # print(df_out['DEPT_ID'].apply(type))
            # print(df_out['CRSE_ID'].apply(type))
            # print(df_out['SECT_ID'].apply(type))
            # print('')
            # print('')
            # print('df_out size!!!!!')
            # print(len(df_out.index))
            # print('')
            # print(df_out)
            # print('')
            # print('')

            # add additional fields for dashboard data table 2
            ##################################################

            # Add columns to df_out by walking df_5
            # NumA, NumE, NumP, NumT, NumH, NumRecs, NumAbsents, AbsentRatio
            ######################################################################
            for index, row in df_out.iterrows():
                # count up results for matching rows in df_5
                # match on dflt_id, dept_id, crse_id, sect_id
                condition = (df5['DFLT_ID'] == row['DFLT_ID']) & \
                            (df5['DEPT_ID'] == row['DEPT_ID']) & \
                            (df5['CRSE_ID'] == row['CRSE_ID']) & \
                            (df5['SECT_ID'] == row['SECT_ID'])

                df_temp = df5[condition].copy()
                # print('df_temp size!!!!!')
                # print(len(df_temp.index))
                # print('')
                # print(df_temp)
                # print('')
                # print('')

                num_As = (df_temp['ATND_ID'] == 'A').sum()
                num_Es = (df_temp['ATND_ID'] == 'E').sum()
                num_Ps = (df_temp['ATND_ID'] == 'P').sum()
                num_Vps = (df_temp['ATND_ID'] == 'VP').sum()
                num_Ts = (df_temp['ATND_ID'] == 'T').sum()
                num_Hs = (df_temp['ATND_ID'] == 'H').sum()
                num_Ccs = (df_temp['ATND_ID'] == 'CC').sum()
                num_Nas = (df_temp['ATND_ID'] == 'NA').sum()

                num_absents = num_As + num_Es
                num_total_recs = num_As + num_Es + num_Ps + num_Vps + num_Ts + num_Hs + num_Ccs + num_Nas

                # if index < 10:
                #     print(index)
                #     print(df_temp)
                #     print(num_As)
                #     print('')

                df_out.loc[index,'NumAs'] = num_As
                df_out.loc[index,'NumEs'] = num_Es
                df_out.loc[index,'NumPs'] = num_Ps
                df_out.loc[index,'NumVps'] = num_Vps
                df_out.loc[index,'NumTs'] = num_Ts
                df_out.loc[index,'NumHs'] = num_Hs
                df_out.loc[index, 'NumCcs'] = num_Ccs
                df_out.loc[index, 'NumNas'] = num_Nas

                df_out.loc[index, 'NumRecs'] = num_total_recs
                df_out.loc[index, 'NumAbsents'] = num_absents

            df_out['AbsentPercentage'] = df_out.apply(lambda row: models.calculate_absent_percentage_for_student_courses_datatable(row), axis=1)

            # Add columns to df_out by walking df4b
            # add code to lookup values from df4b dataset!
            # SESS_ID, DESCR_EXTENDED, INST_ID, SHORT_NAME, MeetDays
            ######################################################################
            for index, row in df_out.iterrows():

                condition = ((df4b['DEPT_ID'] == row['DEPT_ID']) & \
                            (df4b['CRSE_ID'] == row['CRSE_ID']) & \
                            (df4b['SECT_ID'] == row['SECT_ID']))

                df_temp = df4b[condition].copy()

                condition2 = ((df_temp['DEPT_ID'] == row['DEPT_ID']) & \
                             (df_temp['CRSE_ID'] == row['CRSE_ID']) & \
                             (df_temp['SECT_ID'] == row['SECT_ID']))

            #     # print(row['DEPT_ID'], row['CRSE_ID'], row['SECT_ID'])
            #     # print(sess_id)
            #     # print(descr_extended)
            #     # print(df_temp.SESS_ID)
            #     # print(df_temp.loc(,'SESS_ID'))
            #     # print('')
            #     # print('')
                df_out.loc[index, 'SESS_ID'] = df_temp.loc[condition2, 'SESS_ID'].values[0]
                df_out.loc[index, 'CRSE_CREDIT'] = df_temp.loc[condition2, 'CRSE_CREDIT'].values[0]
                df_out.loc[index, 'DESCR_EXTENDED'] = df_temp.loc[condition2, 'DESCR_EXTENDED'].values[0]
                df_out.loc[index, 'INST_ID'] = df_temp.loc[condition2, 'INST_ID'].values[0]
                df_out.loc[index, 'SHORT_NAME'] = df_temp.loc[condition2, 'SHORT_NAME'].values[0]
                df_out.loc[index, 'MeetDays'] = df_temp.loc[condition2, 'MeetDays'].values[0]
                df_out.loc[index, 'TimeStart'] = df_temp.loc[condition2, 'TimeStart'].values[0]
                df_out.loc[index, 'TimeEnd'] = df_temp.loc[condition2, 'TimeEnd'].values[0]
                df_out.loc[index, 'DateFirst'] = df_temp.loc[condition2, 'DateFirst'].values[0]
                df_out.loc[index, 'DateEnd'] = df_temp.loc[condition2, 'DateEnd'].values[0]

            # ######################################################################

        # print('df_courses dtypes!!!!')
        # print(df_courses.dtypes)
        # print('')
        # print('')

        # print('AFTER:')
        # print('student_id=', student_id)
        # print('type(student_id)=', type(student_id))
        # print('')
        # print('')

        # df_c = get_course_data(student_id, df, df.columns)
        # print('student_id=', student_id)
        # print('df_out COURSES!!')
        # print(df_out.columns)
        # print('')
        # print(df_out)
        # print('')
        #limit to a subset of columns during testing!
        # df_out = df_temp[courses_columns]
        # return df_out

        # print(df_out)
        # print('')
        # print('')

        data_df = convert_dataframe_to_datatable_list(df_out)

        return data_df


@app.callback(Output('attendance-detail-datatable', 'data'),
             [Input('dashboard-datasets', 'children'),
              Input('courses-datatable', 'derived_virtual_data'),
              Input('courses-datatable', 'derived_virtual_selected_rows')])
def update_attendance_detail_datatable(json_data, rows, derived_virtual_selected_rows):

    # print('Inside update_attendance_detail_datatable!!!!!')
    # print('')

    # if json_data is not None:
        # Read in attendance detail from json and store as a dataframe.
    datasets = json.loads(json_data)
    # df_courses = pd.read_json(datasets['df_courses'], orient='split')
    df_attendance_detail = pd.read_json(datasets['df5'], orient='split')

    # convert type to a string!
    df_attendance_detail['DFLT_ID'] = df_attendance_detail['DFLT_ID'].astype(str)
    df_attendance_detail['DFLT_ID'] = df_attendance_detail['DFLT_ID'].apply(lambda row: row.zfill(9))
    df_attendance_detail['CRSE_ID'] = df_attendance_detail['CRSE_ID'].astype(str)

    # df_attendance_detail['ATND_DATE'] = df_attendance_detail['ATND_DATE'].astype(str)
    # format = '%Y-%m-%dT%H:%M:%S.%fZ'
    # format = '%Y-%m-%dT%H:%M:%S'
    format = '%Y-%m-%d'
    df_attendance_detail['ATND_DATE'] = pd.to_datetime(df_attendance_detail['ATND_DATE'], format=format)

    # Add code to determine the day of week abbreviated from the attendance date
    df_attendance_detail['DayOfWeek'] = df_attendance_detail['ATND_DATE'].dt.dayofweek
    days = {0:'Mon', 1:'Tues', 2:'Wed', 3:'Thurs', 4:'Fri', 5:'Sat', 6:'Sun'}
    df_attendance_detail['DayOfWeek'] = df_attendance_detail['DayOfWeek'].apply(lambda x: days[x])

    df_attendance_detail['ATND_DATE'] = df_attendance_detail['ATND_DATE'].dt.date

    # print('Inside callback -- df_attendance_detail types!!!!!')
    # print(df_attendance_detail['DFLT_ID'].apply(type))
    # print(df_attendance_detail['DEPT_ID'].apply(type))
    # print(df_attendance_detail['CRSE_ID'].apply(type))
    # print(df_attendance_detail['SECT_ID'].apply(type))
    # print('')
    # print(df_attendance_detail['ATND_DATE'].apply(type))
    # print('')
    # print('')

    # print(df_attendance_detail.head())
    # print('')
    # print('')

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    df_student_courses = df if rows is None else pd.DataFrame(rows)

    # print(dff)
    # print('')
    # print('')

    # Get the index for the selected course
    for i in range(len(df_student_courses)):
        if i in derived_virtual_selected_rows:
            student_id = df_student_courses.DFLT_ID[i]
            dept_id = df_student_courses.DEPT_ID[i]
            crse_id = df_student_courses.CRSE_ID[i]
            sect_id = df_student_courses.SECT_ID[i]
            # print(student_id, dept_id, crse_id, sect_id)
            # print('type student_id = ', type(student_id))
            # print('type dept_id = ', type(dept_id))
            # print('type crse_id = ', type(crse_id))
            # print('type sect_id = ', type(sect_id))
            # print('')

    # print(student_id, dept_id, crse_id, sect_id)
    # df_result = get_attendance_detail_data(student_id, dept_id, crse_id, sect_id, df_attendance_detail)

    condition = ((df_attendance_detail['DFLT_ID'] == student_id) & \
                (df_attendance_detail['DEPT_ID'] == dept_id) & \
                (df_attendance_detail['CRSE_ID'] == crse_id) & \
                (df_attendance_detail['SECT_ID'] == sect_id))

    # temp conditions!!!!
    # condition = ( (df_attendance_detail['DEPT_ID'] == dept_id) )
    # condition = ( (df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['CRSE_ID'] == crse_id) & (df_attendance_detail['SECT_ID'] == sect_id))
    # condition = ( (df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['SECT_ID'] == sect_id))
    # print('condition = ', condition)
    # print('')
    # print('')
    # print('')
    # print('')

    # df_temp = df_attendance_detail[((df_attendance_detail['DFLT_ID'] == int(student_id)) & (df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['CRSE_ID'] == str(crse_id)) & (df_attendance_detail['SECT_ID'] == sect_id))]
    # df_temp = df_attendance_detail[((df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['CRSE_ID'] == int(crse_id)) & (df_attendance_detail['SECT_ID'] == sect_id))]
    df_temp = df_attendance_detail[condition]
    # print(df_temp)
    # print('')
    # print('')

    # TODO sort records by ATND_DATE in descending order?
    df_out = df_temp.sort_values('ATND_DATE', ascending=False)

    # print(df_temp)
    #limit to a subset of columns during testing!
    # df_out = df_temp[col_c]
    # return df_temp
    result = convert_dataframe_to_datatable_list(df_out)
    return result


# HELPER functions
###############################################################################
def convert_dataframe_to_datatable_list(df):

    result = []

    if df is not None:
        if len(df.index) > 0:
            result = list(df.to_dict(orient='records'))
    return result


def format_attendance_date(string_date):
    # created on 2019-09-05
    # reference = https://stackoverflow.com/questions/17594298/date-time-formats-in-python

    format = '%Y-%m-%dT%H:%M:%S'
    # format = '%Y-%m-%d'
    # format = '%Y-%m-%dT%H:%M:%S.%fZ'

    date_obj = datetime.datetime.strptime(string_date, format)
    # Force the leading zeros!
    month = str(date_obj.month).zfill(2)
    day = str(date_obj.day).zfill(2)
    result = f'{date_obj.year}-{month}-{day}'

    return result


def build_dashboard_last_updated_message():
    # created on 9/4/2019
    datetime_stamp = datetime.datetime.now()
    format = '%B %d, %Y - %I:%M %p'
    # Use %e to print day without the leading zero?
    # reference = https://stackoverflow.com/questions/904928/python-strftime-date-without-leading-0
    format = '%A, %B %e, %Y - %I:%M %p'
    formatted_datetime_stamp = datetime_stamp.strftime(format)
    # message = 'The data was last updated on {0}.'.format(datetime_stamp)
    return 'The data was last updated on {0}.'.format(formatted_datetime_stamp)
