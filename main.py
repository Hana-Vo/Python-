import os
import random

pip install bottle 

from bottle import route, run, template, request, static_file
from app_logic import check_credentials, insert_user_input, \
    find_similar_records, insert_possible_matches, \
    get_match_by_id, get_subject_by_id, get_input_by_id, update_possible_matches, get_session_by_id


@route('/static/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='static/')


@route('/')
def index():
    return template('static/login.html', message='Enter login and password.')


@route('/', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_credentials('database/database.db', username, password):
        return template('static/welcome.html', username=username)
    else:
        return template('static/login.html', message='Invalid username or password')


@route('/submit_data', method='GET')
def data_input():
    return template('static/data.html', message='Enter data to find subjects.')


@route('/submit_data', method='POST')
def submit_data():
    first_name = request.forms.get('first_name')
    surname = request.forms.get('surname')
    dob = request.forms.get('dob')
    nationality = request.forms.get('nationality')
    id_user_input = random.randint(1, 999999999)
    user_login = 'User_1'

    insert_user_input(id_user_input, first_name, surname, dob, nationality, user_login)
    threshold = 0.5
    similar_records = find_similar_records(first_name, surname, dob, nationality, threshold)
    if not similar_records:
        return template('static/data.html', message='No subjects found.')
    else:
        id_session = random.randint(1, 999999999)
        for record in similar_records:
            id_match = record[0][5]
            id_subject = record[0][0]
            result = 'unknown'
            reason = 'unknown'
            insert_possible_matches(id_match, id_subject, id_user_input, result, reason, id_session)
        return template('static/matches.html',
                        similar_records=similar_records)


@route('/matches/<id_session>')
def choose_element(id_session):
    ids_subject = get_session_by_id(id_session)
    similar_records = []
    for subject_id in ids_subject:
        subject = get_subject_by_id(subject_id[0])
        match = subject_id[1]
        subject = list(subject)
        subject.append(match)
        similar_records.append(subject)
    return template('static/matches_id.html', similar_records=similar_records, id_session=id_session)


@route('/subject_details/<id_match>')
def element_detail(id_match):
    match_data = get_match_by_id(id_match)
    id_subject = get_match_by_id(id_match)[1]
    id_session = get_match_by_id(id_match)[5]
    element = get_subject_by_id(id_subject)
    return template('static/subject_details.html', element=element, id_session=id_session)


@route('/subject_details/<id_match>', method='POST')
def insert_detail(id_match):
    match_data = get_match_by_id(id_match)
    id_subject = get_match_by_id(id_match)[1]
    id_user_input = get_match_by_id(id_match)[2]
    id_session = get_match_by_id(id_match)[5]

    element = get_subject_by_id(id_subject)
    user_input = get_input_by_id(id_user_input)

    result = request.forms.get('decision')
    reason = request.forms.get('reason')
    update_possible_matches(id_match, result, reason)
    return template('static/subject_details.html', element=element, id_session=id_session)


@route('/summary')
def summary():
    id_session = request.query.id_session
    matches = get_session_by_id(id_session)
    return template('static/summary.html', matches=matches)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)
