import streamlit as st
from PIL import Image
import speech_recognition as sr
from sumapi.api import SumAPI

api = SumAPI(username='GSUINF236', password='RPXfvP2yU7v4')

mic = sr.Microphone()
r = sr.Recognizer()

#Speech recognition yapılan fonksiyon
def recog (r):
    ses = r.listen(mic,timeout=5,phrase_time_limit=5)
    yazi = r.recognize_google(ses, language="tr-tr")
    return yazi


def main():
    st.title("Turkish Speech Emotion Analysis")
    #Resim ekledim.
    image=Image.open('automatic-speech-recognition_updated.png')
    st.image(image)

    if st.button("Press and Talk"):
        with mic as source:
            r.adjust_for_ambient_noise(source)
            st.text("Arka plan gürültüsü:" + str(r.energy_threshold))
            try:
                with st.spinner("Dinliyorum..."):
                    yazi=recog(r)
                #Text'e dönüştürdüğüm cümleyi yazdırıyorum.
                st.info(yazi)
                #Duygu analizini Summarify API kullanarak yaptırıyorum.
                analysis=api.sentiment_analysis(yazi, domain='general')
                st.subheader("Emotion Analysis")
                analysis2=analysis['evaluation']
                #sonuç pozitifse succes negatifse error olarak ekrana bastırıyorum.
                if analysis2['label']=='positive':
                    st.success("POSITIVE, Score:"+ str(analysis2['score']))
                else:
                    st.error("NEGATIVE, Score:"+ str(analysis2['score']))

            #Errorleri de st.error ile bastırıyorum.
            except sr.WaitTimeoutError:
                st.error("Dinleme zaman aşımına uğradı")

            except sr.UnknownValueError:
                st.error("Ne dediğini anlayamadım")

            except sr.RequestError:
                st.error("İnternete bağlanamıyorum")



if __name__ == '__main__':
    main()


