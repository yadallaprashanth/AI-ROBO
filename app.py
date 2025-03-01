import streamlit as st
import requests
import os
import PyPDF2
from gtts import gTTS
import base64

# Your OpenWeatherMap API Key
API_KEY = '3ec136d4c475adee4efe3c3219d70892'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Virtual Assistant Name
va_name = 'Atom'

# Function to Convert Text to Speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    with open("response.mp3", "rb") as file:
        audio_bytes = file.read()
    return audio_bytes

# Function to Fetch Weather
def get_weather(city):
    try:
        params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
        response = requests.get(WEATHER_URL, params=params)
        data = response.json()

        if data['cod'] == 200:
            city_name = data['name']
            weather_desc = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"The weather in {city_name} is {weather_desc} with a temperature of {temp}°C."
        else:
            return "Could not retrieve weather information."
    except Exception as e:
        return "Error fetching weather data."

# Function to Read PDF
def read_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return "Error reading the PDF."

# Streamlit UI
st.title("🔊 Atom - AI Assistant")
st.write("Type your command below:")

user_input = st.text_input("Enter command:", "")

if user_input:
    if "weather in" in user_input.lower():
        city = user_input.replace("weather in", "").strip()
        result = get_weather(city)
        st.write(result)
        st.audio(text_to_speech(result))

    elif "search for" in user_input.lower():
        query = user_input.replace("search for", "").strip()
        st.markdown(f"[Search Google for {query}](https://www.google.com/search?q={query})")

    elif "read pdf" in user_input.lower():
        pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if pdf_file is not None:
            pdf_text = read_pdf(pdf_file)
            st.text_area("PDF Content:", pdf_text)
            st.audio(text_to_speech(pdf_text[:500]))  # Read first 500 characters

    elif "play" in user_input.lower():
        audio_file = st.file_uploader("Upload an MP3 file", type=["mp3"])
        if audio_file is not None:
            st.audio(audio_file)

    else:
        st.write("Command not recognized.")
        st.audio(text_to_speech("Sorry, I did not understand that command."))
