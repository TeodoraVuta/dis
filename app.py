import streamlit as st
from PIL import Image
import base64
from dotenv import load_dotenv
import mysql.connector
import bcrypt
from streamlit_extras.switch_page_button import switch_page
from db_utils import show_logged_in_user

show_logged_in_user()

load_dotenv()

db_host = st.secrets["DB_HOST"]
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_name = st.secrets["DB_USER"]
db_port = int(st.secrets["DB_PORT"])


def get_base64_video(path):
    with open(path, 'rb') as f:
        video_bytes = f.read()
    return base64.b64encode(video_bytes).decode()



video2 = get_base64_video("resources/girlVideo.mp4")

video_gallery_html = f"""
<div style="display: flex; gap: 20px; justify-content: center;">
    <video autoplay loop muted style="width: 30%; margin-left: 320px; margin-top: -167px; margin-bottom: 10px; border-radius: 10px;">
        <source src="data:video/mp4;base64,{video2}" type="video/mp4">
    </video>
</div>
"""
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# def check_password(password, hashed):
#     return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def check_credentials(username, password, conn):
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port
        )
        cursor = conn.cursor()

        query = "SELECT password FROM login WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            stored_hash = result[0]
            return check_password(password, stored_hash)
        else:
            return False

    except mysql.connector.Error as err:
        st.error(f"Eroare la conectarea la baza de date: {err}")
        return False

def check_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception as e:
        st.error(f"Eroare la verificarea parolei: {e}")
        return False

