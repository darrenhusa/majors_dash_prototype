# models.py

import pandas as pd
import re
import datetime


def build_empower_dataset_1(empower, term):
    """creates student majors in term dataset/dataframe.
    """
    # created on 11/06/2019

    #original sql from Access
    ################################################################
    # SELECT CCSJ_PROD_SR_STUDENT_TERM.TERM_ID,
    # CCSJ_PROD_CCSJ_CO_V_NAME.DFLT_ID,
    # CCSJ_PROD_CCSJ_CO_V_NAME.LAST_NAME,
    # CCSJ_PROD_CCSJ_CO_V_NAME.FIRST_NAME,
    # CCSJ_PROD_SR_STUDENT_TERM.STUD_STATUS,
    # CCSJ_PROD_SR_STUDENT_TERM.CDIV_ID,
    # CCSJ_PROD_SR_STUDENT_TERM.ETYP_ID,
    # CCSJ_PROD_SR_STUDENT_TERM.PRGM_ID1,
    # CCSJ_PROD_SR_STUDENT_TERM.MAMI_ID_MJ1,
    # CCSJ_PROD_CO_MAJOR_MINOR.DESCR,
    # CCSJ_PROD_SR_ST_TERM_CRED.TU_CREDIT_ENRL,
    # CCSJ_PROD_SR_ST_TERM_CRED.TG_CREDIT_ENRL
    # FROM ((CCSJ_PROD_SR_STUDENT_TERM INNER JOIN
    #     CCSJ_PROD_CCSJ_CO_V_NAME ON
    #     CCSJ_PROD_SR_STUDENT_TERM.NAME_ID =
    #     CCSJ_PROD_CCSJ_CO_V_NAME.NAME_ID) INNER JOIN
    # CCSJ_PROD_CO_MAJOR_MINOR ON
    # CCSJ_PROD_SR_STUDENT_TERM.MAMI_ID_MJ1 =
    # CCSJ_PROD_CO_MAJOR_MINOR.MAMI_ID) INNER JOIN
    # CCSJ_PROD_SR_ST_TERM_CRED ON
    # (CCSJ_PROD_SR_STUDENT_TERM.NAME_ID =
    #     CCSJ_PROD_SR_ST_TERM_CRED.NAME_ID) AND
    # (CCSJ_PROD_SR_STUDENT_TERM.TERM_ID =
    #     CCSJ_PROD_SR_ST_TERM_CRED.TERM_ID)
    # WHERE (((CCSJ_PROD_SR_STUDENT_TERM.TERM_ID)="20191") AND
    #     ((CCSJ_PROD_SR_STUDENT_TERM.STUD_STATUS)='A' Or
    #         (CCSJ_PROD_SR_STUDENT_TERM.STUD_STATUS)='W'))
    # ORDER BY CCSJ_PROD_CCSJ_CO_V_NAME.LAST_NAME,
    # CCSJ_PROD_CCSJ_CO_V_NAME.FIRST_NAME;

    sql = """
    SELECT CCSJ_PROD.SR_STUDENT_TERM.TERM_ID,
    CCSJ_PROD.CCSJ_CO_V_NAME.DFLT_ID,
    CCSJ_PROD.CCSJ_CO_V_NAME.LAST_NAME,
    CCSJ_PROD.CCSJ_CO_V_NAME.FIRST_NAME,
    CCSJ_PROD.SR_STUDENT_TERM.STUD_STATUS,
    CCSJ_PROD.SR_STUDENT_TERM.CDIV_ID,
    CCSJ_PROD.SR_STUDENT_TERM.ETYP_ID,
    CCSJ_PROD.SR_STUDENT_TERM.PRGM_ID1,
    CCSJ_PROD.SR_STUDENT_TERM.MAMI_ID_MJ1,
    CCSJ_PROD.CO_MAJOR_MINOR.DESCR,
    CCSJ_PROD.SR_ST_TERM_CRED.TU_CREDIT_ENRL,
    CCSJ_PROD.SR_ST_TERM_CRED.TG_CREDIT_ENRL
    FROM ((CCSJ_PROD.SR_STUDENT_TERM INNER JOIN
        CCSJ_PROD.CCSJ_CO_V_NAME ON
        CCSJ_PROD.SR_STUDENT_TERM.NAME_ID =
        CCSJ_PROD.CCSJ_CO_V_NAME.NAME_ID) INNER JOIN
    CCSJ_PROD.CO_MAJOR_MINOR ON
    CCSJ_PROD.SR_STUDENT_TERM.MAMI_ID_MJ1 =
    CCSJ_PROD.CO_MAJOR_MINOR.MAMI_ID) INNER JOIN
    CCSJ_PROD.SR_ST_TERM_CRED ON
    (CCSJ_PROD.SR_STUDENT_TERM.NAME_ID =
        CCSJ_PROD.SR_ST_TERM_CRED.NAME_ID) AND
    (CCSJ_PROD.SR_STUDENT_TERM.TERM_ID =
        CCSJ_PROD.SR_ST_TERM_CRED.TERM_ID)
    WHERE (((CCSJ_PROD.SR_STUDENT_TERM.TERM_ID)='{0}') AND
        ((CCSJ_PROD.SR_STUDENT_TERM.STUD_STATUS)='A' Or
            (CCSJ_PROD.SR_STUDENT_TERM.STUD_STATUS)='W'))
    ORDER BY CCSJ_PROD.CCSJ_CO_V_NAME.LAST_NAME,
    CCSJ_PROD.CCSJ_CO_V_NAME.FIRST_NAME
    """.format(term)

    # print(sql)

    data = pd.read_sql(sql, empower)

    # NOTE when try and use as ColumnName syntax with SQL above
    # the column name comes in in all uppercase characters!!!
    # Rename column
    data.rename(columns={"DESCR": "FirstMajorDesc"}, inplace=True)

    return data


