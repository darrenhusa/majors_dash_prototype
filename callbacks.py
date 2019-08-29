# callbacks.py

import pandas as pd
import pyodbc
from dash.dependencies import Input, Output

from app import app
import models

# global area - get live empower data
term = '20191'
empower = pyodbc.connect('DSN=EMPOWER')
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

#TODO -sort majors data by last, then first in ascending order
#DEBUG operation !!!!??????
# df_trad_majors_data.sort_values('LAST_NAME', ascending=True, inplace=True)
df_trad_majors_data.sort_values(['LAST_NAME', 'FIRST_NAME'], ascending=[True, True], inplace=True)

number_of_records = len(df_trad_majors_data.index)
# print('number of majors all records = ', number_of_records)
# print('')
# print('')
# print(df_trad_majors_data.head())
# print('')
# print('')

# print("Adding additional columns to df_majors_data dataset...")
df_trad_majors_data['FtPtStatus'] = df_trad_majors_data.apply(lambda row: models.create_ft_pt_status_from_undergrad_cr_hrs(row['TU_CREDIT_ENRL']), axis=1)
df_trad_majors_data['Programs'] = df_trad_majors_data.apply(lambda row: models.classify_empower_major_codes_into_programs(row['MAMI_ID_MJ1']), axis=1)
df_trad_majors_data['FirstMajorDesc'] = df_trad_majors_data.apply(lambda row: models.lookup_empower_major_description(empower, row['MAMI_ID_MJ1'], empty_result=''), axis=1)
df_trad_majors_data['Programs'] = df_trad_majors_data.apply(lambda row: models.classify_empower_major_codes_into_programs(row['MAMI_ID_MJ1']), axis=1)
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
df_trad_majors_data['AttendPercentage'] = df_trad_majors_data.apply(lambda row: models.calculate_total_attend_percentage(row), axis=1)

col_a = list(df_trad_majors_data.columns)
# 'TERM_ID', 'DFLT_ID', 'LAST_NAME', 'FIRST_NAME', 'STUD_STATUS', 'CDIV_ID', 'ETYP_ID', 'PRGM_ID1', 'MAMI_ID_MJ1', 'TU_CREDIT_ENRL', 'TG_CREDIT_ENRL', 'College', 'Programs'
programs = df_trad_majors_data['Programs'].unique()
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

col_c = ['﻿TERM_ID', 'DEPT_ID', 'CRSE_ID', 'SECT_ID',
         'DFLT_ID', 'LAST_NAME', 'FIRST_NAME', 'ATND_DATE', 'ATND_ID', 'AttendDateWoTime', 'AttendDateMonth', 'AttendDateDay']

def build_programs_dataframe(Program):
    if not (Program is None or Program is ''):
        filtered_df = df_trad_majors_data[df_trad_majors_data['Programs'] == Program]
    else:
        filtered_df = None
    print(filtered_df.head())
    print('')
    return filtered_df

def get_course_data(student_id):

    # print('Inside get_course_data!!!!!')
    # print('student_id=', student_id)
    # print('')

    # print(df_courses.head())
    # print('')
    # print('')
    # print('')

    # filter 2nd dataset
    df_temp = df_courses[df_courses['DFLT_ID'] == str(student_id)]
    # print('student_id=', student_id)
    # print(df_temp)
    # print('')
    #limit to a subset of columns during testing!
    df_out = df_temp[col_b]
    return df_out

# ﻿TERM_ID,DEPT_ID,CRSE_ID,SECT_ID,DFLT_ID,LAST_NAME,FIRST_NAME,ATND_DATE,ATND_ID,AttendDateWoTime,AttendDateMonth,AttendDateDay

# def get_attendance_detail_data(student_id, dept_id, crse_id, sect_id):
#     # print('inside get_attendance_detail_data')
#     # print(student_id, dept_id, crse_id, sect_id)
#     # print('')
#     # print(df_attendance_detail.head())
#     # print('')
#     # print(df_attendance_detail.tail())
#     # print('')
#
#     # filter 3rd dataset
#     # condition = ((df_attendance_detail['DFLT_ID'] == str(student_id)) & \
#     #             (df_attendance_detail['DEPT_ID'] == dept_id) & \
#     #             (df_attendance_detail['CRSE_ID'] == crse_id) & \
#     #             (df_attendance_detail['SECT_ID'] == sect_id))
#
#     # condition = ( (df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['CRSE_ID'] == crse_id) & (df_attendance_detail['SECT_ID'] == sect_id))
#     # print('condition = ', condition)
#     # print('')
#
#     df_temp = df_attendance_detail[((df_attendance_detail['DFLT_ID'] == int(student_id)) & (df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['CRSE_ID'] == str(crse_id)) & (df_attendance_detail['SECT_ID'] == sect_id))]
#     # df_temp = df_attendance_detail[((df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['CRSE_ID'] == int(crse_id)) & (df_attendance_detail['SECT_ID'] == sect_id))]
#     # df_temp = df_attendance_detail[condition]
#     # print(df_temp)
#
#     # TODO sort records by ATND_DATE in descending order?
#     df_out = df_temp.sort_values('ATND_DATE', ascending=False)
#
#     # print(df_temp)
#     #limit to a subset of columns during testing!
#     # df_out = df_temp[col_c]
#     return df_out


def convert_dataframe_to_datatable_list(df):

    result = []

    if df is not None:
        if len(df.index) > 0:
            result = list(df.to_dict(orient='records'))
    return result


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
    json_not_empty = (json_data is not None)
    row_not_selected = (selected_rows is not None)

    # print('Inside store_courses_data_in_div!!!!!!')
    # result = []
    print(selected_rows)
    print('')

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

# @app.callback(Output('attendance-detail-datatable', 'data'),
#              [Input('courses-data', 'children'),
#               Input('courses-datatable', 'selected_rows')])
# def update_attendance_detail_datatable(json_data, selected_rows):
#
#     json_not_empty = (json_data is not None)
#     row_not_selected = (selected_rows is not None)
#
#     result = []
#
#     if json_not_empty and row_not_selected:
#         dff = pd.read_json(json_data, orient='split')
#         # print(dff)
#         # print('')
#
#         for i in selected_rows:
#             student_id = dff.iloc[i, 0]
#             dept_id = dff.iloc[i, 3]
#             crse_id = dff.iloc[i, 4]
#             sect_id = dff.iloc[i, 5]
#
#         # print(student_id, dept_id, crse_id, sect_id)
#         # print('')
#
#         df = get_attendance_detail_data(student_id, dept_id, crse_id, sect_id)
#         result = convert_dataframe_to_datatable_list(df)
#
#     return result
