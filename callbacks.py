# callbacks.py

import pandas as pd
import pyodbc
import datetime

import dash_html_components as html
from dash.dependencies import Input, Output
import yaml

from app import app
import models


# def process_crse_id_field_for_attendance_detail_datatable(crse_id):
#     # created on 9/3/2019
#
#     if models.isBlank(crse_id):
#         return None
#
#     # result = ''
#     # test for numbers < 100, add a leading zero and convert to a string type
#     # Note: int(115L) throws a 'ValueError since cannot convert to an integer type'
#     try:
#         if int(crse_id) < 100:
#             # Add a leading zero and make the results a string
#             result = f'0{crse_id}'
#         else:
#             result = str(crse_id)
#
#     except ValueError:
#         result = str(crse_id)
#
#     return result


# def process_dlft_id_field(student_id):
#     # created on 9/03/2019
#
#     length = len(str(student_id))
#
#     if length  < 9:
#         # found a DFLT_ID that needs fixing!
#         print('student_id = ', student_id)
#         print('')
#         print('')
#
#         result = ''
#         difference = 9 - length
#
#         while difference > 0:
#             result += '0'
#             difference -= 1
#
#         result += str(student_id)
#         # print(result)
#         # print('')
#         # print('')
#         # print('')
#
#     # elif length == 9:
#     else:
#         # verify that the result is a string type!
#         result = str(student_id)
#
#     return result


# load app configuration!
config = yaml.safe_load(open("configuration.yaml", 'r'))

# for key, value in config.items():
#     print (key + " : " + str(value))

# global area - get live empower data
term = config['TERM']
update_interval_in_minutes = config['UPDATE_INTERVAL_IN_MINUTES']
# empower = pyodbc.connect(dsn='EMPOWER')
empower = pyodbc.connect(dsn=config['DSN'])

# print("term = ", config['TERM'])
# print("dsn = ", config['DSN'])
# print('')

df_majors_data_all = models.build_majors_data_dataset(empower, term)
# print(df_majors_data_all.head())
# print('')

# number_of_records = len(df_majors_data_all.index)
df_majors_data_all['College'] = df_majors_data_all.apply(lambda row: models.create_college_from_prgm_id1(row['PRGM_ID1']), axis=1)

# print('number of majors all records = ', number_of_records)
# print('')

# filter down to trad majors only
# print('Limit to College == TRAD records only!')
df_trad_majors_data = df_majors_data_all[(df_majors_data_all['College'] == 'TRAD')].copy()

# Need to clean-up the DFLT_ID if the length is less than 9
# df_trad_majors_data['DFLT_ID'] = df_trad_majors_data.apply(lambda row: process_dlft_id_field(row['DFLT_ID']), axis=1)
# df_trad_majors_data['DFLT_ID'] = df_trad_majors_data['DFLT_ID'].str.zfill(9)
# df_trad_majors_data['DFLT_ID'] = df_trad_majors_data['DFLT_ID'].str.zfill(9)

# df_trad_majors_data['DFLT_ID'] = df_trad_majors_data['DFLT_ID'].map(lambda x: f'{x:0>9}')
# df_trad_majors_data['DFLT_ID'] = df_trad_majors_data['DFLT_ID'].astype(str).str.zfill(9)

# df['ID'].astype(str).str.zfill(15)
#TODO -sort majors data by last, then first in ascending order
#DEBUG operation !!!!??????
# df_trad_majors_data.sort_values('LAST_NAME', ascending=True, inplace=True)
df_trad_majors_data.sort_values(['LAST_NAME', 'FIRST_NAME'], ascending=[True, True], inplace=True)

# number_of_records = len(df_trad_majors_data.index)

# print('df_trad_majors_data DTYPES:')
# print(df_trad_majors_data.dtypes)
# print('')
# print('')

# print('number of majors all records = ', number_of_records)
# print('')
# print('')
# print(df_trad_majors_data.head())
# print('')
# print('')

