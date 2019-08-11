def convert_grade(grade):
    if grade == 'Juv':
        grade = 'juv'
    if grade == 'Nov A':
        grade = 'Nov%20A'
    if grade == 'Nov B':
        grade = 'Nov%20B'
    return grade