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

Streamlit-Survey can be installed from PyPI:
```
pip install streamlit-survey
```

## Example

Simple paged survey example with a conditional structure and a submit button:
"""
with st.expander("Survey Example:", expanded=True):
    survey = ss.StreamlitSurvey("Survey Example")
    pages = survey.pages(2, on_submit=lambda: st.success("Your responses have been recorded. Thank you!"))
    with pages:
        if pages.current == 0:
            st.write("Have you used Streamlit before?")
            used_before = survey.radio(
                "used_st_before", options=["NA", "Yes", "No"], index=0, label_visibility="collapsed", horizontal=True
            )

            if used_before == "Yes":
                st.write("How often do you use Streamlit?")
                survey.select_slider(
                    "st_frequency",
                    options=["Every Day", "Every week", "Every Month", "Once a year", "Rarely"],
                    label_visibility="collapsed",
                )
            elif used_before == "No":
                st.write("Have you used other dashboarding tools?")
                used_other = survey.radio(
                    "used_other", options=["NA", "Yes", "No"], index=0, label_visibility="collapsed", horizontal=True
                )
                if used_other == "Yes":
                    st.write("Which tools?")
                    survey.multiselect(
                        "other_tools",
                        options=["Dash", "Voila", "Panel", "Bokeh", "Plotly", "Other"],
                        label_visibility="collapsed",
                    )
        elif pages.current == 1:
            st.write("How satisfied are you with this survey?")
            survey.select_slider(
                "Overall Satisfaction",
                options=["Very Unsatisfied", "Unsatisfied", "Neutral", "Satisfied", "Very Satisfied"],
                label_visibility="collapsed",
            )

"""
## In-Depth Example

Error auditing for machine learning applications:

- https://olivierbinette-streamli-docsstandaloneerror-analysis-app-ksc1h7.streamlit.app/


## Usage Overview

The `streamlit_survey` package contains a `StreamlitSurvey` class that can be used to create and manage survey components:
"""

with st.echo():
    import streamlit_survey as ss

    survey = ss.StreamlitSurvey()

"""
Components can be added to the survey using functions similar to Streamlit's input functions:

"""
survey = ss.StreamlitSurvey("Component Examples")
with st.expander("Component examples", expanded=True):
    with st.echo(code_location="below"):
        # Likert scale
        survey.select_slider(
            "Likert scale:", options=["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], id="Q2"
        )

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
