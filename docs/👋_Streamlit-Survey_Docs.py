import streamlit as st

import streamlit_survey as ss

st.set_page_config(
    page_title="Streamlit-Survey Documentation",
    page_icon="👋",
)

"""
# Streamlit-Survey Documentation

**Streamlit-Survey** is a Python package for incorporating surveys and structured feedback into [Streamlit](https://streamlit.io) apps.

It can be used with [Trubrics](https://github.com/trubrics/trubrics-sdk) to collect feedback on datasets, models, and machine learning apps.

## Installation

Streamlit-Survey can be installed from Github:
```
pip install git+https://github.com/OlivierBinette/streamlit-survey.git
```

## Usage

The `streamlit_survey` package contains a `StreamlitSurvey` class that can be used to create and manage survey components:
"""

with st.echo():
    import streamlit_survey as ss

    survey = ss.StreamlitSurvey()

"""
Components can be added to the survey using functions similar to Streamlit's input functions:

"""
with st.expander("Component examples", expanded=True):
    with st.echo(code_location="below"):
        # Radio buttons
        survey.radio("Thumbs up/down:", options=["NA", "👍", "👎"], horizontal=True, id="Q1")

    with st.echo(code_location="below"):
        # Likert scale
        survey.radio("Likert scale:", options=["NA", "😞", "🙁", "😐", "🙂", "😀"], horizontal=True, id="Q2")

    with st.echo(code_location="below"):
        # Text input
        survey.text_input("Text input:", id="Q3")

"""
The survey automatically gives each component a unique ID. Survey component labels and values are stored in the `survey.data` dictionary, which can be saved to a JSON file using the `survey.to_json` method:
"""
with st.echo(code_location="above"):
    json = survey.to_json()
    st.json(json)

"""
## Features

Survey components are similar to Streamlit inputs, but they have additional features that make them suitable for surveys:

- Questions and responses are automatically saved.
- Component states and previous responses are automatically restored and displayed based on survey data.
- Survey can be saved to and loaded from JSON files.
- Custom survey components can be created for more complex input UI and functionality.


## Learn More

- [Survey Components Documentation](https://olivierbinette-streamlit-surv-docs-streamlit-survey-docs-hu1jf8.streamlit.app/~/+/Survey_Components)
- [Advanced Usage](https://olivierbinette-streamlit-surv-docs-streamlit-survey-docs-hu1jf8.streamlit.app/~/+/Advanced_Usage)

"""