def build_empower_dataset_2(empower, term):
    """creates ccsj team rosters in term dataset/dataframe.
    """
    # created on 11/06/2019

    # NOTE: Need to adjust for active status students in term!!

    #original sql from Access
    ################################################################
    # SELECT CCSJ_PROD_SR_STUD_TERM_ACT.TERM_ID,
    # CCSJ_PROD_SR_STUD_TERM_ACT.ACTI_ID,
    # CCSJ_PROD_CO_ACTIV_CODE.DESCR,
    # CCSJ_PROD_CO_ACTIV_CODE.ATHLETIC_FLAG,
    # CCSJ_PROD_CCSJ_CO_V_NAME.DFLT_ID,
    # CCSJ_PROD_CCSJ_CO_V_NAME.LAST_NAME,
    # CCSJ_PROD_CCSJ_CO_V_NAME.FIRST_NAME
    # FROM (CCSJ_PROD_CCSJ_CO_V_NAME INNER JOIN
    #     CCSJ_PROD_SR_STUD_TERM_ACT ON
    #     CCSJ_PROD_CCSJ_CO_V_NAME.NAME_ID =
    #     CCSJ_PROD_SR_STUD_TERM_ACT.NAME_ID) INNER JOIN
    # CCSJ_PROD_CO_ACTIV_CODE ON
    # CCSJ_PROD_SR_STUD_TERM_ACT.ACTI_ID =
    # CCSJ_PROD_CO_ACTIV_CODE.ACTI_ID
    # WHERE (((CCSJ_PROD_SR_STUD_TERM_ACT.TERM_ID)="20191") AND
    #     ((CCSJ_PROD_CO_ACTIV_CODE.ATHLETIC_FLAG)="T"))
    # ORDER BY CCSJ_PROD_SR_STUD_TERM_ACT.ACTI_ID,
    # CCSJ_PROD_CCSJ_CO_V_NAME.LAST_NAME,
    # CCSJ_PROD_CCSJ_CO_V_NAME.FIRST_NAME;

    sql = """
    SELECT CCSJ_PROD.SR_STUD_TERM_ACT.TERM_ID,
    CCSJ_PROD.SR_STUD_TERM_ACT.ACTI_ID,
    CCSJ_PROD.CO_ACTIV_CODE.DESCR,
    CCSJ_PROD.CO_ACTIV_CODE.ATHLETIC_FLAG,
    CCSJ_PROD.CCSJ_CO_V_NAME.DFLT_ID,
    CCSJ_PROD.CCSJ_CO_V_NAME.LAST_NAME,
    CCSJ_PROD.CCSJ_CO_V_NAME.FIRST_NAME
    FROM (CCSJ_PROD.CCSJ_CO_V_NAME INNER JOIN
        CCSJ_PROD.SR_STUD_TERM_ACT ON
        CCSJ_PROD.CCSJ_CO_V_NAME.NAME_ID =
        CCSJ_PROD.SR_STUD_TERM_ACT.NAME_ID) INNER JOIN
    CCSJ_PROD.CO_ACTIV_CODE ON
    CCSJ_PROD.SR_STUD_TERM_ACT.ACTI_ID =
    CCSJ_PROD.CO_ACTIV_CODE.ACTI_ID
    WHERE (((CCSJ_PROD.SR_STUD_TERM_ACT.TERM_ID)='{0}') AND
        ((CCSJ_PROD.CO_ACTIV_CODE.ATHLETIC_FLAG)='T'))
    ORDER BY CCSJ_PROD.SR_STUD_TERM_ACT.ACTI_ID,
    CCSJ_PROD.CCSJ_CO_V_NAME.LAST_NAME,
    CCSJ_PROD.CCSJ_CO_V_NAME.FIRST_NAME
    """.format(term)

    # print(sql)

    data = pd.read_sql(sql, empower)
    return data


