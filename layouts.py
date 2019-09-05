# layouts.py

import dash_core_components as dcc
import dash_html_components as html
import dash_table

from app import app
from callbacks import term, update_interval_in_minutes
# from callbacks import programs, term, update_interval_in_minutes

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
         'TG_CREDIT_ENRL', 'FtPtStatus', 'College', 'Programs', 'FirstMajorDesc',
         'NumCcsjSports', 'IsAthlete', 'AthleticTeamCodes', 'TotalAs', 'TotalEs',
         'TotalPs', 'TotalTs', 'TotalHs', 'TotalCcs', 'TotalRecs',
         'TotalAbsents', 'AbsentRatio']

col_a_visible = ['DFLT_ID', 'LAST_NAME', 'FIRST_NAME', 'FtPtStatus', 'Programs',
                 'FirstMajorDesc', 'IsAthlete', 'AthleticTeamCodes', 'TotalAs', 'TotalEs',
                 'TotalPs', 'TotalTs', 'TotalHs', 'TotalCcs', 'TotalRecs',
                 'TotalAbsents', 'AbsentRatio']

# initial_col_a_state = [True, False, False, False, True,
#                    True, True, True, True, True,
#                    True, False, True, False, False,
#                    True, False, True, False, False,
#                    False, False, False, False, False,
#                    False, False]

hidden_col_a = ['TERM_ID', 'STUD_STATUS',
                'CDIV_ID', 'ETYP_ID', 'PRGM_ID1', 'MAMI_ID_MJ1', 'TU_CREDIT_ENRL',
                'TG_CREDIT_ENRL', 'College',
                'NumCcsjSports']

# col_a_hidden = ['AorWStatus', 'ClassStatus', 'UndergradCrHrsEnrolled'
#                 'TotalAs','TotalEs','TotalPs','TotalTs','TotalHs','TotalCcs']

# col_b = ['DfltId', 'LastName', 'FirstName',
#          'DeptId', 'CrseId', 'SectId', 'InstId', 'ShortName',
#          'MeetDays', 'TimeStart', 'TimeEnd',
#          'NumMeetDaysPerWeek','NumA','NumE','NumH','NumCc','NumP','NumT','Total',
#          'SeatTimeAbsent','NeverAttended','AGtP','GtE9','UnexcusedAbsent','AbsentRanges','Present','PresentRanges']

col_b = ['TERM_ID', 'CRST_ID', 'SESS_ID', 'DEPT_ID', 'CRSE_ID',
         'SECT_ID', 'DESCR_EXTENDED', 'INST_ID', 'SHORT_NAME',	'DFLT_ID',
         'LAST_NAME', 'FIRST_NAME',	'WDRAW_GRADE_FLAG',
         'MeetDays', 'TimeStart', 'TimeEnd', 'DateFirst', 'DateEnd',
         'MidTermGrade', 'FinalGrade', 'NumA', 'NumE', 'NumP', 'NumT', 'NumH', 'NumCc',
         'NumRecs', 'NumAbsents', 'AbsentRatio']

col_b_visible = ['SESS_ID', 'DEPT_ID', 'CRSE_ID',
                 'SECT_ID', 'DESCR_EXTENDED', 'INST_ID', 'SHORT_NAME',
                 'MeetDays', 'TimeStart', 'TimeEnd', 'NumA', 'NumE', 'NumP', 'NumT', 'NumH', 'NumCc',
                 'NumRecs', 'NumAbsents', 'AbsentRatio']

hidden_col_b = ['TERM_ID', 'CRST_ID', 'DFLT_ID',
                'LAST_NAME', 'FIRST_NAME', 'WDRAW_GRADE_FLAG',
                'DateFirst', 'DateEnd', 'MidTermGrade', 'FinalGrade']
# col_b_1 = ['DfltId', 'LastName', 'FirstName', 'DeptId', 'CrseId', 'SectId']
# col_b_hidden = ['InstId', 'ShortName', 'MeetDays', 'TimeStart', 'TimeEnd', 'NumMeetDaysPerWeek']
# col_b_2 = ['NumA','NumE','NumP','NumT','NumH','NumCc','Total', 'SeatTimeAbsent']
#
# col_b = col_b_1 + col_b_hidden + col_b_2

