# models.py

import pandas as pd
import re
import datetime


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


def build_empower_dataset_4(empower, term):
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


def build_empower_dataset_4b(empower, term):
    """creates ccsj course data with meet-code info in term dataset/dataframe.
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
    # CCSJ_PROD_SR_COURSE_SECTION.DELV_ID,
    # CCSJ_PROD_SR_MEET_CODE.MEET_DAYS,
    # CCSJ_PROD_SR_MEET_CODE.TIME_START,
    # CCSJ_PROD_SR_MEET_CODE.TIME_END,
    # CCSJ_PROD_SR_CRSECT_MEET.DATE_FIRST,
    # CCSJ_PROD_SR_CRSECT_MEET.DATE_END
    # FROM (CCSJ_PROD_SR_COURSE_SECTION INNER JOIN
    #     CCSJ_PROD_CO_INSTRUCTOR ON
    #     CCSJ_PROD_SR_COURSE_SECTION.INST_ID =
    #     CCSJ_PROD_CO_INSTRUCTOR.INST_ID) INNER JOIN
    # (CCSJ_PROD_SR_MEET_CODE INNER JOIN
    #     CCSJ_PROD_SR_CRSECT_MEET ON
    #     CCSJ_PROD_SR_MEET_CODE.MEET_ID =
    #     CCSJ_PROD_SR_CRSECT_MEET.MEET_ID) ON
    # (CCSJ_PROD_SR_COURSE_SECTION.SECT_ID =
    #     CCSJ_PROD_SR_CRSECT_MEET.SECT_ID) AND
    # (CCSJ_PROD_SR_COURSE_SECTION.CRSE_ID =
    #     CCSJ_PROD_SR_CRSECT_MEET.CRSE_ID) AND
    # (CCSJ_PROD_SR_COURSE_SECTION.DEPT_ID =
    #     CCSJ_PROD_SR_CRSECT_MEET.DEPT_ID) AND
    # (CCSJ_PROD_SR_COURSE_SECTION.TERM_ID =
    #     CCSJ_PROD_SR_CRSECT_MEET.TERM_ID)
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
    CCSJ_PROD.SR_COURSE_SECTION.DELV_ID,
    CCSJ_PROD.SR_MEET_CODE.MEET_DAYS,
    CCSJ_PROD.SR_MEET_CODE.TIME_START,
    CCSJ_PROD.SR_MEET_CODE.TIME_END,
    CCSJ_PROD.SR_CRSECT_MEET.DATE_FIRST,
    CCSJ_PROD.SR_CRSECT_MEET.DATE_END
    FROM (CCSJ_PROD.SR_COURSE_SECTION INNER JOIN
        CCSJ_PROD.CO_INSTRUCTOR ON
        CCSJ_PROD.SR_COURSE_SECTION.INST_ID =
        CCSJ_PROD.CO_INSTRUCTOR.INST_ID) INNER JOIN
    (CCSJ_PROD.SR_MEET_CODE INNER JOIN
        CCSJ_PROD.SR_CRSECT_MEET ON
        CCSJ_PROD.SR_MEET_CODE.MEET_ID =
        CCSJ_PROD.SR_CRSECT_MEET.MEET_ID) ON
    (CCSJ_PROD.SR_COURSE_SECTION.SECT_ID =
        CCSJ_PROD.SR_CRSECT_MEET.SECT_ID) AND
    (CCSJ_PROD.SR_COURSE_SECTION.CRSE_ID =
        CCSJ_PROD.SR_CRSECT_MEET.CRSE_ID) AND
    (CCSJ_PROD.SR_COURSE_SECTION.DEPT_ID =
        CCSJ_PROD.SR_CRSECT_MEET.DEPT_ID) AND
    (CCSJ_PROD.SR_COURSE_SECTION.TERM_ID =
        CCSJ_PROD.SR_CRSECT_MEET.TERM_ID)
    WHERE (((CCSJ_PROD.SR_COURSE_SECTION.TERM_ID)='{0}') AND
        ((CCSJ_PROD.SR_COURSE_SECTION.CRST_ID)='A'))
    ORDER BY CCSJ_PROD.SR_COURSE_SECTION.DEPT_ID,
    CCSJ_PROD.SR_COURSE_SECTION.CRSE_ID,
    CCSJ_PROD.SR_COURSE_SECTION.SECT_ID
    """.format(term)

    # print(sql)

    data = pd.read_sql(sql, empower)
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
    return data