# print("Adding additional columns to df_majors_data dataset...")
df_trad_majors_data['FtPtStatus'] = df_trad_majors_data.apply(lambda row: models.create_ft_pt_status_from_undergrad_cr_hrs(row['TU_CREDIT_ENRL']), axis=1)
df_trad_majors_data['Programs'] = df_trad_majors_data.apply(lambda row: models.lookup_academic_program(row['MAMI_ID_MJ1'], config['Programs']), axis=1)
# df_trad_majors_data['Programs'] = df_trad_majors_data.apply(lambda row: models.classify_empower_major_codes_into_programs(row['MAMI_ID_MJ1']), axis=1)
df_trad_majors_data['FirstMajorDesc'] = df_trad_majors_data.apply(lambda row: models.lookup_empower_major_description(empower, row['MAMI_ID_MJ1'], empty_result=''), axis=1)
# df_trad_majors_data['Programs'] = df_trad_majors_data.apply(lambda row: models.classify_empower_major_codes_into_programs(row['MAMI_ID_MJ1']), axis=1)
df_trad_majors_data['NumCcsjSports'] = df_trad_majors_data.apply(lambda row: models.determine_number_of_athlete_records_in_sr_activities(empower, row['DFLT_ID'], term), axis=1)
df_trad_majors_data['IsAthlete'] = df_trad_majors_data.apply(lambda row: models.determine_is_athlete_status(row['NumCcsjSports']), axis=1)
df_trad_majors_data['AthleticTeamCodes'] = df_trad_majors_data.apply(lambda row: models.get_empower_sr_activity_data_for_student_for_term(empower, term, row['DFLT_ID']), axis=1)
df_trad_majors_data['TotalAs'] = df_trad_majors_data.apply(lambda row: models.calculate_total_empower_attendance_records_in_term_by_student_by_code(empower, row['TERM_ID'], row['DFLT_ID'], "A"), axis=1)
df_trad_majors_data['TotalEs'] = df_trad_majors_data.apply(lambda row: models.calculate_total_empower_attendance_records_in_term_by_student_by_code(empower, row['TERM_ID'], row['DFLT_ID'], "E"), axis=1)
df_trad_majors_data['TotalPs'] = df_trad_majors_data.apply(lambda row: models.calculate_total_empower_attendance_records_in_term_by_student_by_code(empower, row['TERM_ID'], row['DFLT_ID'], "P"), axis=1)
df_trad_majors_data['TotalTs'] = df_trad_majors_data.apply(lambda row: models.calculate_total_empower_attendance_records_in_term_by_student_by_code(empower, row['TERM_ID'], row['DFLT_ID'], "T"), axis=1)
df_trad_majors_data['TotalHs'] = df_trad_majors_data.apply(lambda row: models.calculate_total_empower_attendance_records_in_term_by_student_by_code(empower, row['TERM_ID'], row['DFLT_ID'], "H"), axis=1)
df_trad_majors_data['TotalCcs'] = df_trad_majors_data.apply(lambda row: models.calculate_total_empower_attendance_records_in_term_by_student_by_code(empower, row['TERM_ID'], row['DFLT_ID'], "CC"), axis=1)
df_trad_majors_data['TotalRecs'] = df_trad_majors_data.apply(lambda row: models.calculate_total_attendance_records(row), axis=1)
df_trad_majors_data['TotalAbsents'] = df_trad_majors_data.apply(lambda row: models.calculate_total_absents_records(row), axis=1)
# df_trad_majors_data['AttendPercentage'] = df_trad_majors_data.apply(lambda row: models.calculate_total_attend_percentage(row), axis=1)
df_trad_majors_data['AbsentRatio'] = df_trad_majors_data.apply(lambda row: models.calculate_absent_ratio_for_majors_datatable(row), axis=1)