def build_empower_dataset_3(empower, term):
    """creates ccsj student-course enrollments in term dataset/dataframe.
    """
    # created on 11/06/2019

    #original sql from Access
    ################################################################
    # SELECT CCSJ_PROD_SR_ENROLL.TERM_ID,
    # CCSJ_PROD_SR_ENROLL.DEPT_ID,
    # CCSJ_PROD_SR_ENROLL.CRSE_ID,
    # CCSJ_PROD_SR_ENROLL.SECT_ID,
    # CCSJ_PROD_CCSJ_CO_V_NAME.DFLT_ID,
    # CCSJ_PROD_CCSJ_CO_V_NAME.LAST_NAME,
    # CCSJ_PROD_CCSJ_CO_V_NAME.FIRST_NAME,
    # CCSJ_PROD_SR_ENROLL.LETTER_GRADE_LST AS MidTermGrade,
    # CCSJ_PROD_SR_ENROLL.LETTER_GRADE_FIN,
    # CCSJ_PROD_SR_ENROLL.WDRAW_GRADE_FLAG
    # FROM CCSJ_PROD_CCSJ_CO_V_NAME INNER JOIN
    # CCSJ_PROD_SR_ENROLL ON
    # CCSJ_PROD_CCSJ_CO_V_NAME.NAME_ID =
    # CCSJ_PROD_SR_ENROLL.NAME_ID
    # WHERE (((CCSJ_PROD_SR_ENROLL.TERM_ID)="20191"))
    # ORDER BY CCSJ_PROD_SR_ENROLL.DEPT_ID,
    # CCSJ_PROD_SR_ENROLL.CRSE_ID,
    # CCSJ_PROD_SR_ENROLL.SECT_ID,
    # CCSJ_PROD_CCSJ_CO_V_NAME.LAST_NAME,
    # CCSJ_PROD_CCSJ_CO_V_NAME.FIRST_NAME;

    sql = """
    SELECT CCSJ_PROD.SR_ENROLL.TERM_ID,
    CCSJ_PROD.SR_ENROLL.DEPT_ID,
    CCSJ_PROD.SR_ENROLL.CRSE_ID,
    CCSJ_PROD.SR_ENROLL.SECT_ID,
    CCSJ_PROD.CCSJ_CO_V_NAME.DFLT_ID,
    CCSJ_PROD.CCSJ_CO_V_NAME.LAST_NAME,
    CCSJ_PROD.CCSJ_CO_V_NAME.FIRST_NAME,
    CCSJ_PROD.SR_ENROLL.LETTER_GRADE_LST AS MidTermGrade,
    CCSJ_PROD.SR_ENROLL.LETTER_GRADE_FIN,
    CCSJ_PROD.SR_ENROLL.WDRAW_GRADE_FLAG
    FROM CCSJ_PROD.CCSJ_CO_V_NAME INNER JOIN
    CCSJ_PROD.SR_ENROLL ON
    CCSJ_PROD.CCSJ_CO_V_NAME.NAME_ID =
    CCSJ_PROD.SR_ENROLL.NAME_ID
    WHERE (((CCSJ_PROD.SR_ENROLL.TERM_ID)='{0}'))
    ORDER BY CCSJ_PROD.SR_ENROLL.DEPT_ID,
    CCSJ_PROD.SR_ENROLL.CRSE_ID,
    CCSJ_PROD.SR_ENROLL.SECT_ID,
    CCSJ_PROD.CCSJ_CO_V_NAME.LAST_NAME,
    CCSJ_PROD.CCSJ_CO_V_NAME.FIRST_NAME
    """.format(term)

    # print(sql)

    data = pd.read_sql(sql, empower)
    return data


