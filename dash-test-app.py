# dash-test-app.py
# usage: python dash-test-app.py
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html

# ﻿TermId,ActivityCode,ActivityDesc,Team,TrnscrptNotes,AthleticFlag,AorWStatus,StudentId,Lastname,Firstname,ClassStatus,UndergradCrHrsEnrolled,IsNaiaEligible,TotalAs,TotalEs,TotalPs,TotalTs,TotalHs,TotalCcs,TotalRecs,TotalAbsents,AbsentRatio,NumMidtermGrades,NumDfwiMidtermGrades,MidtermAtRiskRatio
df_full = pd.read_csv('spring_2019_data1.csv')
# print(df_full.head())
teams = df_full['ActivityDesc'].unique()

col_a_1 = ['ActivityDesc', 'StudentId', 'Lastname', 'Firstname']
col_a_hidden = ['AorWStatus', 'ClassStatus', 'UndergradCrHrsEnrolled',\
                'TotalAs','TotalEs','TotalPs','TotalTs','TotalHs','TotalCcs']
col_a_2 = ['TotalRecs', 'TotalAbsents', 'AbsentRatio']

col_a = col_a_1 + col_a_hidden + col_a_2

# col_a = ['ActivityDesc', 'StudentId', 'Lastname', 'Firstname', \
#          'TotalRecs', 'TotalAbsents', 'AbsentRatio']

# col_a_hidden = ['AorWStatus', 'ClassStatus', 'UndergradCrHrsEnrolled'
#                 'TotalAs','TotalEs','TotalPs','TotalTs','TotalHs','TotalCcs']

df_courses = pd.read_csv('spring_2019_data2.csv')
# ﻿DfltId,LastName,FirstName,FiOfLastName,FiOfFirstName,FullName,CdivId,PrgmId1,College,FirstMajor,1stMajorDescAndCode,NumCcsjSports,IsAthlete,AthleticTeamCodes,HasAttendanceData,SessionId,SessionDesc,TermId,DeptId,CrseId,SectId,IsGenEd,InstId,ShortName,MeetDays,TimeStart,TimeEnd,MidtermGrade,FinalGrade,NumMeetDaysPerWeek,NumA,NumE,NumH,NumCc,NumP,NumT,Total,SeatTimeAbsent,NeverAttended,AGtP,GtE9,UnexcusedAbsent,AbsentRanges,Present,PresentRanges

df_attendance_detail = pd.read_csv('spring_2019_data3.csv')
# ﻿TERM_ID,DEPT_ID,CRSE_ID,SECT_ID,DFLT_ID,LAST_NAME,FIRST_NAME,ATND_DATE,ATND_ID,AttendDateWoTime,AttendDateMonth,AttendDateDay

# col_b = ['DfltId', 'LastName', 'FirstName',
#          'DeptId', 'CrseId', 'SectId', 'InstId', 'ShortName',
#          'MeetDays', 'TimeStart', 'TimeEnd',
#          'NumMeetDaysPerWeek','NumA','NumE','NumH','NumCc','NumP','NumT','Total',
#          'SeatTimeAbsent','NeverAttended','AGtP','GtE9','UnexcusedAbsent','AbsentRanges','Present','PresentRanges']

col_b_1 = ['DfltId', 'LastName', 'FirstName', 'DeptId', 'CrseId', 'SectId']
col_b_hidden = ['InstId', 'ShortName', 'MeetDays', 'TimeStart', 'TimeEnd', 'NumMeetDaysPerWeek']
col_b_2 = ['NumA','NumE','NumP','NumT','NumH','NumCc','Total', 'SeatTimeAbsent']

col_b = col_b_1 + col_b_hidden + col_b_2