col_a = list(df_trad_majors_data.columns)
# 'TERM_ID', 'DFLT_ID', 'LAST_NAME', 'FIRST_NAME', 'STUD_STATUS', 'CDIV_ID', 'ETYP_ID', 'PRGM_ID1', 'MAMI_ID_MJ1', 'TU_CREDIT_ENRL', 'TG_CREDIT_ENRL', 'College', 'Programs'
# programs = df_trad_majors_data['Programs'].unique().sort_values()
programs = df_trad_majors_data['Programs'].sort_values().unique()
# print(programs)
# print(col_a)
# print('')

# number_of_records = len(df_trad_majors_data.index)
# print('number_of trad majors records = ', number_of_records)
# print('')

# df_full = pd.read_csv('data/spring_2019_data1.csv')
# teams = df_full['ActivityDesc'].unique()

# col_a = ['ActivityDesc', 'StudentId', 'Lastname', 'Firstname', \
#          'AorWStatus', 'ClassStatus', 'UndergradCrHrsEnrolled',\
#          'TotalAs','TotalEs','TotalPs','TotalTs','TotalHs','TotalCcs', \
#          'TotalRecs', 'TotalAbsents', 'AbsentRatio']

# df_courses = pd.read_csv('data/spring_2019_data2.csv')
df_courses_temp = models.build_courses_data_dataset(empower, term)

# number_of_records = len(df_courses_temp.index)
# print('number_of df_courses_temp records = ', number_of_records)
# print('')

# Remove any MTI courses from the data!
df_courses = df_courses_temp[df_courses_temp['DEPT_ID'] != 'MTI'].copy()

# print('df_courses DTYPES:')
# print(df_courses.dtypes)
# print('')
# print('')

# clean-up the CRSE_ID field
# works???
# df_courses['CRSE_ID_ALT'] = df_courses.apply(lambda row: process_crse_id_field_for_attendance_detail_datatable(row['CRSE_ID']), axis=1)
# doesn't work????
# df_courses['CRSE_ID'] = df_courses.apply(lambda row: process_crse_id_field_for_attendance_detail_datatable(row['CRSE_ID']), axis=1)

# number_of_records = len(df_courses.index)
# print('number_of df_courses records = ', number_of_records)
# print('')
# print('')
# print('')

# print(df_courses.head())
# print(df_courses.columns)
# print('')

# print("Adding additional columns to df_courses dataset...")
df_courses['MeetDays'] = df_courses.apply(lambda row: models.lookup_course_meet_details(empower, row['TERM_ID'], row['DEPT_ID'], row['CRSE_ID'], row['SECT_ID'])[0], axis=1)
df_courses['TimeStart'] = df_courses.apply(lambda row: models.lookup_course_meet_details(empower, row['TERM_ID'], row['DEPT_ID'], row['CRSE_ID'], row['SECT_ID'])[1], axis=1)
df_courses['TimeEnd'] = df_courses.apply(lambda row: models.lookup_course_meet_details(empower, row['TERM_ID'], row['DEPT_ID'], row['CRSE_ID'], row['SECT_ID'])[2], axis=1)
df_courses['DateFirst'] = df_courses.apply(lambda row: models.lookup_course_meet_details(empower, row['TERM_ID'], row['DEPT_ID'], row['CRSE_ID'], row['SECT_ID'])[3], axis=1)
df_courses['DateEnd'] = df_courses.apply(lambda row: models.lookup_course_meet_details(empower, row['TERM_ID'], row['DEPT_ID'], row['CRSE_ID'], row['SECT_ID'])[4], axis=1)

df_courses['NumA'] = df_courses.apply(lambda row: models.get_empower_student_attendance_in_course(empower,
                                     row['TERM_ID'], row['DEPT_ID'], row['CRSE_ID'], row['SECT_ID'], row['DFLT_ID'], 'A'), axis=1)

