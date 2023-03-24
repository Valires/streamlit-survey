import streamlit as st
import streamlit_survey as ss

st.write("## Welcome to Streamlit Survey")

survey = ss.StreamlitSurvey()

thumb = survey.thumbs("Thumbs:")
faces = survey.faces("Faces:")
text = survey.text_input("Text input:")
area = survey.text_area("Area input:")
multichoice = survey.multichoice(
    "Multiple choice:", options=["Option 1", "Option 2", "Option 3", "etc"]
)
selectbox = survey.selectbox(
    "Select box:", options=["Option 1", "Option 2", "Option 3", "etc"]
)
radio = survey.radio("Radio:", options=["Option 1", "Option 2", "Option 3", "etc"])
checkbox = survey.checkbox("Check box")
dateinput = survey.dateinput("Date input:")
timeinput = survey.timeinput("Time input:")

st.write("### Current survey state:")
st.json(survey.to_json())

st.write("### Current session state:")
st.json(st.session_state)
