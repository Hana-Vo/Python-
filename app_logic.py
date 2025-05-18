import difflib
import sqlite3
import random


def execute_dml(db_file, script_path):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    with open(script_path, 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()
    conn.close()


def execute_dql(db_file, script_path):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    with open(script_path, 'r') as f:
        sql = f.read()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def check_credentials(db_file, username, password):
    """ Check if the given username and password exist in the database"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, password FROM credentials WHERE user_name = ? AND password = ?",
                   (username, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False


def insert_user_input(id_user_input, first_name, surname, dob, nationality, user_login):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_input (id_user_input, first_name, surname, birth_date, nationality, user_login) "
                   "VALUES (?,?,?,?,?,?)", (id_user_input, first_name, surname, dob, nationality, user_login))
    conn.commit()
    conn.close()


def find_similar_records(first_name, surname, dob, nationality, threshold):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_subject, first_name, surname, birth_date, nationality FROM subject")
    records = cursor.fetchall()
    similar_records = []
    for record in records:
        sequence = difflib.SequenceMatcher(a=record[1:], b=(first_name, surname, dob, nationality))
        ratio = sequence.ratio()
        if ratio >= threshold:
            match_id = random.randint(1, 999999999)
            record = list(record)
            record.append(match_id)
            similar_records.append((record, ratio))

    similar_records = sorted(similar_records, key=lambda x: x[1], reverse=True)
    conn.close()
    return similar_records[:3]


def insert_possible_matches(id_match, id_subject, id_user_input, result, reason, id_session):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO possible_match (id_match, id_subject, id_user_input, result, reason, id_session) "
                   "VALUES (?,?,?,?,?,?)", (id_match, id_subject, id_user_input, result, reason, id_session))
    conn.commit()
    conn.close()


def update_possible_matches(id_match, result, reason):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE possible_match SET result = ?, reason = ? WHERE id_match = ?",
                   (result, reason, id_match))
    conn.commit()
    conn.close()


def get_match_by_id(id_match):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_match, id_subject, id_user_input, result, reason, id_session FROM possible_match WHERE "
                   "id_match = ?",
                   (id_match,))
    result = cursor.fetchone()
    conn.close()
    return result


def get_session_by_id(id_session):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_subject, id_match, result, reason FROM possible_match WHERE "
                   "id_session = ?",
                   (id_session,))
    result = cursor.fetchall()
    conn.close()
    return result


def get_subject_by_id(id_subject):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_subject, first_name, surname, birth_date, nationality, category FROM subject WHERE "
                   "id_subject = ?",
                   (id_subject,))
    result = cursor.fetchone()
    conn.close()
    return result


def get_input_by_id(id_user_input):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_user_input, first_name, surname, birth_date, nationality FROM user_input WHERE "
                   "id_user_input = ?",
                   (id_user_input,))
    result = cursor.fetchone()
    conn.close()
    return result
