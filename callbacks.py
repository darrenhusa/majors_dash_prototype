# callbacks.py

import pandas as pd
from dash.dependencies import Input, Output
from app import app

# global area - read in data from csv files
df_full = pd.read_csv('data/spring_2019_data1.csv')
teams = df_full['ActivityDesc'].unique()

col_a = ['ActivityDesc', 'StudentId', 'Lastname', 'Firstname', \
         'AorWStatus', 'ClassStatus', 'UndergradCrHrsEnrolled',\
         'TotalAs','TotalEs','TotalPs','TotalTs','TotalHs','TotalCcs', \
         'TotalRecs', 'TotalAbsents', 'AbsentRatio']

df_courses = pd.read_csv('data/spring_2019_data2.csv')

col_b = ['DfltId', 'LastName', 'FirstName', 'DeptId', 'CrseId', 'SectId', \
           'InstId', 'ShortName', 'MeetDays', 'TimeStart', 'TimeEnd', 'NumMeetDaysPerWeek', \
           'NumA','NumE','NumP','NumT','NumH','NumCc','Total', 'SeatTimeAbsent']

df_attendance_detail = pd.read_csv('data/spring_2019_data3.csv')

col_c = ['﻿TERM_ID', 'DEPT_ID', 'CRSE_ID', 'SECT_ID',
         'DFLT_ID', 'LAST_NAME', 'FIRST_NAME', 'ATND_DATE', 'ATND_ID', 'AttendDateWoTime', 'AttendDateMonth', 'AttendDateDay']

def build_team_dataframe(Team):
    if not (Team is None or Team is ''):
        filtered_df = df_full[df_full['ActivityDesc'] == Team]
    else:
        filtered_df = None
    return filtered_df

def get_course_data(student_id):
    # filter 2nd dataset
    df_temp = df_courses[df_courses['DfltId'] == student_id]
    # print(df_temp)
    #limit to a subset of columns during testing!
    df_out = df_temp[col_b]
    return df_out

# ﻿TERM_ID,DEPT_ID,CRSE_ID,SECT_ID,DFLT_ID,LAST_NAME,FIRST_NAME,ATND_DATE,ATND_ID,AttendDateWoTime,AttendDateMonth,AttendDateDay

def get_attendance_detail_data(student_id, dept_id, crse_id, sect_id):
    # print('inside get_attendance_detail_data')
    # print(student_id, dept_id, crse_id, sect_id)
    # print('')
    # print(df_attendance_detail.head())
    # print('')
    # print(df_attendance_detail.tail())
    # print('')

    # filter 3rd dataset
    # condition = ((df_attendance_detail['DFLT_ID'] == str(student_id)) & \
    #             (df_attendance_detail['DEPT_ID'] == dept_id) & \
    #             (df_attendance_detail['CRSE_ID'] == crse_id) & \
    #             (df_attendance_detail['SECT_ID'] == sect_id))

    # condition = ( (df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['CRSE_ID'] == crse_id) & (df_attendance_detail['SECT_ID'] == sect_id))
    # print('condition = ', condition)
    # print('')

    df_temp = df_attendance_detail[((df_attendance_detail['DFLT_ID'] == int(student_id)) & (df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['CRSE_ID'] == str(crse_id)) & (df_attendance_detail['SECT_ID'] == sect_id))]
    # df_temp = df_attendance_detail[((df_attendance_detail['DEPT_ID'] == dept_id) & (df_attendance_detail['CRSE_ID'] == int(crse_id)) & (df_attendance_detail['SECT_ID'] == sect_id))]
    # df_temp = df_attendance_detail[condition]
    # print(df_temp)

    # TODO sort records by ATND_DATE in descending order?
    df_out = df_temp.sort_values('ATND_DATE', ascending=False)

    # print(df_temp)
    #limit to a subset of columns during testing!
    # df_out = df_temp[col_c]
    return df_out


def convert_dataframe_to_datatable_list(df):

    result = []

    if df is not None:
        if len(df.index) > 0:
            result = list(df.to_dict(orient='records'))
    return result


@app.callback(Output('roster-data', 'children'), [Input('Team', 'value')])
def store_roster_data_in_div(Team):
    if not (Team is None or Team is ''):
        filtered_df = df_full[df_full['ActivityDesc'] == Team]

        filtered_df = filtered_df[col_a]
        return filtered_df.to_json(orient='split')

@app.callback(Output('roster-datatable', 'data'), [Input('roster-data', 'children')])
def update_roster_datatable(json_data):

    df = pd.read_json(json_data, orient='split')
    data_df = convert_dataframe_to_datatable_list(df)
    return data_df

@app.callback(Output('courses-data', 'children'),
             [Input('roster-data', 'children'),
              Input('roster-datatable', 'selected_rows')])
def store_courses_data_in_div(json_data, selected_rows):
    json_not_empty = (json_data is not None)
    row_not_selected = (selected_rows is not None)

    # result = []

    if json_not_empty and row_not_selected:
        dff = pd.read_json(json_data, orient='split')

        for i in selected_rows:
            student_id = dff.iloc[i, 1]

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

@app.callback(Output('attendance-detail-datatable', 'data'),
             [Input('courses-data', 'children'),
              Input('courses-datatable', 'selected_rows')])
def update_attendance_detail_datatable(json_data, selected_rows):

    json_not_empty = (json_data is not None)
    row_not_selected = (selected_rows is not None)

    result = []

    if json_not_empty and row_not_selected:
        dff = pd.read_json(json_data, orient='split')
        # print(dff)
        # print('')

        for i in selected_rows:
            student_id = dff.iloc[i, 0]
            dept_id = dff.iloc[i, 3]
            crse_id = dff.iloc[i, 4]
            sect_id = dff.iloc[i, 5]

        # print(student_id, dept_id, crse_id, sect_id)
        # print('')

        df = get_attendance_detail_data(student_id, dept_id, crse_id, sect_id)
        result = convert_dataframe_to_datatable_list(df)

    return result
