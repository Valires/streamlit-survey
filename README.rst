.. image:: https://img.shields.io/badge/Lifecycle-Experimental-339999
   :alt: Lifecycle: experimental
   :target: https://olivierbinette-streamlit-surv-docs-streamlit-survey-docs-hu1jf8.streamlit.app

**Streamlit-Survey**: Survey components for Streamlit apps
==========================================================

**Streamlit-Survey** is a Python package for incorporating surveys and structured feedback into `Streamlit <https://streamlit.io>`_ apps.

It can be used in combination to `Trubrics <https://github.com/trubrics/trubrics-sdk>`_ to collect feedback on datasets, models, and machine learning apps.

Installation
------------

Streamlit-Survey can be installed from Github::

        pip install git+https://github.com/OlivierBinette/streamlit-survey.git

Usage
-----

The `streamlit_survey` package contains a `StreamlitSurvey` class that can be used to create and manage survey components::

        import streamlit_survey as ss

        survey = ss.StreamlitSurvey("Example 1")

Components can be added to the survey using functions similar to Streamlit's input functions:

.. image:: streamlit-survey-screenshot.png
        :width: 500
        :align: center
        :target: https://olivierbinette-streamlit-surv-docs-streamlit-survey-docs-hu1jf8.streamlit.app


Read the docs:
--------------

`Streamlit-Survey Documentation <https://olivierbinette-streamlit-surv-docs-streamlit-survey-docs-hu1jf8.streamlit.app>`_

License
-------

* Apache 2.0