def build_empower_dataset_4_p1(empower, term):
    """creates basic ccsj course data in term dataset/dataframe.
    """
    # created on 11/06/2019

    #original sql from Access
    ################################################################
    # SELECT CCSJ_PROD_SR_COURSE_SECTION.TERM_ID,
    # CCSJ_PROD_SR_COURSE_SECTION.CRST_ID,
    # CCSJ_PROD_SR_COURSE_SECTION.CATA_ID,
    # CCSJ_PROD_SR_COURSE_SECTION.SESS_ID,
    # CCSJ_PROD_SR_COURSE_SECTION.DEPT_ID,
    # CCSJ_PROD_SR_COURSE_SECTION.CRSE_ID,
    # CCSJ_PROD_SR_COURSE_SECTION.SECT_ID,
    # CCSJ_PROD_SR_COURSE_SECTION.DESCR_EXTENDED,
    # CCSJ_PROD_SR_COURSE_SECTION.INST_ID,
    # CCSJ_PROD_CO_INSTRUCTOR.SHORT_NAME,
    # CCSJ_PROD_SR_COURSE_SECTION.DELV_ID
    # FROM CCSJ_PROD_SR_COURSE_SECTION INNER JOIN
    # CCSJ_PROD_CO_INSTRUCTOR ON
    # CCSJ_PROD_SR_COURSE_SECTION.INST_ID =
    # CCSJ_PROD_CO_INSTRUCTOR.INST_ID
    # WHERE (((CCSJ_PROD_SR_COURSE_SECTION.TERM_ID)="20191") AND
    #     ((CCSJ_PROD_SR_COURSE_SECTION.CRST_ID)="A"))
    # ORDER BY CCSJ_PROD_SR_COURSE_SECTION.DEPT_ID,
    # CCSJ_PROD_SR_COURSE_SECTION.CRSE_ID,
    # CCSJ_PROD_SR_COURSE_SECTION.SECT_ID;

    sql = """
    SELECT CCSJ_PROD.SR_COURSE_SECTION.TERM_ID,
    CCSJ_PROD.SR_COURSE_SECTION.CRST_ID,
    CCSJ_PROD.SR_COURSE_SECTION.CATA_ID,
    CCSJ_PROD.SR_COURSE_SECTION.SESS_ID,
    CCSJ_PROD.SR_COURSE_SECTION.DEPT_ID,
    CCSJ_PROD.SR_COURSE_SECTION.CRSE_ID,
    CCSJ_PROD.SR_COURSE_SECTION.SECT_ID,
    CCSJ_PROD.SR_COURSE_SECTION.DESCR_EXTENDED,
    CCSJ_PROD.SR_COURSE_SECTION.INST_ID,
    CCSJ_PROD.CO_INSTRUCTOR.SHORT_NAME,
    CCSJ_PROD.SR_COURSE_SECTION.DELV_ID
    FROM CCSJ_PROD.SR_COURSE_SECTION INNER JOIN
    CCSJ_PROD.CO_INSTRUCTOR ON
    CCSJ_PROD.SR_COURSE_SECTION.INST_ID =
    CCSJ_PROD.CO_INSTRUCTOR.INST_ID
    WHERE (((CCSJ_PROD.SR_COURSE_SECTION.TERM_ID)='{0}') AND
        ((CCSJ_PROD.SR_COURSE_SECTION.CRST_ID)='A'))
    ORDER BY CCSJ_PROD.SR_COURSE_SECTION.DEPT_ID,
    CCSJ_PROD.SR_COURSE_SECTION.CRSE_ID,
    CCSJ_PROD.SR_COURSE_SECTION.SECT_ID
    """.format(term)

    # print(sql)

    data = pd.read_sql(sql, empower)
    return data


