# Majors Dash Prototype

# TODO - Major
- [] Test the Live Updating of Empower data based on dcc.Interval component.  See https://dash.plot.ly/live-updates
- [] Fix the toggle show behavior so that columns appear where desired as opposed to at the end of the datatable.
- [X] Use pyyaml library and a yaml data file for app configuration data.  Remove code like models.py/classify_empower_major_codes_into_programs() since it HARDCODES the mapping/lookup of values! See https://www.hackerearth.com/practice/notes/samarthbhargav/a-design-pattern-for-configuration-management-in-python/
- [] Test operation with additional dropdown boxes. Possibilities include IsAthlete dropdown to reproduce or mimic the athletics dash prototype operation.

- [] Can the performance be improved by doing various pandas aggregations for the datasets needed instead of the current implementation? See Example 2 at https://dash.plot.ly/sharing-data-between-callbacks
- [] Can the performance be improved by using caching with redis or some equivalent technology? See Example 3 at https://dash.plot.ly/sharing-data-between-callbacks
- [] Add unit tests and/or integration tests.
- [] Improve the web design. Use a CSS framework like Bootstrap. Fix datatable presentation and dropdown appearances.
- [] Improve the web design. Use dash-bootstrap components. See https://dash-bootstrap-components.opensource.faculty.ai/ for more information.

# TODO - Minor
- [] Need to fix the cases where the student_id is less than 9 characters long (example is KM in Human Services)!!!
- [] Need to verify if attendance detail data for coruses like EWPC 096 print properly. See JA in Criminal Justice for an example.
 
- [X] Rename the field AttendPercentage in majors datatable and courses datatable to AbsentRatio.  Calculate the same way AbsentRatio = NumAbsents/NumTotal where NumAbsents = NumAs + NumEs and NumPresents = NumPs + NumTs and NumTotal = NumPresents + NumAbsents.  Note do not want to count NumHs and NumCcs in this calculation because it would penalize the student for holidays and/or class cancellations. Note larger values of AbsentRatio indicate greater concern or urgency.
- [] Debug why the IsAthlete field is empty in majors datatable.
- [] Use yaml config files to store CCSJ courses IsGenEd status? Add IsGenEd dropdown to courses datatable?
- [] Add field to calculate TotalPresents to majors datatable and courses datatable.  This should make the checking of the data/calculations easier during testing.
- [] Clean-up fields on datatables. Hide or show additional fields based on desired appearance.
- [] Can I refactor the app to eliminate the use of the hidden divs and use the datatable fields directly instead? See https://dash.plot.ly/datatable/interactivity Can I use rows and derived_virtual_selected_rows  as in the update_graphs callback to improve the implementation.
- [] Clean-up code relative to None values for initial app state. Am I doing this in a pythonesque way or using preferred code patterns?
