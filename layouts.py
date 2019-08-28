# layouts.py

import dash_core_components as dcc
import dash_html_components as html
import dash_table

from app import app
from callbacks import programs

# col_a_1 = ['ActivityDesc', 'StudentId', 'Lastname', 'Firstname']
# col_a_hidden = ['AorWStatus', 'ClassStatus', 'UndergradCrHrsEnrolled',\
#                 'TotalAs','TotalEs','TotalPs','TotalTs','TotalHs','TotalCcs']
# col_a_2 = ['TotalRecs', 'TotalAbsents', 'AbsentRatio']
#
# col_a = col_a_1 + col_a_hidden + col_a_2

# col_a = ['ActivityDesc', 'StudentId', 'Lastname', 'Firstname', \
#          'TotalRecs', 'TotalAbsents', 'AbsentRatio']

col_a = ['TERM_ID', 'DFLT_ID', 'LAST_NAME', 'FIRST_NAME', 'STUD_STATUS',
         'CDIV_ID', 'ETYP_ID', 'PRGM_ID1', 'MAMI_ID_MJ1', 'TU_CREDIT_ENRL',
         'TG_CREDIT_ENRL', 'College', 'Programs']

# col_a_hidden = ['AorWStatus', 'ClassStatus', 'UndergradCrHrsEnrolled'
#                 'TotalAs','TotalEs','TotalPs','TotalTs','TotalHs','TotalCcs']

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


layout1 = html.Div(children=[
    html.H2('Fall 2019 Attendance Tracking Dashboard'),
    html.Div(
        [
            dcc.Dropdown(
                id="Program",
                options=[{'label': i, 'value': i} for i in programs],
                value='',
                placeholder="Select an academic program",
                clearable=False,
                style={'width': '25%',
                       'display': 'inline-block'},
            ), #end dropdown
        ]),

        html.H4('Attendance Summary by Academic Program'),
        dash_table.DataTable(
            id='majors-datatable',
            columns=[{"name": i, "id": i} for i in col_a],
                    # [{"name": i, "id": i, 'hidden': True} for i in col_a_hidden] +
                    # [{"name": i, "id": i, 'hideable': True} for i in col_a_hidden] +
                    # [{"name": i, "id": i} for i in col_a_2],
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
        # html.H4('Attendance Summary by Course'),
        # dash_table.DataTable(
        #     id='courses-datatable',
        #     # columns=[{"name": i, "id": i} for i in col_b],
        #     columns=[{"name": i, "id": i} for i in col_b_1] +
        #     [{"name": i, "id": i, 'hideable': True} for i in col_b_hidden] +
        #     [{"name": i, "id": i} for i in col_b_2],
        #     row_selectable='single',
        #     selected_rows=[],
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
        # html.H4('Course Attendance Detail Data'),
        # dash_table.DataTable(
        #     id='attendance-detail-datatable',
        #     columns=[{"name": i, "id": i} for i in col_c],
        #     page_action="native",
        #     page_current= 0,
        #     page_size= 5,
        #     style_header={'backgroundColor': 'rgb(230, 230, 230)',
        #                   'fontWeight': 'bold'},
        #     style_data_conditional=[{
        #         'if': {'row_index': 'odd'},
        #         'backgroundColor': 'rgb(248, 248, 248)'}],
        # ),#end datatable
        #
        # # Hidden div that stores rosters-data
        html.Div(id='majors-data', style={'display': 'none'}),
        #
        # # Hidden div that stores courses-data
        # html.Div(id='courses-data', style={'display': 'none'})

        ])#end outer div