def build_empower_dataset_4_p2(empower, term):
    # created on 11/11/2019

    # for course meet code detail information in term
    # NOTE PSM and PSA courses will result in multiple records or rows

    #original sql from Access
    ################################################################
    # SELECT CCSJ_PROD_SR_CRSECT_MEET.TERM_ID,
    # CCSJ_PROD_SR_CRSECT_MEET.CATA_ID,
    # CCSJ_PROD_SR_CRSECT_MEET.DEPT_ID,
    # CCSJ_PROD_SR_CRSECT_MEET.CRSE_ID,
    # CCSJ_PROD_SR_CRSECT_MEET.SECT_ID,
    # CCSJ_PROD_SR_CRSECT_MEET.MEET_ID,
    # CCSJ_PROD_SR_MEET_CODE.MEET_DAYS,
    # CCSJ_PROD_SR_MEET_CODE.TIME_START,
    # CCSJ_PROD_SR_MEET_CODE.TIME_END,
    # CCSJ_PROD_SR_CRSECT_MEET.DATE_FIRST,
    # CCSJ_PROD_SR_CRSECT_MEET.DATE_END
    # FROM CCSJ_PROD_SR_MEET_CODE INNER JOIN
    # CCSJ_PROD_SR_CRSECT_MEET ON
    # CCSJ_PROD_SR_MEET_CODE.MEET_ID =
    # CCSJ_PROD_SR_CRSECT_MEET.MEET_ID
    # WHERE (((CCSJ_PROD_SR_CRSECT_MEET.TERM_ID)="20191"))
    # ORDER BY CCSJ_PROD_SR_CRSECT_MEET.DEPT_ID,
    # CCSJ_PROD_SR_CRSECT_MEET.CRSE_ID,
    # CCSJ_PROD_SR_CRSECT_MEET.SECT_ID,
    # CCSJ_PROD_SR_MEET_CODE.TIME_START;

    sql = """
    SELECT CCSJ_PROD.SR_CRSECT_MEET.TERM_ID,
    CCSJ_PROD.SR_CRSECT_MEET.CATA_ID,
    CCSJ_PROD.SR_CRSECT_MEET.DEPT_ID,
    CCSJ_PROD.SR_CRSECT_MEET.CRSE_ID,
    CCSJ_PROD.SR_CRSECT_MEET.SECT_ID,
    CCSJ_PROD.SR_CRSECT_MEET.MEET_ID,
    CCSJ_PROD.SR_MEET_CODE.MEET_DAYS,
    CCSJ_PROD.SR_MEET_CODE.TIME_START,
    CCSJ_PROD.SR_MEET_CODE.TIME_END,
    CCSJ_PROD.SR_CRSECT_MEET.DATE_FIRST,
    CCSJ_PROD.SR_CRSECT_MEET.DATE_END
    FROM CCSJ_PROD.SR_MEET_CODE INNER JOIN
    CCSJ_PROD.SR_CRSECT_MEET ON
    CCSJ_PROD.SR_MEET_CODE.MEET_ID =
    CCSJ_PROD.SR_CRSECT_MEET.MEET_ID
    WHERE (((CCSJ_PROD.SR_CRSECT_MEET.TERM_ID)='{0}'))
    ORDER BY CCSJ_PROD.SR_CRSECT_MEET.DEPT_ID,
    CCSJ_PROD.SR_CRSECT_MEET.CRSE_ID,
    CCSJ_PROD.SR_CRSECT_MEET.SECT_ID,
    CCSJ_PROD.SR_MEET_CODE.TIME_START
    """.format(term)

    # print(sql)

    data = pd.read_sql(sql, empower)

    data['TIME_START'] = data['TIME_START'].astype(str)
    data['TIME_END'] = data['TIME_END'].astype(str)

    data['DATE_FIRST'] = data['DATE_FIRST'].astype(str)
    data['DATE_END'].fillna(value='', inplace=True)
    data['DATE_END'] = data['DATE_END'].astype(str)

    return data


