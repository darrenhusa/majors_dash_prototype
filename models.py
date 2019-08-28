# models.py

import pandas as pd
import re


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

    cursor = empower.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

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


def classify_empower_major_codes_into_programs(major_code):
    # created on 7/16/2019

    if isBlank(major_code):
        return ''

    # print(col)

    if major_code == 'A105' or major_code == '0105':
        #Accounting
        program = "Acct"
    elif major_code == '4500' or major_code == '4503':
        # Kinesiology/Biokinetics
        program = "Kines/Biok"
    elif major_code == '4501':
        # Biomedical Science
        program = "Biomed"
    elif major_code == 'A205' or major_code == '2205' or major_code == 'J305':
        # Business Management
        program = "Bmt"
    elif major_code == 'A705' or major_code == 'A605' or major_code == '0905' or major_code == '0805':
        #strProgram = "CIS"
        program = "CIS"
    elif major_code == '0705' or major_code == '1505' or major_code == '1506' or major_code == 'A505':
        #strProgram = "Communications"
        program = "Comm"
    elif major_code == 'A805' or major_code == '1005' or major_code == 'J505':
        #strProgram = "Criminal Justice"
        program = "CriJ"
    elif major_code == '1405' or major_code == '5505' or major_code == '5305' or major_code == 'J605':
        #strProgram = "Digital Studio Arts/MFA"
        program = "DSA/MFA"

    elif major_code == '1205' or major_code == '3005' or major_code == '6805' or major_code == '6815':
        #strProgram = "Education"
        program = "Educ"
    elif major_code == 'A905' or major_code == '1305' or major_code == '1306' or major_code == '1307':
        #strProgram = "English"
        program = "Eng"
    elif major_code == '4502':
        # Forensic Biotechnology
        program = "FrnsBio"
    elif major_code == '4504':
        # Forensic Science
        program = "FrnsSci"
    elif major_code == '1705' or major_code == 'B105':
        #strProgram = "General Studies"
        program = "GenStud"
    elif major_code == '1706' or major_code == 'B104':
        #strProgram = "Integrated Studies"
        program = "IntStud"
    elif major_code == 'D101' or major_code == '3305':
        #strProgram = "General Science"
        program = "GenSci"
    elif major_code == 'C104' or major_code == '4905':
        #strProgram = "Human Services"
        program = "HSv"
    elif major_code == 'B106' or major_code == '2005':
        #strProgram = "Humanities"
        program = "Hum"
    elif major_code == 'B306' or major_code == '4910' or major_code == '4805' or major_code == '4806' or major_code == 'B305' or major_code == 'J705' or major_code == 'B303':
        #strProgram = "Legal/Paralegal Studies"
        program = "LSCC/PS"
    elif major_code == '2805' or major_code == '6910' or major_code == 'B905' or major_code == 'B505':
        #strProgram = "Psychology"
        program = "Psyc"
    elif major_code == '3205':
        #strProgram = "Social Science"
        program = "SocS"
    elif major_code == '3606' or major_code == '3805' or major_code == '3605' or major_code == 'B405' or major_code == 'J805':
        #strProgram = "Theology/Religious Studies"
        program = "Theo/RlSt"
    elif major_code == '9805':
        program = "Und"
    elif major_code == '9905':
        #not applicable/non-degree
        program = "NA"

    #dcp programs
    elif major_code == '2405':
        program = "OrMn"
    elif major_code == '5805' or major_code == '6005':
        program = "LEM/PSM"

    #graduate programs
    elif major_code == '6705' or major_code == '7605':
        program = "QA/Mn"
    elif major_code == '6905':
        program = "LEA/PSA"

    else:
        program = '<<OTHER>>'

    return program


def isBlank(myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True
