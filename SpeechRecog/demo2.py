import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
from sumapi.api import SumAPI

api = SumAPI(username='GSUINF236', password='RPXfvP2yU7v4')
st.title("Duygu Analizi Web Uygulaması")
image=Image.open('automatic-speech-recognition_updated.png')
st.image(image)

stt_button = Button(label="Bas-Konuş", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        ipt=result.get("GET_TEXT")
        analysis=api.sentiment_analysis(ipt, domain='general')
        st.subheader("Speech -> Text")
        st.info(ipt)
        st.subheader("Emotion Analysis")
        analysis2=analysis['evaluation']
        
        if analysis2['label']=='positive':
            st.success("POSITIVE, Score:"+ str(analysis2['score']))
        else:
            st.error("NEGATIVE, Score:"+ str(analysis2['score']))