# ﻿TERM_ID,DEPT_ID,CRSE_ID,SECT_ID,DFLT_ID,LAST_NAME,FIRST_NAME,ATND_DATE,ATND_ID,AttendDateWoTime,AttendDateMonth,AttendDateDay
col_c = ['TERM_ID', 'DEPT_ID', 'CRSE_ID', 'SECT_ID', 'DFLT_ID', 'LAST_NAME', 'FIRST_NAME', 'ATND_DATE', 'ATND_ID']
hidden_col_c = ['TERM_ID', 'DFLT_ID', 'LAST_NAME', 'FIRST_NAME']
col_c_visible = ['DEPT_ID', 'CRSE_ID', 'SECT_ID', 'ATND_DATE', 'ATND_ID']
# col_c = ['TERM_ID', 'DEPT_ID', 'CRSE_ID', 'SECT_ID', 'DFLT_ID', 'LAST_NAME', 'FIRST_NAME', 'ATND_DATE', 'ATND_ID', 'AttendDateWoTime', 'AttendDateMonth', 'AttendDateDay']

def set_datatable_columns(columns, hideable):
    #TODO - Need to fix code so that it is easier to specify and/or change the visible and hideable columns
    column_list = []

    # print('Inside set_datatable_columns!!!!!!')
    # print(columns)
    # print(hideable)
    # print(hideable[0])
    # print(hideable[1])
    # print('')

    # for i in columns:
        # print(i)

        # column_list.append({"name": i, "id": i, 'hideable': columns[]})

    return column_list


def convert_term_to_long_term(term_code):
    term_year = term_code[0:4]
    term_part = term_code[-1]

    if term_part == '1':
        result = 'Fall {0}'.format(term_year)
    elif term_part == '2':
        result = 'Spring {0}'.format(int(term_year) + 1)

    return result


def set_update_interval_for_dcc_interval_component(num_minutes):
    # created on 8/30/2019

    # conversion factors:
    # 1 min = 60 seconds
    # 1 sec = 1000 ms = 1,000 milliseconds

    return (num_minutes * 60 * 1000)

long_term = convert_term_to_long_term(term)

layout1 = html.Div(children=[
    html.H2(f'{long_term} Attendance Tracking Dashboard'), # end h2
    html.H5(id='live-update-text'), # end h5
    dcc.Interval(
            id='interval-component',
            interval=set_update_interval_for_dcc_interval_component(update_interval_in_minutes),
            n_intervals=0
    ), # end dcc.ioterval

    html.H4('Attendance Summary by Student'), # end h4
    dash_table.DataTable(
            id='majors-datatable',
            columns=[{"name": i, "id": i} for i in col_a_visible] + [{"name": i, "id": i, 'hideable': True} for i in hidden_col_a],
            # columns=[{"name": i, "": i} for i in col_a],
            hidden_columns=hidden_col_a,
            # columns=set_datatable_columns(col_a, hideable_a_cols),
            row_selectable='single',
            selected_rows=[],
            # selected_rows=[0],
            sort_action='native',
            filter_action='native',
            page_action="native",
            page_current= 0,
            page_size= 10,
            style_header={'backgroundColor': 'rgb(230, 230, 230)',
                          'fontWeight': 'bold'},
            style_data_conditional=[{
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'}],
            style_table={'overflowX': 'scroll'},
        ), # end datatable

        # ],#end inner div
        # style={'width': '25%',
        #        'display': 'inline-block'},
        # ),
        # style={'width': '25%',
        #        'display': 'inline-block'},
        # # html.Div(id='intermediate-value'),

        # html.Div(id='final-value'),
        html.H4('Student Attendance Summary by Course'),
        # html.Div(id='test-print-courses'),

        dash_table.DataTable(
            id='courses-datatable',
            # columns=[{"name": i, "id": i} for i in col_b],
            # columns=[{"name": i, "id": i} for i in col_b],
            columns=[{"name": i, "id": i} for i in col_b_visible] + [{"name": i, "id": i, 'hideable': True} for i in hidden_col_b],
            hidden_columns=hidden_col_b,

            # [{"name": i, "id": i, 'hideable': True} for i in col_b_hidden] +
            # [{"name": i, "id": i} for i in col_b_2],
            row_selectable='single',
            selected_rows=[],
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

        html.H4('Student Course Attendance Detail'),
        dash_table.DataTable(
            id='attendance-detail-datatable',
            columns=[{"name": i, "id": i} for i in col_c_visible] + [{"name": i, "id": i, 'hideable': True} for i in hidden_col_c],
            hidden_columns=hidden_col_c,
            page_action="native",
            page_current= 0,
            page_size= 5,
            style_header={'backgroundColor': 'rgb(230, 230, 230)',
                          'fontWeight': 'bold'},
            style_data_conditional=[{
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'}],
        ),#end datatable

        # Hidden div that stores rosters-data
        # html.Div(id='majors-data', style={'display': 'none'}),
        #
        # Hidden div that stores courses-data
        # html.Div(id='courses-data', style={'display': 'none'}),

        # temporarily set to visible!
        # load datasets into these divs!!!!
        html.Div(id='dashboard-datasets', style={'display': 'none'}), # end div
        # html.Div(id='courses-datasets', style={'display': 'none'}), # end div
    ]) #end outer div
