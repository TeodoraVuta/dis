import streamlit as st
from PIL import Image
import base64

def get_base64_video(path):
    with open(path, 'rb') as f:
        video_bytes = f.read()
    return base64.b64encode(video_bytes).decode()

def next_page():
    st.session_state.page += 1

video2 = get_base64_video("resources/girlVideo.mp4")  

video_gallery_html = f"""
<div style="display: flex; gap: 20px; justify-content: center;">
    <video autoplay loop muted style="width: 30%; margin-left: 320px; margin-top: -220px; margin-bottom: 10px; border-radius: 10px">
        <source src="data:video/mp4;base64,{video2}" type="video/mp4">
    </video>
</div>
"""

col1, col2 = st.columns([4,2])

with col2:
    image = Image.open("my_qrcode.png")
    st.image(image, caption="Scaneaza codul QR pentru a accesa chestionarul", width=200)
    st.text("Care este opinia ta despre invatarea online?")    



with col1:
    st.image("resources/img1.jpg", width=300) 
    st.markdown(video_gallery_html, unsafe_allow_html=True)
    
    with st.form(key='logIn'):
        st.text_input("Username")
        st.text_input("Password", type="password")
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button(label='Log In')
        with col2:
            submit_button = st.form_submit_button(label='Forgot Password')

st.title("Nu ai inca un cont? Inregistreaza-te aici!")

with st.popover("Cont nou"):
        with st.form(key='signUp'):
            st.text_input("Nume utilizator nou")
            st.text_input("Parolă nouă", type="password")
            st.text_input("Confirmă parola", type="password")
            sign_up_submit = st.form_submit_button(label='Creează cont')
            if sign_up_submit:
                st.success("Cont creat cu succes!")
        

                