df_courses['NumE'] = df_courses.apply(lambda row: models.get_empower_student_attendance_in_course(empower,
                                     row['TERM_ID'], row['DEPT_ID'], row['CRSE_ID'], row['SECT_ID'], row['DFLT_ID'], 'E'), axis=1)
df_courses['NumT'] = df_courses.apply(lambda row: models.get_empower_student_attendance_in_course(empower,
                                     row['TERM_ID'], row['DEPT_ID'], row['CRSE_ID'], row['SECT_ID'], row['DFLT_ID'], 'T'), axis=1)
df_courses['NumP'] = df_courses.apply(lambda row: models.get_empower_student_attendance_in_course(empower,
                                     row['TERM_ID'], row['DEPT_ID'], row['CRSE_ID'], row['SECT_ID'], row['DFLT_ID'], 'P'), axis=1)
df_courses['NumH'] = df_courses.apply(lambda row: models.get_empower_student_attendance_in_course(empower,
                                     row['TERM_ID'], row['DEPT_ID'], row['CRSE_ID'], row['SECT_ID'], row['DFLT_ID'], 'H'), axis=1)
df_courses['NumCc'] = df_courses.apply(lambda row: models.get_empower_student_attendance_in_course(empower,
                                     row['TERM_ID'], row['DEPT_ID'], row['CRSE_ID'], row['SECT_ID'], row['DFLT_ID'], 'CC'), axis=1)

df_courses['NumRecs'] = df_courses.apply(lambda row: models.calculate_total_attendance_records_for_courses_datatable(row), axis=1)
df_courses['NumAbsents'] = df_courses.apply(lambda row: models.calculate_total_absents_records_for_courses_datatable(row), axis=1)
# df_courses['AttendPercentage'] = df_courses.apply(lambda row: models.calculate_total_attend_percentage_for_courses_datatable(row), axis=1)
df_courses['AbsentRatio'] = df_courses.apply(lambda row: models.calculate_absent_ratio_for_courses_datatable(row), axis=1)

# df_courses['NumMeetDaysPerWeek'] =
# df_courses['SeatTimeAbsent'] =
# print(df_courses.columns)
# print('')
# print('')

#works!!!!
############################
# print(df_courses.head())
# print('')
# print('')

# TERM_ID CRST_ID SESS_ID DEPT_ID CRSE_ID
# SECT_ID DESCR_EXTENDED INST_ID SHORT_NAME	DFLT_ID
# LAST_NAME	FIRST_NAME	WDRAW_GRADE_FLAG
col_b = list(df_courses.columns)
#works!!!!
############################
# print(col_b)
# print('')

# col_b = ['TERM_ID', 'CRST_ID', 'SESS_ID', 'DEPT_ID', 'CRSE_ID',
#          'SECT_ID', 'DESCR_EXTENDED', 'INST_ID', 'SHORT_NAME',	'DFLT_ID',
#          'LAST_NAME', 'FIRST_NAME',	'WDRAW_GRADE_FLAG']

# col_b = ['DfltId', 'LastName', 'FirstName', 'DeptId', 'CrseId', 'SectId', \
#            'InstId', 'ShortName',
#            'MeetDays', 'TimeStart', 'TimeEnd', 'NumMeetDaysPerWeek', \
#            'NumA','NumE','NumP','NumT','NumH','NumCc','Total', 'SeatTimeAbsent']

# df_attendance_detail = pd.read_csv('data/spring_2019_data3.csv')
df_attendance_detail = models.build_attendance_detail_data_dataset(empower, term)

# print('DF DATA TYPES- before')
# print(df_attendance_detail.dtypes)
# print('')

# print('df_attendance_detail DTYPES - BEFORE:')
# print(df_attendance_detail.dtypes)
# print('')
# print('')

# print('DF DATA TYPES- after')
#DEBUG - this does not work!!!!!!!
#################################
# using apply method
# NOTE: course numbers can have letters --> need to use string type!!!
df_attendance_detail[['DFLT_ID']] = df_attendance_detail[['DFLT_ID']].astype(str)