# ﻿TERM_ID,DEPT_ID,CRSE_ID,SECT_ID,DFLT_ID,LAST_NAME,FIRST_NAME,ATND_DATE,ATND_ID,AttendDateWoTime,AttendDateMonth,AttendDateDay
col_c = ['TERM_ID', 'DEPT_ID', 'CRSE_ID', 'SECT_ID', 'DFLT_ID', 'LAST_NAME', 'FIRST_NAME', 'ATND_DATE', 'ATND_ID', 'AttendDateWoTime', 'AttendDateMonth', 'AttendDateDay']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[
    html.H2('Attendance Demo App'),
    html.Div(
        [
            dcc.Dropdown(
                id="Team",
                options=[{'label': i, 'value': i} for i in teams],
                value='',
                placeholder="Select a team",
                clearable=False,
                style={'width': '25%',
                       'display': 'inline-block'},
            ), #end dropdown
        ]),

        html.H4('Attendance Summary by Team'),
        dash_table.DataTable(
            id='roster-datatable',
            columns=[{"name": i, "id": i} for i in col_a_1] +
                    # [{"name": i, "id": i, 'hidden': True} for i in col_a_hidden] +
                    [{"name": i, "id": i, 'hideable': True} for i in col_a_hidden] +
                    [{"name": i, "id": i} for i in col_a_2],
            row_selectable='single',
            selected_rows=[],
            # selected_rows=[0],
            page_action="native",
            page_current= 0,
            page_size= 10,
            style_header={'backgroundColor': 'rgb(230, 230, 230)',
                          'fontWeight': 'bold'},
            style_data_conditional=[{
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'}],
        ),#end datatable
        # ],#end inner div
        # style={'width': '25%',
        #        'display': 'inline-block'},
        # ),
        # style={'width': '25%',
        #        'display': 'inline-block'},
        # html.Div(id='intermediate-value'),

        # html.Div(id='final-value'),
        html.H4('Attendance Summary by Course'),
        dash_table.DataTable(
            id='courses-datatable',
            # columns=[{"name": i, "id": i} for i in col_b],
            columns=[{"name": i, "id": i} for i in col_b_1] +
            [{"name": i, "id": i, 'hideable': True} for i in col_b_hidden] +
            [{"name": i, "id": i} for i in col_b_2],
            # row_selectable='single',
            # selected_rows=[],
            # selected_rows=[0],
            # page_action="native",
            # page_current= 0,
            # page_size= 5,
            style_header={'backgroundColor': 'rgb(230, 230, 230)',
                          'fontWeight': 'bold'},
            style_data_conditional=[{
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'}],
        ),#end datatable

        # dash_table.DataTable(
        #     id='attendance-detail-datatable-datatable',
        #     columns=[{"name": i, "id": i} for i in col_c],
        #     # row_selectable='single',
        #     # selected_rows=[],
        #     # selected_rows=[0],
        #     # page_action="native",
        #     # page_current= 0,
        #     # page_size= 5,
        #     style_header={'backgroundColor': 'rgb(230, 230, 230)',
        #                   'fontWeight': 'bold'},
        #     style_data_conditional=[{
        #         'if': {'row_index': 'odd'},
        #         'backgroundColor': 'rgb(248, 248, 248)'}],
        # ),#end datatable
        # # Hidden div inside the app that stores the intermediate value
        html.Div(id='intermediate-value', style={'display': 'none'})
        ])#end outer div

def build_team_dataframe(Team):
    if not (Team is None or Team is ''):
        filtered_df = df_full[df_full['ActivityDesc'] == Team]
    else:
        filtered_df = None
    return filtered_df

@app.callback(Output('roster-datatable', 'data'), [Input('Team', 'value')])
def update_roster_datatable(Team):
    df = build_team_dataframe(Team)
    if df is not None:
        if len(df.index) > 0:
            data_df = df.to_dict(orient='records')
        else:
            data_df = []
    else:
        data_df = []

    return data_df
        # return [data_df]


@app.callback(Output('intermediate-value', 'children'), [Input('Team', 'value')])
def update_table(Team):
    if not (Team is None or Team is ''):
        filtered_df = df_full[df_full['ActivityDesc'] == Team]

        columns = ['ActivityDesc', 'StudentId', 'Lastname', 'Firstname']
        filtered_df = filtered_df[columns]
        # print(filtered_df.head())
        return filtered_df.to_json(orient='split')

def get_course_data(student_id):
    # filter 2nd dataset by student_id
    df_temp = df_courses[df_courses['DfltId'] == student_id]
    print(df_temp)
    #limit to a subset of columns during testing!
    df_out = df_temp[col_b]
    return df_out

@app.callback(Output('courses-datatable', 'data'),
             [Input('intermediate-value', 'children'),
              Input('roster-datatable', 'selected_rows')])
def update_debug_display(jsonified_cleaned_data, selected_rows):
    # print(derived_viewport_selected_row_ids)
    # print('')

    json_not_empty = (jsonified_cleaned_data is not None)
    row_not_selected = (selected_rows is not None)

    # result = ''
    data_df = []

    if json_not_empty and row_not_selected:
        dff = pd.read_json(jsonified_cleaned_data, orient='split')
        # print(dff.head())
    # if selected_rows is not None:
        # student_id = dff.iloc[selected_row_id, 1]
        # last = dff.iloc[i, 2]
        # first = dff.iloc[i, 3]
        # result = '{0}'.format(student_id)
        # result = '{0} {1}, {2}'.format(student_id, last, first)
        for i in selected_rows:
            student_id = dff.iloc[i, 1]
            last = dff.iloc[i, 2]
            first = dff.iloc[i, 3]
            result = '{0} {1}, {2}'.format(student_id, last, first)

        # add code to filter 2nd datset by the given stduent_id
        df_c = get_course_data(student_id)
        # print(df_c)

        if df_c is not None:
            if len(df_c.index) > 0:
                data_df = df_c.to_dict(orient='records')
            else:
                data_df = []
        else:
            data_df = []

        return data_df

    # else:
        # result = None
        # result = ''

    return data_df

    # if not active_cell is None:
        # print(active_cell)
        # student_id = dff.iloc[active_cell['row'], 1]
        # last = dff.iloc[active_cell['row'], 2]
        # first = dff.iloc[active_cell['row'], 3]
        # result = '{0} {1}, {2}'.format(student_id, last, first)
        # result = '{0}, {1}'.format(last, first)
    # else:
    #     result = ''
    #     # print('')
    #
        # return result

        # student_id = dff.iloc[active_cell['row'], 1]
        # last = dff.iloc[active_cell['row'], 2]
        # first = dff.iloc[active_cell['row'], 3]
        # result = '{0} {1}, {2}'.format(student_id, last, first)
        # result = '{0}, {1}'.format(last, first)
        # else:
        #     result = ''
        #     # print('')
        # return result

    # table = create_table(dff)
    # return table
    # return 'placeholder'


if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False)
