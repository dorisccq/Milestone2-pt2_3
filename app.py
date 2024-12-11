import streamlit as st
import openai
from dotenv import load_dotenv
import os
load_dotenv()

from utils.tts import get_tts, post_tts_job
from utils.llm import get_ans
from utils.picgen import sample_block_call
st.sidebar.title('Hello I am CHIIKANA AI')
import time

from PIL import Image
import requests
import io

st.image("./sources/IMG_1222.GIF", caption="Baby I am here for you ~")


st.sidebar.header('Q&A')
question = st.sidebar.text_input('Input any questions here')
tone = st.sidebar.selectbox(
    "choose a tone to communicate",
    ( "bestie", "parent","sis/bro","peer","lover","pet")
)

if st.sidebar.button("Submit"):
    if tone == "bestie":
        st.sidebar.write("Bestie Tone")
        question +='please answer me as you are my bestie.'

    if tone == "parent":
        st.sidebar.write ("Parent Tone")
        question +='please answer me as you are my parent.'

    if tone == "sis/bro":
        st.sidebar.write ("Sis/Bro Tone")
        question +='please answer me as you are my sister or brother.'

    if tone == "peer":
        st.sidebar.write ("Peer Tone")
        question +='please answer me as you are my peer, like my peer in school.'

    if tone == "lover":
        st.sidebar.write ("Lover Tone")
        question +='please answer me as you are my lover, my darling, my sweetheart.'

    elif tone == "pet":
        st.sidebar.write("Pet Tone")
        question +='please answer me as my pet -- a cat/dog'
    
    answer = get_ans(question)
    
    st.write(answer)
    try:
        with st.spinner('Generating audio...'):
            print('play audio')
            t = int(time.time())
            audio_bytes = get_tts(answer,t)
            st.audio(audio_bytes, format='audio/wav')
            st.success('Audio played!')
    except Exception as e:
        print(e)


st.sidebar.header('Image for Ya')

question_pic = st.sidebar.text_input('Enter what pic you want today')
    
if st.sidebar.button("generate picture"):
    with st.spinner("Generating picture..."):
        try:
            # Prepare the data and files for the POST request
            
            # Send POST request to the image service
            picbyte = sample_block_call(question_pic)
            st.image(picbyte, caption='picture', use_column_width=True)
        except:
            pass