# Need to handle cases like EWPC 096 --> currently showing as EWPC 96 and returning no attendance detail records!!
# df_attendance_detail[['CRSE_ID']] = df_attendance_detail[['CRSE_ID']].astype(str)
# df_attendance_detail['CRSE_ID'] = df_attendance_detail.apply(lambda row: process_crse_id_field_for_attendance_detail_datatable(row['CRSE_ID']), axis=1)

df_attendance_detail['ATND_DATE'] = df_attendance_detail.apply(lambda row: models.remove_time_from_datetime_object(row['ATND_DATE']), axis=1)

# print('df_attendance_detail DTYPES - AFTER:')
# print(df_attendance_detail.dtypes)
# print('')
# print('')

# df_attendance_detail[['DFLT_ID', 'CRSE_ID']] = df_attendance_detail[['DFLT_ID', 'CRSE_ID']].apply(pd.to_numeric)
# print(df_attendance_detail.dtypes)
# print('')

#works!!!!
############################
# print(df_attendance_detail.head())
# print(df_attendance_detail.columns)
# print('')
# print('')

# col_c = ['﻿TERM_ID', 'DEPT_ID', 'CRSE_ID', 'SECT_ID',
#          'DFLT_ID', 'LAST_NAME', 'FIRST_NAME', 'ATND_DATE', 'ATND_ID', 'AttendDateWoTime', 'AttendDateMonth', 'AttendDateDay']

col_c = list(df_attendance_detail.columns)

def build_programs_dataframe(Program):
    if not (Program is None or Program is ''):
        filtered_df = df_trad_majors_data[df_trad_majors_data['Programs'] == Program]
    else:
        # filtered_df = df_trad_majors_data
        filtered_df = None
    # print(filtered_df.head())
    # print('')
    return filtered_df

def get_course_data(student_id):

    # print('Inside get_course_data!!!!!')
    # print('BEFORE:')
    # print('student_id = ', student_id)
    # print('type(student_id) = ', type(student_id))
    # print('')

    # convert int to a string a pad with leading zeros.
    student_id = str(student_id).zfill(9)

    # print('AFTER:')
    # print('student_id = ', student_id)
    # print('type(student_id) = ', type(student_id))
    # print('')

    # print('student_id=', student_id)
    # print('')

    # print(df_courses.head())
    # print('')
    # print('')
    # print('')

    # filter 2nd dataset
    # df_temp = df_courses[df_courses['DFLT_ID'] == str(student_id)]
    df_temp = df_courses[(df_courses['DFLT_ID'] == student_id)]
    # print('student_id=', student_id)
    # print(df_temp)
    # print('')
    #limit to a subset of columns during testing!
    df_out = df_temp[col_b]
    return df_out

# ﻿TERM_ID,DEPT_ID,CRSE_ID,SECT_ID,DFLT_ID,LAST_NAME,FIRST_NAME,ATND_DATE,ATND_ID,AttendDateWoTime,AttendDateMonth,AttendDateDay