def build_empower_dataset_5(empower, term):
    """creates ccsj student-course attendance detail in term dataset/dataframe.
    """
    # created on 11/06/2019

    #original sql from Access
    ################################################################
    # SELECT CCSJ_PROD_SR_STUD_ATTEND.TERM_ID,
    # CCSJ_PROD_SR_STUD_ATTEND.DEPT_ID,
    # CCSJ_PROD_SR_STUD_ATTEND.CRSE_ID,
    # CCSJ_PROD_SR_STUD_ATTEND.SECT_ID,
    # CCSJ_PROD_CCSJ_CO_V_NAME.DFLT_ID,
    # CCSJ_PROD_CCSJ_CO_V_NAME.LAST_NAME,
    # CCSJ_PROD_CCSJ_CO_V_NAME.FIRST_NAME,
    # CCSJ_PROD_SR_STUD_ATTEND.ATND_DATE,
    # CCSJ_PROD_SR_STUD_ATTEND.ATND_ID
    # FROM CCSJ_PROD_CCSJ_CO_V_NAME INNER JOIN
    # CCSJ_PROD_SR_STUD_ATTEND ON
    # CCSJ_PROD_CCSJ_CO_V_NAME.NAME_ID =
    #     CCSJ_PROD_SR_STUD_ATTEND.NAME_ID
    # WHERE (((CCSJ_PROD_SR_STUD_ATTEND.TERM_ID)='20191'))
    # ORDER BY CCSJ_PROD_SR_STUD_ATTEND.DEPT_ID,
    # CCSJ_PROD_SR_STUD_ATTEND.CRSE_ID,
    # CCSJ_PROD_SR_STUD_ATTEND.SECT_ID,
    # CCSJ_PROD_CCSJ_CO_V_NAME.LAST_NAME,
    # CCSJ_PROD_CCSJ_CO_V_NAME.FIRST_NAME,
    # CCSJ_PROD_SR_STUD_ATTEND.ATND_DATE;

    sql = """
    SELECT CCSJ_PROD.SR_STUD_ATTEND.TERM_ID,
    CCSJ_PROD.SR_STUD_ATTEND.DEPT_ID,
    CCSJ_PROD.SR_STUD_ATTEND.CRSE_ID,
    CCSJ_PROD.SR_STUD_ATTEND.SECT_ID,
    CCSJ_PROD.CCSJ_CO_V_NAME.DFLT_ID,
    CCSJ_PROD.CCSJ_CO_V_NAME.LAST_NAME,
    CCSJ_PROD.CCSJ_CO_V_NAME.FIRST_NAME,
    CCSJ_PROD.SR_STUD_ATTEND.ATND_DATE,
    CCSJ_PROD.SR_STUD_ATTEND.ATND_ID
    FROM CCSJ_PROD.CCSJ_CO_V_NAME INNER JOIN
    CCSJ_PROD.SR_STUD_ATTEND ON
    CCSJ_PROD.CCSJ_CO_V_NAME.NAME_ID =
        CCSJ_PROD.SR_STUD_ATTEND.NAME_ID
    WHERE (((CCSJ_PROD.SR_STUD_ATTEND.TERM_ID)='{0}'))
    ORDER BY CCSJ_PROD.SR_STUD_ATTEND.DEPT_ID,
    CCSJ_PROD.SR_STUD_ATTEND.CRSE_ID,
    CCSJ_PROD.SR_STUD_ATTEND.SECT_ID,
    CCSJ_PROD.CCSJ_CO_V_NAME.LAST_NAME,
    CCSJ_PROD.CCSJ_CO_V_NAME.FIRST_NAME,
    CCSJ_PROD.SR_STUD_ATTEND.ATND_DATE
    """.format(term)

    # print(sql)

    data = pd.read_sql(sql, empower)

    data['ATND_DATE'] = data['ATND_DATE'].astype(str)

    return data


def determine_if_course_is_gen_ed(key, dictionary):
    try:
        # print('dictionary[{0}] = {1}'.format(key, dictionary[key]))
        return dictionary[key]
    except KeyError:
        return False


def lookup_academic_program(key, dictionary):
    try:
        result = dictionary[key]
    except KeyError:
        result = '<<OTHER>>'

    return result


def calculate_absent_ratio_for_majors_datatable(row):
    # created on 9/03/2019

    numerator = int(row['TotalAbsents'])
    denominator = numerator + int(row['TotalPs']) + int(row['TotalTs'])

    if denominator != 0:
        number_result = 100 * float(numerator / denominator)
        rounded_result = round(number_result , 0)
        result = rounded_result
        # result = "{0:.0f}".format(number_result)
    else:
        result = ""

    return result


def calculate_absent_ratio_for_student_courses_datatable(row):
    # created on 11/07/2019

    numerator = int(row['NumAbsents'])
    denominator = numerator + int(row['NumPs']) + int(row['NumTs'])

    if denominator != 0:
        number_result = 100 * float(numerator / denominator)
        rounded_result = round(number_result , 0)
        result = rounded_result
        # result = "{0:.0f}".format(number_result)
    else:
        result = ""

    return result


def isBlank(myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True
