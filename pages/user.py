import streamlit as st
from db_utils import show_logged_in_user, get_user_id_by_username, get_conn, get_or_create_topic
import pandas as pd

show_logged_in_user()

if "page" not in st.session_state:
    st.session_state.page = "select_topic"

username = st.session_state.get("username", None)

def get_all_topics():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM topics ORDER BY name")
    topics = cursor.fetchall()
    cursor.close()
    conn.close()
    return topics

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

def get_answers_for_question(question_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.answer_text, u.username, a.created_at 
        FROM answers a
        JOIN login u ON a.user_id = u.id
        WHERE a.question_id = %s
        ORDER BY a.created_at ASC
    """, (question_id,))
    answers = cursor.fetchall()
    cursor.close()
    conn.close()
    return answers

def insert_answer(question_id, user_id, answer_text, created_at):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO answers (question_id, user_id, answer_text, created_at)
        VALUES (%s, %s, %s, NOW())
    """, (question_id, user_id, answer_text, created_at))
    conn.commit()
    cursor.close()
    conn.close()

def deactivate_question(question_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE questions SET is_active = FALSE WHERE id = %s", (question_id,))
    conn.commit()
    cursor.close()
    conn.close()

def insert_feedback(user_id, feedback):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (user_id, feedback)
        VALUES (%s, %s)
    """, (user_id, feedback))
    conn.commit()
    cursor.close()
    conn.close()

def create_feedback():
    st.subheader("Adaugă un feedback despre această aplicație")
    feedback = st.text_area("Aici:")
    if st.button("Trimite feedback"):
        if feedback.strip() != "":
            if "username" in st.session_state:
                user_id = get_user_id_by_username(st.session_state["username"])
                if user_id:
                    insert_feedback(user_id, feedback.strip())
                    st.success("Mulțumim pentru feedback!")
                else:
                    st.error("Utilizatorul nu a fost găsit.")
            else:
                st.warning("Trebuie să fii autentificat pentru a trimite feedback.")
        else:
            st.warning("Te rugăm să completezi feedback-ul înainte de a trimite.")

# Verifică dacă utilizatorul e logat
if not username:
    st.warning("⚠️ Nu ești conectat. Click aici pentru a te conecta: [Conectare](./app)")
    st.stop()

user_id = get_user_id_by_username(username)

# Pagina de selectare subiect
if st.session_state.page == "select_topic":
    st.title("📌 Pune o întrebare")
    st.markdown("### 🔍 Alege un subiect:")

    topics = get_all_topics()
    num_cols = 4
    cols = st.columns(num_cols)

    for i, (tid, name) in enumerate(topics):
        col = cols[i % num_cols]
        with col:
            if st.button(name, key=f"topic_{tid}"):
                st.session_state.selected_topic_id = tid
                st.session_state.selected_topic_name = name
                st.session_state.page = "topic_questions"
                st.rerun()

    st.markdown("---")
    st.markdown("### ➕ Adaugă un subiect nou")
    new_topic = st.text_input("Nume subiect nou", placeholder="Ex: Machine Learning")
    if st.button("Adaugă subiect"):
        topic_names = [name.lower() for (_, name) in topics]
        if not new_topic.strip():
            st.error("⚠️ Introdu un nume valid.")
        elif new_topic.strip().lower() in topic_names:
            st.warning("🔁 Subiectul există deja.")
        else:
            topic_id = get_or_create_topic(new_topic.strip())
            st.success(f"✅ Subiectul „{new_topic}” a fost adăugat!")
            st.rerun()
    
    create_feedback()


    

# Pagina întrebărilor pentru un subiect
elif st.session_state.page == "topic_questions":
    selected_topic_id = st.session_state.selected_topic_id
    selected_topic_name = st.session_state.selected_topic_name

    st.title(f"📋 Întrebări pentru subiectul: {selected_topic_name}")

    questions = get_questions_for_topic(selected_topic_id)
    if questions:
        for i, (question_id, q_text, q_user_id, is_active) in enumerate(questions):
            st.markdown(f"#### ❓ Întrebarea {i+1}: {q_text}")
            
            if not is_active:
                st.warning("🔒 Această întrebare a fost dezactivată de autor. Nu se mai pot adăuga răspunsuri.")

            answers = get_answers_for_question(question_id)
            if answers:
                for ans_text, ans_user, ans_time in answers:
                    st.markdown(f"🗨️ **{ans_user}** ({ans_time.strftime('%Y-%m-%d %H:%M')}): {ans_text}")
            else:
                st.markdown("ℹ️ Nu există răspunsuri încă.")

            if is_active:
                with st.form(f"answer_form_{question_id}"):
                    user_answer = st.text_area("Răspunsul tău", key=f"answer_input_{question_id}")
                    submitted = st.form_submit_button("Trimite răspunsul")
                    if submitted:
                        if not user_answer.strip():
                            st.warning("⚠️ Nu poți trimite un răspuns gol.")
                        else:
                            insert_answer(user_id, question_id, user_answer.strip())
                            st.success("✅ Răspunsul tău a fost trimis.")
                            st.rerun()

            if user_id == q_user_id and is_active:
                if st.button("🔒 Dezactivează întrebarea", key=f"deactivate_{question_id}"):
                    deactivate_question(question_id)
                    st.success("✅ Întrebarea a fost dezactivată.")
                    st.rerun()

            st.markdown("---")
    else:
        st.info("Nu există întrebări pentru acest subiect încă.")

    st.subheader("✍️ Pune o întrebare nouă")
    question_text = st.text_area("Scrie întrebarea ta:")

    if st.button("Adaugă întrebare"):
        if not question_text.strip():
            st.error("⚠️ Întrebarea nu poate fi goală.")
        else:
            insert_question(user_id, selected_topic_id, question_text.strip())
            st.success("✅ Întrebarea a fost adăugată!")
            st.rerun()

    if st.button("⬅️ Înapoi la selecția subiectului"):
        st.session_state.page = "select_topic"
        st.rerun()

    create_feedback()