def get_attendance_detail_data(student_id, dept_id, crse_id, sect_id):
    #works!!!!!
    ############################################
    # print('inside get_attendance_detail_data')

    # print('BEFORE:')
    # print('student_id = ', student_id)
    # print('type(student_id) = ', type(student_id))
    # print('')
    # print('crse_id = ', crse_id)
    # print('type(crse_id) = ', type(crse_id))
    # print('')

    #convert student_id int to a string and pad with leading zeros
    #convert crse_id int to a string
    student_id = str(student_id).zfill(9)
    crse_id = str(crse_id)

    # convert input crse_id so that has a leading zero so matches the atendance detail data format?
    # try:
    #     if int(crse_id) < 100:
    #         # print('Found crse_id less than 100 case!!!')
    #         crse_id = f'0{crse_id}'
    #         # print('crse_id = ', crse_id)
    #     else:
    #         crse_id = str(crse_id)
    #
    # except ValueError:
    #     crse_id = str(crse_id)

    # print('AFTER:')
    # print('student_id = ', student_id)
    # print('type(student_id) = ', type(student_id))
    # print('')
    # print('crse_id = ', crse_id)
    # print('type(crse_id) = ', type(crse_id))
    # print('')

    # print(student_id, dept_id, crse_id, sect_id)
    # print('')
    # print(df_attendance_detail.head())
    # print('')
    # print(df_attendance_detail.tail())

    # print('Input data-types')
    # print('type(student_id) = ', type(student_id))
    # print('type(crse_id_id) = ', type(crse_id))
    # print('')
    # print('DF DATA TYPES- before')
    # print(df_attendance_detail.dtypes)
    # print('')

    # print('DF DATA TYPES- after')
    #DEBUG - this does not work!!!!!!!
    #################################
    # using apply method
    # df_attendance_detail[['DFLT_ID', 'CRSE_ID']] = df_attendance_detail[['DFLT_ID', 'CRSE_ID']].apply(pd.to_numeric)
    # print(df_attendance_detail.dtypes)

    # filter 3rd dataset
    condition = ((df_attendance_detail['DFLT_ID'] == student_id) & \
                (df_attendance_detail['DEPT_ID'] == dept_id) & \
                (df_attendance_detail['CRSE_ID'] == crse_id) & \
                (df_attendance_detail['SECT_ID'] == sect_id))

    # temp conditions!!!!
    # condition = ( (df_attendance_detail['DEPT_ID'] == dept_id) )
    # condition = ( (df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['CRSE_ID'] == int(crse_id)) & (df_attendance_detail['SECT_ID'] == sect_id))
    # condition = ( (df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['SECT_ID'] == sect_id))
    # print('condition = ', condition)
    # print('')

    # df_temp = df_attendance_detail[((df_attendance_detail['DFLT_ID'] == int(student_id)) & (df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['CRSE_ID'] == str(crse_id)) & (df_attendance_detail['SECT_ID'] == sect_id))]
    # df_temp = df_attendance_detail[((df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['CRSE_ID'] == int(crse_id)) & (df_attendance_detail['SECT_ID'] == sect_id))]
    df_temp = df_attendance_detail[condition]
    # print(df_temp)

    # TODO sort records by ATND_DATE in descending order?
    df_out = df_temp.sort_values('ATND_DATE', ascending=False)

    # print(df_temp)
    #limit to a subset of columns during testing!
    # df_out = df_temp[col_c]
    # return df_temp
    return df_out


def convert_dataframe_to_datatable_list(df):

    result = []

    if df is not None:
        if len(df.index) > 0:
            result = list(df.to_dict(orient='records'))
    return result

@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def reload_empower_data(n):
    print('inside reload_empower_data!!!!')
    # print('')
    datetime_stamp = datetime.datetime.now()
    format = '%B %d, %Y - %I:%M %p'
    formatted_datetime_stamp = datetime_stamp.strftime(format)
    # message = 'The data was last updated on {0}.'.format(datetime_stamp)
    message = 'The data was last updated on {0}.'.format(formatted_datetime_stamp)
    print(message)

    return html.H5(message)


@app.callback(Output('majors-data', 'children'), [Input('Program', 'value')])
def store_majors_data_in_div(Program):
    #works!!!!
    ############################
    # print(Program)
    # print('')
    # filtered_df = []
    if not (Program is None or Program is ''):
        filtered_df = df_trad_majors_data[df_trad_majors_data['Programs'] == Program]
        #works!!!!
        ############################
        # print(filtered_df.head())
        # print('')
        filtered_df = filtered_df[col_a]
        json_data = filtered_df.to_json(orient='split')
        # json_data = filtered_df.to_json(orient='split')
        #works!!!!
        ############################
        # print('json_data = ', json_data)
        # print('')
        return json_data

