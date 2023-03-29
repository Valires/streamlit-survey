import streamlit as st
import streamlit_survey as ss
import ml_project as mp

"""
# Error Auditing in Machine Learning

This app is a simple demo of Streamlit-Survey to carry out error analysis of a toy digit recognition model.
"""

st.info("Error editing (qualitative error analysis) in machine learning involves manually reviewing a sample of a model's predictions or known errors. Then, errors are categorized based on their type, potential cause, and severity. The goal is to identify and analyze errors, assess their impact on the model's performance, and provide recommendations for improvement.", icon="ℹ️")

with st.echo(code_location="below"):
    import streamlit_survey as ss
    import ml_project as mp
    survey = ss.StreamlitSurvey()

    with st.sidebar:
        file = survey.importer("Import Survey Data:")
        survey.download_button("Export Survey Data")

    with survey.pages(len(mp.X_test)) as page:
        """#### 1. Select test case ID:"""
        st.number_input("test-case", value=page.current, min_value=0, max_value=len(mp.X_test) - 1, label_visibility="collapsed", key="page", on_change=lambda: page.update(st.session_state["page"]))

        """#### 2. Review the test case:"""
        _, center, _ = st.columns(3)
        with center:
            st.pyplot(mp.make_plot(page.current))

        """#### 3. Log your observations:"""
        st.info("Use newline-separated keywords to record your observations. Press ctrl+enter to save.", icon="ℹ️")
        survey.text_area("Tags", id=f"tags_{page.current}", label_visibility="collapsed")

    """#### 4. Analyze"""
    st.plotly_chart(mp.analysis_plot(survey.data))
