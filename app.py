import streamlit as st
from PIL import Image
import base64

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

# Inject CSS for full-page animated gradient background
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
        # Schimbă pragul după cum trebuie, aici e un exemplu
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            # devine transparent
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
    with st.form(key='logIn'):
        st.text_input("Username")
        st.text_input("Password", type="password")
        c1, c2 = st.columns(2)
        with c1:
            submit_button = st.form_submit_button(label='Log In')
        with c2:
            submit_button = st.form_submit_button(label='Forgot Password')

st.title("Nu ai inca un cont? Inregistreaza-te aici!")

with st.expander("Cont nou - Înregistrează-te aici"):
    with st.form(key='signUp'):
        st.write("Completează câmpurile de mai jos pentru a crea un cont nou:")
        username = st.text_input("Nume utilizator nou", placeholder="Introdu un nume de utilizator")
        password = st.text_input("Parolă nouă", type="password", placeholder="Alege o parolă sigură")
        confirm_password = st.text_input("Confirmă parola", type="password", placeholder="Reintrodu parola")

        sign_up_submit = st.form_submit_button(label='Creează cont')

        if sign_up_submit:
            if not username or not password or not confirm_password:
                st.error("Te rog completează toate câmpurile.")
            elif password != confirm_password:
                st.error("Parolele nu coincid. Încearcă din nou.")
            else:
                # Aici poți pune logica de creare cont
                st.success(f"Cont creat cu succes pentru utilizatorul '{username}'!")