def build_majors_data_dataset(empower, term):
    # created on 8/28/2019

    # For the python/dash/flask dashboard app

    # SELECT CCSJ_PROD_SR_STUDENT_TERM.TERM_ID,
    # CCSJ_PROD_CCSJ_CO_V_NAME.DFLT_ID,
    # CCSJ_PROD_CCSJ_CO_V_NAME.LAST_NAME,
    # CCSJ_PROD_CCSJ_CO_V_NAME.FIRST_NAME,
    # CCSJ_PROD_SR_STUDENT_TERM.STUD_STATUS,
    # CCSJ_PROD_SR_STUDENT_TERM.CDIV_ID,
    # CCSJ_PROD_SR_STUDENT_TERM.ETYP_ID,
    # CCSJ_PROD_SR_STUDENT_TERM.PRGM_ID1,
    # CCSJ_PROD_SR_STUDENT_TERM.MAMI_ID_MJ1,
    # CCSJ_PROD_SR_ST_TERM_CRED.TU_CREDIT_ENRL,
    # CCSJ_PROD_SR_ST_TERM_CRED.TG_CREDIT_ENRL
    # FROM (CCSJ_PROD_SR_STUDENT_TERM INNER JOIN
    #     CCSJ_PROD_CCSJ_CO_V_NAME ON
    #     CCSJ_PROD_SR_STUDENT_TERM.NAME_ID =
    #     CCSJ_PROD_CCSJ_CO_V_NAME.NAME_ID) INNER JOIN
    # CCSJ_PROD_SR_ST_TERM_CRED ON
    # (CCSJ_PROD_SR_STUDENT_TERM.TERM_ID =
    #     CCSJ_PROD_SR_ST_TERM_CRED.TERM_ID) AND
    # (CCSJ_PROD_SR_STUDENT_TERM.NAME_ID =
    #     CCSJ_PROD_SR_ST_TERM_CRED.NAME_ID)
    # WHERE (((CCSJ_PROD_SR_STUDENT_TERM.TERM_ID)="20191") AND
    #     ((CCSJ_PROD_SR_STUDENT_TERM.STUD_STATUS)="A" Or
    #         (CCSJ_PROD_SR_STUDENT_TERM.STUD_STATUS)="W") AND
    #     ((CCSJ_PROD_SR_STUDENT_TERM.PRGM_ID1) Not In ("MTI")));

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
    CCSJ_PROD.SR_ST_TERM_CRED.TU_CREDIT_ENRL,
    CCSJ_PROD.SR_ST_TERM_CRED.TG_CREDIT_ENRL
    FROM (CCSJ_PROD.SR_STUDENT_TERM INNER JOIN
        CCSJ_PROD.CCSJ_CO_V_NAME ON
        CCSJ_PROD.SR_STUDENT_TERM.NAME_ID =
        CCSJ_PROD.CCSJ_CO_V_NAME.NAME_ID) INNER JOIN
    CCSJ_PROD.SR_ST_TERM_CRED ON
    (CCSJ_PROD.SR_STUDENT_TERM.TERM_ID =
        CCSJ_PROD.SR_ST_TERM_CRED.TERM_ID) AND
    (CCSJ_PROD.SR_STUDENT_TERM.NAME_ID =
        CCSJ_PROD.SR_ST_TERM_CRED.NAME_ID)
    WHERE (((CCSJ_PROD.SR_STUDENT_TERM.TERM_ID)='{0}') AND
        ((CCSJ_PROD.SR_STUDENT_TERM.STUD_STATUS)='A' Or
            (CCSJ_PROD.SR_STUDENT_TERM.STUD_STATUS)='W') AND
        ((CCSJ_PROD.SR_STUDENT_TERM.PRGM_ID1) Not In ('MTI')))
    """.format(term)

    data = pd.read_sql(sql, empower)
    data['DFLT_ID'] = data['DFLT_ID'].astype(str)

    # Add code to clean-up the DFLT_ID - Need to add leading zeros if the length < 9
    # data['DFLT_ID'] = data['DFLT_ID'].astype(str).str.zfill(9)
    # data['DFLT_ID'] = data['DFLT_ID'].map(lambda x: f'{x:0>9}')

    # cursor = empower.cursor()
    # cursor.execute(sql)
    # rows = cursor.fetchall()

    #insert test for if no records returned???
    # for row in rows:
    #     student_id = row.DFLT_ID
    #     length = len(row.DFLT_ID)
    #     print('student_id = {0}, length = {1}'.format(student_id, length))
    #
    #     if length < 9:
    #         print('Need to fix the DFLT_ID = ', student_id)
    #         print('')
    #         print('')
    #         # data[]

    return data


def process_crse_id_field_for_attendance_detail_datatable(crse_id):
    # created on 9/3/2019

    # if isBlank(crse_id):
    #     return None

    result = ''
    # test for numbers < 100, add a leading zero and convert to a string type
    # Note: int(115L) throws a 'ValueError since cannot convert to an integer type'
    try:
        if int(crse_id) < 100:
            # Add a leading zero and make the results a string
            result = f'0{crse_id}'
        else:
            result = str(crse_id)

    except ValueError:
        result = str(crse_id)

    return result


def build_courses_data_dataset(empower, term):
    # created on 8/29/2019

    sql = """
    SELECT DISTINCT CCSJ_PROD.SR_ENROLL.TERM_ID,
    CCSJ_PROD.SR_COURSE_SECTION.CRST_ID,
    CCSJ_PROD.SR_COURSE_SECTION.SESS_ID,
    CCSJ_PROD.SR_ENROLL.DEPT_ID,
    CCSJ_PROD.SR_ENROLL.CRSE_ID,
    CCSJ_PROD.SR_ENROLL.SECT_ID,
    CCSJ_PROD.SR_COURSE_SECTION.DESCR_EXTENDED,
    CCSJ_PROD.SR_COURSE_SECTION.INST_ID,
    CCSJ_PROD.CO_INSTRUCTOR.SHORT_NAME,
    CCSJ_PROD.CCSJ_CO_V_NAME.DFLT_ID,
    CCSJ_PROD.CCSJ_CO_V_NAME.LAST_NAME,
    CCSJ_PROD.CCSJ_CO_V_NAME.FIRST_NAME,
    CCSJ_PROD.SR_ENROLL.WDRAW_GRADE_FLAG,
    CCSJ_PROD.SR_ENROLL.LETTER_GRADE_LST,
    CCSJ_PROD.SR_ENROLL.LETTER_GRADE_FIN
    FROM (CCSJ_PROD.CCSJ_CO_V_NAME INNER JOIN
        CCSJ_PROD.SR_ENROLL ON
        CCSJ_PROD.CCSJ_CO_V_NAME.NAME_ID =
        CCSJ_PROD.SR_ENROLL.NAME_ID) INNER JOIN
    (CCSJ_PROD.CO_INSTRUCTOR INNER JOIN
        CCSJ_PROD.SR_COURSE_SECTION ON
        CCSJ_PROD.CO_INSTRUCTOR.INST_ID =
        CCSJ_PROD.SR_COURSE_SECTION.INST_ID) ON
    (CCSJ_PROD.SR_ENROLL.TERM_ID =
        CCSJ_PROD.SR_COURSE_SECTION.TERM_ID) AND
    (CCSJ_PROD.SR_ENROLL.DEPT_ID =
        CCSJ_PROD.SR_COURSE_SECTION.DEPT_ID) AND
    (CCSJ_PROD.SR_ENROLL.CRSE_ID =
        CCSJ_PROD.SR_COURSE_SECTION.CRSE_ID) AND
    (CCSJ_PROD.SR_ENROLL.SECT_ID =
        CCSJ_PROD.SR_COURSE_SECTION.SECT_ID)
    WHERE (((CCSJ_PROD.SR_ENROLL.TERM_ID)='{0}') AND
        ((CCSJ_PROD.SR_COURSE_SECTION.CRST_ID)='A'))
    ORDER BY CCSJ_PROD.SR_ENROLL.DEPT_ID,
    CCSJ_PROD.SR_ENROLL.CRSE_ID,
    CCSJ_PROD.SR_ENROLL.SECT_ID,
    CCSJ_PROD.CCSJ_CO_V_NAME.LAST_NAME,
    CCSJ_PROD.CCSJ_CO_V_NAME.FIRST_NAME
    """.format(term)

    # read the results into a dataframe
    data = pd.read_sql(sql, empower)

    return data


def build_attendance_detail_data_dataset(empower, term):
    # created on 8/29/2019

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

    data = pd.read_sql(sql, empower)
    return data


def create_college_from_prgm_id1(input_string):
    # updated on 7/10/2019
    # added new code for 2019-20?
    # MAT =>    MAT --> GRAD

    # updated on 3/28/2019
    # added new codes for 2019-20
    # PSM =>    PMnn --> DCP
    # PSA =>    PAnn --> GRAD
    # MAT =>    MTnn --> GRAD
    # MAP =>    MPnn --> GRAD

    # updated on 2/14/2018
    # added ORnn --> DCP and MSnn --> GRAD

    # input_string = col['PRGM_ID1']

    if isBlank(input_string):
        return '<<EMPTY>>'

    # print(col)

    if re.match(r'TR', input_string):
        return 'TRAD'
    # added for legacy entry ACCU
    # on 11/10/2017
    elif re.match(r'ACCU', input_string):
        return 'DCP'
    elif re.match(r'AC[0-9]', input_string):
        return 'DCP'
    elif re.match(r'OR[0-9]', input_string):
        return 'DCP'
    elif re.match(r'PM[0-9]', input_string):
        return 'DCP'
    #added for legacy entry GACC
    elif re.match(r'GACC', input_string):
        return 'GRAD'
    elif re.match(r'G[AM][0-9]', input_string):
        return 'GRAD'
    elif re.match(r'MS[0-9]', input_string):
        return 'GRAD'
    elif re.match(r'PA[0-9]', input_string):
        return 'GRAD'
    elif re.match(r'MT[0-9]', input_string):
        return 'GRAD'
    elif re.match(r'MP[0-9]', input_string):
        return 'GRAD'
    elif re.match(r'MAT', input_string):
        return 'GRAD'
    elif re.match(r'D[UG]', input_string):
        return 'DUAL'
    elif re.match(r'MTI', input_string):
        return 'MTI'
    elif re.match(r'STEM', input_string):
        return 'STEM'
    else:
        #print(col['PRGM_ID1'])
        return '<<OTHER>>'


# def classify_empower_major_codes_into_programs(major_code):
#     # created on 7/16/2019
#
#     if isBlank(major_code):
#         return ''
#
#     # print(col)
#
#     if major_code == 'A105' or major_code == '0105':
#         #Accounting
#         program = "Acct"
#     elif major_code == '4500' or major_code == '4503':
#         # Kinesiology/Biokinetics
#         program = "Kines/Biok"
#     elif major_code == '4501':
#         # Biomedical Science
#         program = "Biomed"
#     elif major_code == 'A205' or major_code == '2205' or major_code == 'J305':
#         # Business Management
#         program = "Bmt"
#     elif major_code == 'A705' or major_code == 'A605' or major_code == '0905' or major_code == '0805':
#         #strProgram = "CIS"
#         program = "CIS"
#     elif major_code == '0705' or major_code == '1505' or major_code == '1506' or major_code == 'A505':
#         #strProgram = "Communications"
#         program = "Comm"
#     elif major_code == 'A805' or major_code == '1005' or major_code == 'J505':
#         #strProgram = "Criminal Justice"
#         program = "CriJ"
#     elif major_code == '1405' or major_code == '5505' or major_code == '5305' or major_code == 'J605':
#         #strProgram = "Digital Studio Arts/MFA"
#         program = "DSA/MFA"
#
#     elif major_code == '1205' or major_code == '3005' or major_code == '6805' or major_code == '6815':
#         #strProgram = "Education"
#         program = "Educ"
#     elif major_code == 'A905' or major_code == '1305' or major_code == '1306' or major_code == '1307':
#         #strProgram = "English"
#         program = "Eng"
#     elif major_code == '4502':
#         # Forensic Biotechnology
#         program = "FrnsBio"
#     elif major_code == '4504':
#         # Forensic Science
#         program = "FrnsSci"
#     elif major_code == '1705' or major_code == 'B105':
#         #strProgram = "General Studies"
#         program = "GenStud"
#     elif major_code == '1706' or major_code == 'B104':
#         #strProgram = "Integrated Studies"
#         program = "IntStud"
#     elif major_code == 'D101' or major_code == '3305':
#         #strProgram = "General Science"
#         program = "GenSci"
#     elif major_code == 'C104' or major_code == '4905':
#         #strProgram = "Human Services"
#         program = "HSv"
#     elif major_code == 'B106' or major_code == '2005':
#         #strProgram = "Humanities"
#         program = "Hum"
#     elif major_code == 'B306' or major_code == '4910' or major_code == '4805' or major_code == '4806' or major_code == 'B305' or major_code == 'J705' or major_code == 'B303':
#         #strProgram = "Legal/Paralegal Studies"
#         program = "LSCC/PS"
#     elif major_code == '2805' or major_code == '6910' or major_code == 'B905' or major_code == 'B505':
#         #strProgram = "Psychology"
#         program = "Psyc"
#     elif major_code == '3205':
#         #strProgram = "Social Science"
#         program = "SocS"
#     elif major_code == '3606' or major_code == '3805' or major_code == '3605' or major_code == 'B405' or major_code == 'J805':
#         #strProgram = "Theology/Religious Studies"
#         program = "Theo/RlSt"
#     elif major_code == '9805':
#         program = "Und"
#     elif major_code == '9905':
#         #not applicable/non-degree
#         program = "NA"
#
#     #dcp programs
#     elif major_code == '2405':
#         program = "OrMn"
#     elif major_code == '5805' or major_code == '6005':
#         program = "LEM/PSM"
#
#     #graduate programs
#     elif major_code == '6705' or major_code == '7605':
#         program = "QA/Mn"
#     elif major_code == '6905':
#         program = "LEA/PSA"
#
#     else:
#         program = '<<OTHER>>'
#
#     return program


def isBlank(myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True


def trim_unwanted_spaces_at_end_of_string(input_string, number_of_spaces):
    # created on 10/19/2017

    length_of_string = len(input_string)
    last_character = length_of_string - number_of_spaces

    result = input_string[0:last_character]

    return result


def remove_time_from_datetime_object(datetime_obj):

    year = datetime_obj.year
    month = datetime_obj.month
    day = datetime_obj.day

    return datetime.date(year, month, day)


def remove_date_from_datetime_object(datetime_obj):
    # created on 8/29/2019

    return datetime_obj.time()


def create_ft_pt_status_from_undergrad_cr_hrs(number):

    # number = col['TU_CREDIT_ENRL']

    if number >= 12.0:
        return 'FT'
    else:
        return 'PT'


def lookup_empower_major_description(empower, input_code, empty_result='<<BLANK>>'):

    #modified on 1/6/2017
    # to accept an (optional) empty_result parameter
    # usage: lookup_empower_major_description(empower, input_code, '') or
    #        lookup_empower_major_description(empower, input_code)
    ###############################################################################

    if isBlank(input_code):
        return empty_result

    sql = """
    SELECT CCSJ_PROD.CO_MAJOR_MINOR.DESCR
    FROM CCSJ_PROD.CO_MAJOR_MINOR
    WHERE (((CCSJ_PROD.CO_MAJOR_MINOR.MAMI_ID)='{0}'))
    """.format(input_code)

    cursor = empower.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    #set to empty string
    description = ""

    #insert test for if no records returned???
    for row in rows:
        description = row.DESCR

    # print(rows[0])
    return description

    #sample code
    # dbCursor = conn.cursor()
    # sql = ('select field1, field2 from table')
    # dbCursor = conn.cursor()
    # dbCursor.execute(sql)
    # for row in dbCursor:
    #     # Now you should be able to access the fields as properties of "row"
    #     myVar1 = row.field1
    #     myVar2 = row.field2

    # conn.close()

def determine_number_of_athlete_records_in_sr_activities(empower, student_id, term):

 # SELECT CCSJ_PROD_CO_ACTIV_CODE.ACTI_ID,
 #    CCSJ_PROD_CO_ACTIV_CODE.DESCR
 #    FROM (CCSJ_PROD_CCSJ_CO_V_NAME INNER JOIN
 #    CCSJ_PROD_SR_STUD_TERM_ACT ON
 #    CCSJ_PROD_CCSJ_CO_V_NAME.NAME_ID =
 #    CCSJ_PROD_SR_STUD_TERM_ACT.NAME_ID) INNER JOIN
 #    CCSJ_PROD_CO_ACTIV_CODE ON
 #    CCSJ_PROD_SR_STUD_TERM_ACT.ACTI_ID =
 #    CCSJ_PROD_CO_ACTIV_CODE.ACTI_ID
 #    WHERE (((CCSJ_PROD_CCSJ_CO_V_NAME.DFLT_ID)='123456789') AND
 #    ((CCSJ_PROD_SR_STUD_TERM_ACT.TERM_ID)='20161') AND
 #    ((CCSJ_PROD_CO_ACTIV_CODE.ATHLETIC_FLAG)='T'))


    sql = """
    SELECT CCSJ_PROD.CO_ACTIV_CODE.ACTI_ID,
    CCSJ_PROD.CO_ACTIV_CODE.DESCR
    FROM (CCSJ_PROD.CCSJ_CO_V_NAME INNER JOIN
    CCSJ_PROD.SR_STUD_TERM_ACT ON
    CCSJ_PROD.CCSJ_CO_V_NAME.NAME_ID =
    CCSJ_PROD.SR_STUD_TERM_ACT.NAME_ID) INNER JOIN
    CCSJ_PROD.CO_ACTIV_CODE ON
    CCSJ_PROD.SR_STUD_TERM_ACT.ACTI_ID =
    CCSJ_PROD.CO_ACTIV_CODE.ACTI_ID
    WHERE (((CCSJ_PROD.CCSJ_CO_V_NAME.DFLT_ID)='{0}') AND
    ((CCSJ_PROD.SR_STUD_TERM_ACT.TERM_ID)='{1}') AND
    ((CCSJ_PROD.CO_ACTIV_CODE.ATHLETIC_FLAG)='T'))
    """.format(student_id, term)

    cursor = empower.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    result = len(list(rows))

    #TODO - modify so that uses cursor object to determine the number of rows returned instead?
    # should be more efficient

    #initialize counter to zero
    # result = 0

    #insert test for if no records returned???
    # for row in rows:
        #increment counter for each record found!
        # result += 1

    # print(rows[0])
    return result

def calculate_total_empower_attendance_records_in_term_by_student_by_code(empower, term, student_id, attendance_code):
    # created on 9/18/2017

    # SELECT CCSJ_PROD_SR_STUD_ATTEND.dept_id,
    # CCSJ_PROD_SR_STUD_ATTEND.crse_id,
    # CCSJ_PROD_SR_STUD_ATTEND.sect_id,
    # CCSJ_PROD_SR_STUD_ATTEND.ATND_DATE,
    # CCSJ_PROD_SR_STUD_ATTEND.ATND_ID
    # FROM CCSJ_PROD_SR_STUD_ATTEND INNER JOIN
    # CCSJ_PROD_CCSJ_CO_V_NAME ON
    # CCSJ_PROD_SR_STUD_ATTEND.NAME_ID =
    # CCSJ_PROD_CCSJ_CO_V_NAME.NAME_ID
    # WHERE (((CCSJ_PROD_CCSJ_CO_V_NAME.DFLT_ID) = "100098666") And
    #     ((CCSJ_PROD_SR_STUD_ATTEND.term_id) = "20151") And
    #     ((CCSJ_PROD_SR_STUD_ATTEND.ATND_ID) = "A"))
    # ORDER BY CCSJ_PROD_SR_STUD_ATTEND.dept_id,
    # CCSJ_PROD_SR_STUD_ATTEND.crse_id,
    # CCSJ_PROD_SR_STUD_ATTEND.sect_id,
    # CCSJ_PROD_SR_STUD_ATTEND.ATND_DATE;

    sql = """
    SELECT CCSJ_PROD.SR_STUD_ATTEND.dept_id,
    CCSJ_PROD.SR_STUD_ATTEND.crse_id,
    CCSJ_PROD.SR_STUD_ATTEND.sect_id,
    CCSJ_PROD.SR_STUD_ATTEND.ATND_DATE,
    CCSJ_PROD.SR_STUD_ATTEND.ATND_ID
    FROM CCSJ_PROD.SR_STUD_ATTEND INNER JOIN
    CCSJ_PROD.CCSJ_CO_V_NAME ON
    CCSJ_PROD.SR_STUD_ATTEND.NAME_ID =
    CCSJ_PROD.CCSJ_CO_V_NAME.NAME_ID
    WHERE (((CCSJ_PROD.CCSJ_CO_V_NAME.DFLT_ID) = '{0}') And
        ((CCSJ_PROD.SR_STUD_ATTEND.term_id) = '{1}') And
        ((CCSJ_PROD.SR_STUD_ATTEND.ATND_ID) = '{2}'))
    ORDER BY CCSJ_PROD.SR_STUD_ATTEND.dept_id,
    CCSJ_PROD.SR_STUD_ATTEND.crse_id,
    CCSJ_PROD.SR_STUD_ATTEND.sect_id,
    CCSJ_PROD.SR_STUD_ATTEND.ATND_DATE;
    """.format(student_id, term, attendance_code)

    cursor = empower.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    result = len(list(rows))

    # count = 0

    # for row in rows:
    #     count = count + 1

    # data = pd.read_sql(sql, empower)
    return result


def get_empower_sr_activity_data_for_student_for_term(empower, term, student_id):
    # created on 8/28/2019

    #original sql from Access
    ################################################################
    # SELECT DISTINCT CCSJ_PROD_SR_STUD_TERM_ACT.ACTI_ID
    # FROM (CCSJ_PROD_CCSJ_CO_V_NAME INNER JOIN
    #     CCSJ_PROD_SR_STUD_TERM_ACT ON
    #     CCSJ_PROD_CCSJ_CO_V_NAME.NAME_ID =
    #     CCSJ_PROD_SR_STUD_TERM_ACT.NAME_ID) INNER JOIN
    # CCSJ_PROD_CO_ACTIV_CODE ON
    # CCSJ_PROD_SR_STUD_TERM_ACT.ACTI_ID =
    # CCSJ_PROD_CO_ACTIV_CODE.ACTI_ID
    # WHERE (((CCSJ_PROD_CCSJ_CO_V_NAME.DFLT_ID)="100085633") AND
    #     ((CCSJ_PROD_SR_STUD_TERM_ACT.TERM_ID)="20191") AND
    #     ((CCSJ_PROD_CO_ACTIV_CODE.ATHLETIC_FLAG)="T"))
    # ORDER BY CCSJ_PROD_SR_STUD_TERM_ACT.ACTI_ID;

    sql = """
    SELECT DISTINCT
    CCSJ_PROD.SR_STUD_TERM_ACT.ACTI_ID
    FROM (CCSJ_PROD.CCSJ_CO_V_NAME INNER JOIN
        CCSJ_PROD.SR_STUD_TERM_ACT ON
        CCSJ_PROD.CCSJ_CO_V_NAME.NAME_ID =
        CCSJ_PROD.SR_STUD_TERM_ACT.NAME_ID) INNER JOIN
    CCSJ_PROD.CO_ACTIV_CODE ON
    CCSJ_PROD.SR_STUD_TERM_ACT.ACTI_ID =
    CCSJ_PROD.CO_ACTIV_CODE.ACTI_ID
    WHERE (((CCSJ_PROD.CCSJ_CO_V_NAME.DFLT_ID)='{0}') AND
        ((CCSJ_PROD.SR_STUD_TERM_ACT.TERM_ID)='{1}') AND
        ((CCSJ_PROD.CO_ACTIV_CODE.ATHLETIC_FLAG)='T'))
    ORDER BY CCSJ_PROD.SR_STUD_TERM_ACT.ACTI_ID
    """.format(student_id, term)

    # print(sql)

    cursor = empower.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    result = ''

    # row[0] --> ACTI_ID

    for row in rows:
        # print(row)
        # print(row[0])
        result += "{0}, ".format(row[0])

    # add code to trim the last two charcters
    result = trim_unwanted_spaces_at_end_of_string(result, 2)

    return result


def calculate_total_attendance_records(row):
    # created on 9/18/2017

    # [TotalAs]+[TotalEs]+[TotalPs]+[TotalTs]+[TotalHs]+[TotalCcs] AS TotalRecs

    result = int(row['TotalAs']) + int(row['TotalEs']) + int(row['TotalPs']) + int(row['TotalTs']) + int(row['TotalHs']) + int(row['TotalCcs'])

    return result


def calculate_total_absents_records(row):
    # created on 9/18/2017

    # [TotalAs]+[TotalEs] AS TotalAbsents

    result = int(row['TotalAs']) + int(row['TotalEs'])

    return result


# def calculate_total_attend_percentage(row):
#     # created on 9/18/2017
#
#     # =IF(L2+M2+Q2<>0,(L2+M2)/(L2+M2+Q2),"")
#
#     numerator = int(row['TotalPs']) + int(row['TotalTs'])
#     denominator = numerator + int(row['TotalAbsents'])
#
#     if denominator != 0:
#         number_result = 100 * float(numerator / denominator)
#         rounded_result = round(number_result , 0)
#         result = rounded_result
#         # result = "{0:.0f}".format(number_result)
#     else:
#         result = ""
#
#     return result

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


def calculate_total_attendance_records_for_courses_datatable(row):
    # created on 8/28/2019

    result = int(row['NumA']) + int(row['NumE']) + int(row['NumP']) + \
             int(row['NumT']) + int(row['NumH']) + int(row['NumCc'])

    return result


def calculate_total_absents_records_for_courses_datatable(row):
    # created on 8/28/2019

    result = int(row['NumA']) + int(row['NumE'])

    return result

# def calculate_total_attend_percentage_for_courses_datatable(row):
#     # created on 8/28/2019
#
#     numerator = int(row['NumP']) + int(row['NumT'])
#     denominator = numerator + int(row['NumAbsents'])
#
#     if denominator != 0:
#         number_result = 100 * float(numerator / denominator)
#         rounded_result = round(number_result , 0)
#         result = rounded_result
#         # result = "{0:.0f}".format(number_result)
#     else:
#         result = ""
#
#     return result

def calculate_absent_ratio_for_courses_datatable(row):
    # created on 9/03/2019

    # NOTE: do not count H or CC type attendance records.

    numerator = int(row['NumAbsents'])
    denominator = numerator + int(row['NumP']) + int(row['NumT'])

    if denominator != 0:
        number_result = 100 * float(numerator / denominator)
        rounded_result = round(number_result , 0)
        result = rounded_result
        # result = "{0:.0f}".format(number_result)
    else:
        result = ""

    return result


def determine_is_athlete_status(number_of_sports):
    # created on 8/28/2019

    if number_of_sports > 0:
        result = True
    else:
        result = False

    return result


def lookup_course_meet_details(empower, term, dept, crse, section):
    # created on 8/29/2019

    # SELECT CCSJ_PROD_SR_MEET_CODE.MEET_DAYS,
    # CCSJ_PROD_SR_MEET_CODE.TIME_START,
    # CCSJ_PROD_SR_MEET_CODE.TIME_END
    # FROM CCSJ_PROD_SR_CRSECT_MEET INNER JOIN
    # CCSJ_PROD_SR_MEET_CODE ON
    # CCSJ_PROD_SR_CRSECT_MEET.MEET_ID =
    # CCSJ_PROD_SR_MEET_CODE.MEET_ID
    # WHERE (((CCSJ_PROD_SR_CRSECT_MEET.TERM_ID)='{0}') AND
    #     ((CCSJ_PROD_SR_CRSECT_MEET.DEPT_ID)='{1}') AND
    #     ((CCSJ_PROD_SR_CRSECT_MEET.CRSE_ID)='{2}') AND
    #     ((CCSJ_PROD_SR_CRSECT_MEET.SECT_ID)='{3}'))

    sql = """
    SELECT CCSJ_PROD.SR_MEET_CODE.MEET_DAYS,
    CCSJ_PROD.SR_MEET_CODE.TIME_START,
    CCSJ_PROD.SR_MEET_CODE.TIME_END,
    CCSJ_PROD.SR_CRSECT_MEET.DATE_FIRST,
    CCSJ_PROD.SR_CRSECT_MEET.DATE_END
    FROM CCSJ_PROD.SR_CRSECT_MEET INNER JOIN
    CCSJ_PROD.SR_MEET_CODE ON
    CCSJ_PROD.SR_CRSECT_MEET.MEET_ID =
    CCSJ_PROD.SR_MEET_CODE.MEET_ID
    WHERE (((CCSJ_PROD.SR_CRSECT_MEET.TERM_ID)='{0}') AND
        ((CCSJ_PROD.SR_CRSECT_MEET.DEPT_ID)='{1}') AND
        ((CCSJ_PROD.SR_CRSECT_MEET.CRSE_ID)='{2}') AND
        ((CCSJ_PROD.SR_CRSECT_MEET.SECT_ID)='{3}'))
    """.format(term, dept, crse, section)

    # print(sql)
    # print('')

    cursor = empower.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    # row[0] = MEET_DAYS
    # row[1] = TIME_START
    # row[2] = TIME_END
    # row[3] = DATE_FIRST
    # row[4] = DATE_END

    if rows is None:
        # result = None
        result = ('', '', '', '', '')

    for row in rows:
        meet_days = row[0]

        if row[1] is not None:
            time_start = remove_date_from_datetime_object(row[1])
        else:
            time_start = None

        if row[2] is not None:
            time_end = remove_date_from_datetime_object(row[2])
        else:
            time_end = None

        if row[3] is not None:
            date_first = remove_time_from_datetime_object(row[3])
        else:
            date_first = None

        if row[4] is not None:
            date_end = remove_time_from_datetime_object(row[4])
        else:
            date_end = None

        result = (meet_days, time_start, time_end, date_first, date_end)

    return result


def get_empower_student_attendance_in_course(empower, term, dept, course_number, section, student_id, attendance_code):
    # created on 8/29/2019

    # revised - added attendance_code as part of WHERE
    ##################################################
    # SELECT CCSJ_PROD_SR_STUD_ATTEND.ATND_DATE
    # FROM CCSJ_PROD_SR_STUD_ATTEND INNER JOIN
    # CCSJ_PROD_CCSJ_CO_V_NAME ON
    # CCSJ_PROD_SR_STUD_ATTEND.NAME_ID =
    # CCSJ_PROD_CCSJ_CO_V_NAME.NAME_ID
    # WHERE (((CCSJ_PROD_SR_STUD_ATTEND.TERM_ID)="20182") AND
    # ((CCSJ_PROD_SR_STUD_ATTEND.DEPT_ID)="CMIS") AND
    # ((CCSJ_PROD_SR_STUD_ATTEND.CRSE_ID)="225") AND
    # ((CCSJ_PROD_SR_STUD_ATTEND.SECT_ID)="X") AND
    # ((CCSJ_PROD_CCSJ_CO_V_NAME.DFLT_ID)="100115182") AND
    # ((CCSJ_PROD_SR_STUD_ATTEND.ATND_ID)="P"))
    # ORDER BY CCSJ_PROD_SR_STUD_ATTEND.ATND_DATE DESC;

    sql = """
    SELECT CCSJ_PROD.SR_STUD_ATTEND.ATND_DATE
    FROM CCSJ_PROD.SR_STUD_ATTEND INNER JOIN
    CCSJ_PROD.CCSJ_CO_V_NAME ON
    CCSJ_PROD.SR_STUD_ATTEND.NAME_ID =
    CCSJ_PROD.CCSJ_CO_V_NAME.NAME_ID
    WHERE (((CCSJ_PROD.SR_STUD_ATTEND.TERM_ID)='{0}') AND
    ((CCSJ_PROD.SR_STUD_ATTEND.DEPT_ID)='{1}') AND
    ((CCSJ_PROD.SR_STUD_ATTEND.CRSE_ID)='{2}') AND
    ((CCSJ_PROD.SR_STUD_ATTEND.SECT_ID)='{3}') AND
    ((CCSJ_PROD.CCSJ_CO_V_NAME.DFLT_ID)='{4}') AND
    ((CCSJ_PROD.SR_STUD_ATTEND.ATND_ID)='{5}'))
    ORDER BY CCSJ_PROD.SR_STUD_ATTEND.ATND_DATE DESC
    """.format(term, dept, course_number, section, student_id, attendance_code)

    cursor = empower.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    result = len(list(rows))

    # initialize accumulator to zero
    # result = 0

    # for row in rows:
        # count up number of dates with the given attendance code!
        # result += 1

    return result
