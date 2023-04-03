import ml_project as mp
import streamlit as st
import streamlit_survey as ss

"""
# Error Auditing in Machine Learning

This app is a simple demo of [Streamlit-Survey](https://github.com/Valires/streamlit-survey) to carry out error auditing of a toy digit recognition model.
"""

st.info(
    "Error auditing (qualitative error analysis) in machine learning involves manually reviewing a sample of a model's predictions or known errors. Then, errors are categorized based on their type, potential cause, and severity. The goal is to identify and analyze errors, assess their impact on the model's performance, and provide recommendations for improvement.",
    icon="ℹ️",
)

with st.echo(code_location="below"):
    import ml_project as mp
    import streamlit_survey as ss

    survey = ss.StreamlitSurvey()

    with survey.pages(10) as page:
        """#### 1. Select test case ID:"""
        st.number_input(
            "test-case",
            value=page.current,
            min_value=0,
            max_value=9,
            label_visibility="collapsed",
            key="page",
            on_change=lambda: page.update(st.session_state["page"]),
        )

        """#### 2. Review the test case:"""
        _, center, _ = st.columns(3)
        with center:
            st.pyplot(mp.make_plot(page.current))

        """#### 3. Log your observations:"""
        error = survey.radio(
            "Is there an error?", options=["No", "Yes", "Unsure"], horizontal=True, id=f"error_{page.current}"
        )
        if error in ["Yes", "Unsure"]:
            col1, col2 = st.columns([2, 1])
            with col1:
                type = survey.selectbox("Error type", options=["Type 1", "Type 2", "Other"], id=f"type_{page.current}")
                if type == "Other":
                    survey.text_input("Error description:", id=f"other_type_{page.current}")
            with col2:
                survey.selectbox(
                    "Error severity", options=["Minor", "Moderate", "Severe"], id=f"severity_{page.current}"
                )
        survey.text_area("Notes", id=f"notes_{page.current}")


    """#### 4. Export or import survey data"""
    survey.download_button("Export Survey Data", use_container_width=True)
    survey.importer("Import Survey Data:")
