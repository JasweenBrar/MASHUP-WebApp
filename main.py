import streamlit as st
from utils.sendmail import send_email
from utils.constants import (SMTP_SERVER_ADDRESS,PORT,SENDER_PASSWORD,SENDER_ADDRESS)
from utils.mashup import MASHUP
import pandas as pd
import numpy as np
import requests     
from streamlit_lottie import st_lottie


st.set_page_config(page_title="MASHUP",)
st.title('Mashup-Jasween-102017187')

# To put up animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_music = "https://assets10.lottiefiles.com/packages/lf20_b8ofyxmg.json"

st_lottie(load_lottieurl(lottie_music), height=200)

def check(singerName,Num,Ysec,email):
    if singerName == '' or Num == '' or Ysec == '' or email == '':
        st.error('Please fill all the fields')
        return False
    else:
        return True 


if __name__ == '__main__':
    
    # Creating email form
    with st.form("Email Form"):
        singerName = st.text_input(label='Singer Name', placeholder="Satinder Sartaaj")
        Num = st.text_input(label='No. of videos',placeholder="10")
        Ysec = st.text_input(label='Duration of each video',placeholder="20")
        email = st.text_input(label='Email', placeholder="sample@gmail.com")
        submit_res = st.form_submit_button('Submit')


    if (check(singerName,Num,Ysec,email) == True):
        if submit_res:
            result_file = MASHUP(singerName,Num,Ysec)
            fullName = "Jasween Kaur Brar"
            subject = "MASHUP File"
            message = """Sender Full Name: {} \n\n""".format(fullName)
            send_email(sender=SENDER_ADDRESS, password=SENDER_PASSWORD,
            receiver=email, smtp_server=SMTP_SERVER_ADDRESS, smtp_port=PORT,
            email_message=message, subject=subject, attachment=result_file)