@app.callback(Output('majors-datatable', 'data'), [Input('majors-data', 'children')])
def update_majors_datatable(json_data):

    df = pd.read_json(json_data, orient='split')

    # print('Inside update_majors_datatable!!!!!!')
    #works!!!!
    ############################
    # print(df.head())
    # print('')

    data_df = convert_dataframe_to_datatable_list(df)

    #works!!!!
    ############################
    # print(data_df)
    # print('')

    return data_df

@app.callback(Output('courses-data', 'children'),
             [Input('majors-data', 'children'),
              Input('majors-datatable', 'selected_rows')])
def store_courses_data_in_div(json_data, selected_rows):
    # print('Inside store_courses_data_in_div')
    # print('')

    json_not_empty = (json_data is not None)
    row_not_selected = (selected_rows is not None)

    # print('Inside store_courses_data_in_div!!!!!!')
    # result = []
    # print(selected_rows)
    # print('')

    if json_not_empty and row_not_selected:
        dff = pd.read_json(json_data, orient='split')
        #works!!!!
        ############################
        # print(dff)
        # print('')
        for i in selected_rows:
            student_id = dff.iloc[i, 1]

        #works!!!!
        ############################
        # print('student_id=', student_id)
        # print('')

        df_c = get_course_data(student_id)

    #convert to json
    return df_c.to_json(orient='split')
    # return result


@app.callback(Output('courses-datatable', 'data'),
             [Input('courses-data', 'children')])
def update_courses_datatable(json_data):

    # print('Inside update_courses_datatable!!!!')
    # print('')

    json_not_empty = (json_data is not None)
    # row_not_selected = (selected_rows is not None)

    result = []

    if json_not_empty:
        dff = pd.read_json(json_data, orient='split')

        # for i in selected_rows:
        #     student_id = dff.iloc[i, 1]
        #
        # df_c = get_course_data(student_id)
        result = convert_dataframe_to_datatable_list(dff)

    return result

# DfltId,LastName,FirstName,FiOfLastName,FiOfFirstName,FullName,
# CdivId,PrgmId1,College,FirstMajor,1stMajorDescAndCode,NumCcsjSports,IsAthlete,AthleticTeamCodes,
# HasAttendanceData,SessionId,SessionDesc,
# TermId,DeptId,CrseId,SectId,IsGenEd,InstId,ShortName,MeetDays,TimeStart,TimeEnd,MidtermGrade,FinalGrade,NumMeetDaysPerWeek,NumA,NumE,NumH,NumCc,NumP,NumT,Total,SeatTimeAbsent,NeverAttended,AGtP,GtE9,UnexcusedAbsent,AbsentRanges,Present,PresentRanges

@app.callback(Output('attendance-detail-datatable', 'data'),
             [Input('courses-data', 'children'),
              Input('courses-datatable', 'selected_rows')])
def update_attendance_detail_datatable(json_data, selected_rows):

    # print('Inside update_attendance_detail_datatable!!!!!')
    # print('')

    json_not_empty = (json_data is not None)
    row_not_selected = (selected_rows is not None)

    result = []

    if json_not_empty and row_not_selected:
        # Note dff is the attendance_detail data!
        dff = pd.read_json(json_data, orient='split')
        # print(dff)
        # print(dff.columns)
        # print('')
        # print('')

        for i in selected_rows:
            student_id = dff.iloc[i, 9]
            dept_id = dff.iloc[i, 3]
            crse_id = dff.iloc[i, 4]
            sect_id = dff.iloc[i, 5]

        # print(student_id, dept_id, crse_id, sect_id)
        # print('')

        df = get_attendance_detail_data(student_id, dept_id, crse_id, sect_id)
        result = convert_dataframe_to_datatable_list(df)

    return result