st.markdown(
    """
    <style>
    /* Background gradient animation */
    @keyframes gradientBG {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    /* Aplicăm background pe body și containerul principal */
    body, .stApp {
        background: linear-gradient(-45deg, #a3cef1, #f7d6e0, #a3cef1, #f7d6e0);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        height: 100vh;
        margin: 0;
    }
    /* Optional: face textul un pic mai vizibil */
    .custom-text {
        border-radius: 10px;
        margin-left: 180px;
        margin-top: -400px;
        font-size: 75px;
        font-weight: bold;
        color: #34495e;  /* mai închis pentru contrast bun */
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.7);  
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([4,2])

def remove_white_background(img):
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

with col2:
    image = Image.open("my_qrcode.png")
    image = remove_white_background(image)
    st.image(image, caption="Scaneaza codul QR pentru a accesa chestionarul", width=180)
    st.markdown("Care este :rainbow[opinia ta] despre invatarea online?")
with col1:
    st.markdown(
        """
        <style>
        .custom-img {
            border-radius: 10px;
            width: 250px;
            margin-left: 50px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        '<img src="https://cdn.pixabay.com/photo/2020/09/07/00/39/virtual-learning-5550480_1280.jpg" class="custom-img">',
        unsafe_allow_html=True
    )
    
    # Videoclipul îl afișezi așa cum l-ai avut, fără modificări
    st.markdown(video_gallery_html, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .custom-img-1 {
            border-radius: 10px;
            width: 150px;
            margin-top: -100px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<img src="https://cdn.pixabay.com/photo/2021/01/10/20/53/telework-5906362_1280.jpg" class="custom-img-1">',
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="custom-text">
    EduSENSE
    </div>
    """,
    unsafe_allow_html=True
)

with col1:
    st.subheader("Autentificare")

    with st.form(key='logIn'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label='Log In')

        if submit_button:
            try:
                conn = mysql.connector.connect(
                    host=db_host,
                    user=db_user,
                    password=db_password,
                    database=db_name,
                    port=db_port
                )

                if check_credentials(username, password, conn):
                    st.success("Autentificare reușită! Bine ai revenit, " + username)
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    switch_page("user")  

                else:
                    st.error("Nume de utilizator sau parolă incorecte.")
                
                conn.close()

            except mysql.connector.Error as err:
                st.error(f"Eroare de conectare la baza de date: {err}")

    
st.title("Nu ai inca un cont? Inregistreaza-te aici!")

with st.expander("Cont nou - Înregistrează-te aici"):
    with st.form(key='signUp'):
        st.write("Completează câmpurile de mai jos pentru a crea un cont nou:")
        email = st.text_input("Email", placeholder="Introdu adresa ta de email")
        username = st.text_input("Nume utilizator nou", placeholder="Introdu un nume de utilizator")
        password = st.text_input("Parolă nouă", type="password", placeholder="Alege o parolă sigură")
        confirm_password = st.text_input("Confirmă parola", type="password", placeholder="Reintrodu parola")

        sign_up_submit = st.form_submit_button(label='Creează cont')

        if sign_up_submit:
            if not username or not password or not confirm_password:
                st.error("Te rog completează toate câmpurile.")
            elif password != confirm_password:
                st.error("Parolele nu coincid. Încearcă din nou.")
            elif len(password) < 8:
                st.error("Parola trebuie să aibă cel puțin 8 caractere.")
            elif not any(char.isdigit() for char in password):
                st.error("Parola trebuie să conțină cel puțin un caracter numeric.")
            elif not any(char.isalpha() for char in password):
                st.error("Parola trebuie să conțină cel puțin o literă.")
            elif not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/" for char in password):
                st.error("Parola trebuie să conțină cel puțin un caracter special.")
            elif any(password[i] == password[i+1] == password[i+2] for i in range(len(password) - 2)):
                st.error("Parola nu poate conține același caracter repetat de 3 ori consecutiv.")
            elif len(username) < 3 or len(username) > 20:
                st.error("Numele de utilizator trebuie să aibă între 3 și 20 de caractere.")
            elif not email or '@' not in email or '.' not in email.split('@')[-1]:
                st.error("Te rog introdu o adresă de email validă.")
            else:
                try:
                    conn = mysql.connector.connect(
                        host=db_host,
                        user=db_user,
                        password=db_password,
                        database=db_user,
                        port=db_port,
                    )
                    cursor = conn.cursor()

                    cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
                    if cursor.fetchone():
                        st.error("Acest nume de utilizator este deja folosit. Alege altul.")
                    cursor.execute("SELECT * FROM login WHERE email = %s", (email,))
                    if cursor.fetchone():
                        st.error("Acest email este deja folosit. Te rog folosește altul.")
                    else:
                        hashed_password = hash_password(password)
                        cursor.execute("INSERT INTO login (email, username, password) VALUES (%s, %s, %s)", (email, username, hashed_password))
                        conn.commit()
                except mysql.connector.Error as err:
                    st.error(f"Eroare la crearea contului: {err}")
                finally:
                    cursor.close()
                    conn.close()
                st.success(f"Cont creat cu succes pentru utilizatorul '{username}'!")





reviews_html = """
<style>
    /* Container pentru toate review-urile, fixat jos */
    .reviews-container {
        # position: fixed;
        padding-top: 20px;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(255,255,255,0.9);
        display: flex;
        gap: 15px;
        padding: 10px 20px;
        overflow-x: auto;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 9999;
    }

    /* Fiecare card review */
    .review-card {
        flex: 0 0 220px;
        background: #f0f4f8;
        border-radius: 10px;
        padding: 15px 15px 15px 60px; /* spațiu pentru poza */
        position: relative;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #34495e;
    }

    /* Poza mică în colțul stânga sus */
    .review-img {
        position: absolute;
        top: 15px;
        left: 15px;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }

    /* Username */
    .review-username {
        font-weight: bold;
        margin-bottom: 8px;
    }

    /* Culoare carduri diferite */
    .color1 { background: #d6e9f8; }
    .color2 { background: #f8e3e1; }
    .color3 { background: #e8f9e8; }
    .color4 { background: #fff4d1; }
    .color5 { background: #d9e6f2; }
</style>

<div class="reviews-container">
    <div class="review-card color1">
        <img class="review-img" src="https://randomuser.me/api/portraits/women/65.jpg" alt="user1">
        <div class="review-username">Maria92</div>
        <div>Am găsit cursurile foarte bine structurate și utile.</div>
    </div>
    <div class="review-card color2">
        <img class="review-img" src="https://randomuser.me/api/portraits/men/43.jpg" alt="user2">
        <div class="review-username">AndreiG</div>
        <div>Platforma este intuitivă și materialele sunt de calitate.</div>
    </div>
    <div class="review-card color3">
        <img class="review-img" src="https://randomuser.me/api/portraits/women/44.jpg" alt="user3">
        <div class="review-username">IoanaM</div>
        <div>Mi-a plăcut că pot învăța în ritmul meu, oricând.</div>
    </div>
    <div class="review-card color4">
        <img class="review-img" src="https://randomuser.me/api/portraits/men/20.jpg" alt="user4">
        <div class="review-username">Cristi77</div>
        <div>Recomand cu căldură pentru cei pasionați de dezvoltare personală.</div>
    </div>
    <div class="review-card color5">
        <img class="review-img" src="https://randomuser.me/api/portraits/women/30.jpg" alt="user5">
        <div class="review-username">AncaB</div>
        <div>Experiență plăcută și interactivă, foarte bine realizată.</div>
    </div>
</div>
"""

st.markdown(reviews_html, unsafe_allow_html=True)

