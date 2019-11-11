# Majors Dash Prototype

# To run the python/dash app
* Start a python command-line prompt/environment (e.g. base)
* Navigate to the local folder/directory (i.e c:\users\darrenh\dash_code\majors_dash_prototype)
* Run conda activate dash-env
* To start the python app, run python index.py
* Start a browser and visit http://127.0.0.1:8050/ to view the dash application


# TODO - New Features
- [] Add total undergraduate credit hours enrolled to dash datatable #1.
- [] Add course credit hours to dash datatable #2.
- [] Resize columns of dash datatable #3?
- [] Modify dash datatable #3 to allow vertical scrolling through the records (as opposed to current pagination behavior)
- [] Add dash datatable multi-headers to dash datatable #1 and #2 to group attendance info field visually


# TODO - Optimization
- [] Figure out how to write a function that takes two dataframes and returns a new df column.


# TODO - User Interface
- [] Fix the toggle show behavior so that columns appear where desired as opposed to at the end of the datatable.
- [] Test operation with additional dropdown boxes. Possibilities include IsAthlete dropdown to reproduce or mimic the athletics dash prototype operation.
- [] Add IsGenEd dropdown to courses datatable?
- [] Clean-up fields on datatables. Hide or show additional fields based on desired appearance.
- [] Can I refactor the app to eliminate the use of the hidden divs and use the datatable fields directly instead? See https://dash.plot.ly/datatable/interactivity Can I use rows and derived_virtual_selected_rows  as in the update_graphs callback to improve the implementation.
- [] Clean-up code relative to None values for initial app state. Am I doing this in a pythonesque way or using preferred code patterns?


# TODO - Other
- [] Can the performance be improved by using caching with redis or some equivalent technology? See Example 3 at https://dash.plot.ly/sharing-data-between-callbacks
- [] Add unit tests and/or integration tests.
- [] Improve the web design. Use a CSS framework like Bootstrap. Fix datatable presentation and dropdown appearances.
- [] Improve the web design. Use dash-bootstrap components. See https://dash-bootstrap-components.opensource.faculty.ai/ for more information.


# COMPLETED #
############

# MAJOR
- [X] Test the Live Updating of Empower data based on dcc.Interval component.  See https://dash.plot.ly/live-updates
- [X] Use pyyaml library and a yaml data file for app configuration data.  Remove code like models.py/classify_empower_major_codes_into_programs() since it HARDCODES the mapping/lookup of values! See https://www.hackerearth.com/practice/notes/samarthbhargav/a-design-pattern-for-configuration-management-in-python/
- [X] Can the performance be improved by doing various pandas aggregations for the datasets needed instead of the current implementation? See Example 2 at https://dash.plot.ly/sharing-data-between-callbacks

# MINOR
- [X] Add code figure out the day of the week from the ATND_DATE and update dash datatable #3 to include the new field/column.
- [X] Build courses data with meet code info (e.g. time start, time end, date start, date end) by doing a merge of dataframes instead.
- [X] Need to fix the cases where the student_id is less than 9 characters long (example is KM in Human Services)!!!
- [X] Need to fix the display of the student_id field in dash datatable #1 so that it has leading zeros.
- [X] Need to verify if attendance detail data for courses like EWPC 096 print properly. See JA in Criminal Justice for an example.
- [X] Rename the field AttendPercentage in majors datatable and courses datatable to AbsentRatio.  Calculate the same way AbsentRatio = NumAbsents/NumTotal where NumAbsents = NumAs + NumEs and NumPresents = NumPs + NumTs and NumTotal = NumPresents + NumAbsents.  Note do not want to count NumHs and NumCcs in this calculation because it would penalize the student for holidays and/or class cancellations. Note larger values of AbsentRatio indicate greater concern or urgency.
- [X] Debug why the IsAthlete field is empty in majors datatable.
- [X] Use yaml config files to store CCSJ courses IsGenEd status?
- [X] Add field to calculate TotalPresents to majors datatable and courses datatable.  This should make the checking of the data/calculations easier during testing.
