import streamlit as st

import streamlit_survey as ss

st.set_page_config(
    page_title="Streamlit Survey Components",
    page_icon="🗃️",
)

"""
# Advanced Usage

**Streamlit-Survey** supports conditional survey structures and survey state restoration.

## Conditional Survey Structures

Conditional survey structures can be used to create surveys with branching logic. The survey components can be grouped into sections, which can be shown or hidden based on the values of other components.

The simplest way to create a condition is to query the value of a survey component. For example, to show a text input component only if the user selects "👍" from a radio component, you can use the following code:
"""

with st.expander("Code Example", expanded=True):
    with st.echo(code_location="below"):
        survey = ss.StreamlitSurvey("Survey 1")
        Q1 = survey.radio("Thumbs up/down:", options=["NA", "👍", "👎"], horizontal=True, id="Q1")
        if Q1 == "👍":
            Q1_1 = survey.text_input("Why did you select '👍'?", id="Q1_1")

"""

When using conditional survey structures, we recommend manually specifying the `id` parameter. Otherwise, the automatic ID assignment may cause inconsistent question IDs across surveys due to the branching path.

Alternatively, you can specify all questions in advance as `SurveyComponent` instances and use the `display()` function to display the question where appropriate. This separates defining questions from the display logic. For example:
"""
with st.expander("Code Example", expanded=True):
    with st.echo(code_location="below"):
        survey = ss.StreamlitSurvey("Survey 2")

        # Define questions:
        Q1 = ss.Radio(survey, "Thumbs up/down:", options=["NA", "👍", "👎"], horizontal=True)
        Q1_1 = ss.TextInput(survey, "Why did you select '👍'?")

        # Display logic:
        q1_value = Q1.display()
        if q1_value == "👍":
            Q1_1.display()

"""
## Survey State Restoration

In Streamlit, widgets are restored to their default values after they are no longer displayed (even if you specify a `key` to store their state in `st.session_state`). Instead, our survey components remember their state and are automatically restored to their previous value or default value when displayed.

This way, you can associate questions to user inputs, using the `id` parameter to distinguish between answers corresponding to different inputs. For example, you may want to ask a user feedback on each prediction made by a ML model. You can let the user choose the prediction and give feedback. Using survey state restoration, users can easily go back to see and edit previous answers. 

Here's an example below. As long as you press "enter" to save your changes, you can go back and forth to edit your answers regarding different test case IDs.
"""

with st.echo(code_location="below"):
    user_input = st.number_input("Select a test case ID:", value=0, min_value=0, max_value=50)
    survey = ss.StreamlitSurvey("Survey 3")
    survey.text_input("What do you think about this test case?", id=f"Q1_{user_input}")

"""
## Paged Surveys

Survey components can be grouped into pages using the `Pages` class. The `Pages` class also supports survey state restoration, so that users can go back and forth between pages without losing their answers:
"""

with st.expander("Code Example:", expanded=True):
    with st.echo(code_location="below"):
        survey = ss.StreamlitSurvey("Survey Example - Advanced Usage")
        pages = survey.pages(2, on_submit=lambda: st.success("Your responses have been recorded. Thank you!"))
        with pages:
            if pages.current == 0:
                st.write("Have you used Streamlit before?")
                used_before = survey.radio(
                    "used_st_before",
                    options=["NA", "Yes", "No"],
                    index=0,
                    label_visibility="collapsed",
                    horizontal=True,
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
                        "used_other",
                        options=["NA", "Yes", "No"],
                        index=0,
                        label_visibility="collapsed",
                        horizontal=True,
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
