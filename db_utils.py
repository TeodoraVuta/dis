from dotenv import load_dotenv
import streamlit as st
from country_list import countries_for_language
import mysql.connector
import os

load_dotenv()

db_host = st.secrets["DB_HOST"]
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_name = st.secrets["DB_NAME"]
db_port = int(st.secrets["DB_PORT"])

st.set_page_config(page_title="survey", page_icon="📋", layout="centered")

def get_conn():
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_user,
        port=db_port,
    )
    return conn

def get_connection():
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_user,
        port=db_port,
    )

    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS responses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            age INT,
            gender VARCHAR(50),
            country VARCHAR(100),
            education VARCHAR(100),
            selected_platforms TEXT,
            selected_courses TEXT,
            preference VARCHAR(100),
            selected_usage TEXT,
            job VARCHAR(1000),
            mandatory VARCHAR(10),
            promotion VARCHAR(10),
            reasons_for_choosing_course TEXT,
            check_lectures VARCHAR(10),
            check_exams VARCHAR(10),
            grade_before FLOAT,
            max_grade_before FLOAT,
            grade_after FLOAT,
            max_grade_after FLOAT,
            learning_method VARCHAR(100),
            frequency VARCHAR(100),
            payed_courses VARCHAR(10),
            payment INT,
            best_course VARCHAR(500),
            dropout_status VARCHAR(10),
            dropout_reason VARCHAR(100),
            completion_rate VARCHAR(50),
            certification VARCHAR(100),
            notes TEXT,
            multitasking VARCHAR(50),
            vr_usage VARCHAR(10),
            live_interaction VARCHAR(10),
            immersive_learning VARCHAR(10),
            replacement VARCHAR(10),
            ai_assistant VARCHAR(10),
            ai_professor VARCHAR(10),
            about_course TEXT,
            specific_course TEXT,
            submission_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

    return conn, cursor  
    
def close_connection(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def show_logged_in_user():
    if "username" in st.session_state:
        # folosim un container cu 2 coloane, partea dreaptă afișează user-ul
        col1, col2 = st.columns([9,1])
        with col2:
            st.markdown(
                f"<div style='text-align: right; font-weight: bold;'>👤 {st.session_state['username']}</div>",
                unsafe_allow_html=True
            )

def get_user_id_by_username(username):
    conn, cursor = get_connection()
    cursor.execute("SELECT id FROM login WHERE username = %s", (username,))
    result = cursor.fetchone()
    close_connection(conn, cursor)
    
    if result:
        return result[0]
    else:
        return None
    

def get_or_create_topic(topic_name):
    conn, cursor = get_connection()
    cursor.execute("SELECT id FROM topics WHERE name = %s", (topic_name,))
    result = cursor.fetchone()
    
    if result:
        topic_id = result[0]
    else:
        cursor.execute("INSERT INTO topics (name) VALUES (%s)", (topic_name,))
        conn.commit()
        topic_id = cursor.lastrowid
    
    close_connection(conn, cursor)
    return topic_id


def get_answers_for_question(question_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.answer_text, u.username, a.created_at 
        FROM answers a
        JOIN users u ON a.user_id = u.id
        WHERE a.question_id = %s
        ORDER BY a.created_at ASC
    """, (question_id,))
    answers = cursor.fetchall()
    cursor.close()
    conn.close()
    return answers

def insert_question(user_id, topic_id, question_text):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO questions (user_id, topic_id, question_text)
        VALUES (%s, %s, %s)
    """, (user_id, topic_id, question_text))
    conn.commit()
    cursor.close()
    conn.close()


def get_my_questions_for_topic(topic_id, only_mine=False, user_id=None):
    conn = get_conn()
    cursor = conn.cursor()
    if only_mine and user_id:
        cursor.execute("""
            SELECT id, question_text, user_id, is_active 
            FROM questions 
            WHERE topic_id = %s AND user_id = %s 
            ORDER BY id DESC
        """, (topic_id, user_id))
    else:
        cursor.execute("""
            SELECT id, question_text, user_id, is_active 
            FROM questions 
            WHERE topic_id = %s 
            ORDER BY id DESC
        """, (topic_id,))
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    return questions

def get_answers_for_question(question_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, a.answer_text, u.username, a.created_at 
        FROM answers a
        JOIN login u ON a.user_id = u.id
        WHERE a.question_id = %s
        ORDER BY a.created_at ASC
    """, (question_id,))
    answers = cursor.fetchall()
    cursor.close()
    conn.close()
    return answers


# def insert_answer(user_id, question_id, answer_text):
#     conn = get_conn()
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO answers (user_id, question_id, answer_text, created_at)
#         VALUES (%s, %s, %s, NOW())
#     """, (user_id, question_id, answer_text))
#     conn.commit()
#     cursor.close()
#     conn.close()

def deactivate_question(question_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE questions SET is_active = FALSE WHERE id = %s", (question_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_questions_for_topic(topic_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, question_text, user_id, is_active 
        FROM questions 
        WHERE topic_id = %s 
        ORDER BY id DESC
    """, (topic_id,))
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    return questions

def save_feedback(user_id, feedback):
    conn, cursor = get_connection()
    cursor.execute("""
        INSERT INTO feedback (user_id, feedback)
        VALUES (%s, %s)
    """, (user_id, feedback))
    conn.commit()
    # close_connection(conn, cursor)

def get_feedbacks(limit=5):
    conn, cursor = get_connection()
    cursor.execute("""
       SELECT l.username, f.feedback
        FROM feedback AS f
        JOIN login AS l
            ON f.user_id = l.id
        ORDER BY f.id DESC
        LIMIT %s
    """, (limit,))
    reviews = cursor.fetchall()
    return reviews


def insert_notification(user_id, question_id, message):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notifications (user_id, question_id, seen, message)
        VALUES (%s, %s, FALSE, %s)
    """, (user_id, question_id, message))
    conn.commit()
    cursor.close()
    conn.close()

def get_unread_notifications(user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, message, question_id FROM notifications 
    WHERE user_id = %s AND seen = FALSE
    ORDER BY id DESC
""", (user_id,))
    notifications = cursor.fetchall()
    cursor.close()
    conn.close()
    return notifications

def mark_notifications_as_read(notification_ids):
    if not notification_ids:
        return
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE notifications SET seen = TRUE WHERE id IN %s",
        (tuple(notification_ids),)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_all_topics():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM topics ORDER BY name")
    topics = cursor.fetchall()
    cursor.close()
    conn.close()
    return topics




def insert_answer(question_id, user_id, answer_text):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO answers (question_id, user_id, answer_text)
        VALUES (%s, %s, %s)
    """, (question_id, user_id, answer_text))

    cursor.execute("SELECT user_id FROM questions WHERE id = %s", (question_id,))
    question_owner = cursor.fetchone()
    if question_owner and question_owner[0] != user_id:
        message = f"Ai primit un răspuns nou la întrebarea ta."
        cursor.execute("""
            INSERT INTO notifications (user_id, question_id, message, seen)
            VALUES (%s, %s, %s, FALSE)
        """, (question_owner[0], question_id, message))

    conn.commit()
    cursor.close()
    conn.close()

def mark_notifications_as_read(notification_ids):
    if not notification_ids:
        return
    conn = get_conn()
    cursor = conn.cursor()
    
    format_strings = ','.join(['%s'] * len(notification_ids))
    query = f"UPDATE notifications SET seen = TRUE WHERE id IN ({format_strings})"
    cursor.execute(query, tuple(notification_ids))
    
    conn.commit()
    cursor.close()
    conn.close()
