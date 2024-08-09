"""
Copyright 2023 Olivier Binette

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import datetime
import json
import os
from collections import defaultdict
from typing import Any, Hashable, List, Optional, Union

import streamlit as st

from streamlit_survey.pages import Pages
from streamlit_survey.survey_component import (
    CheckBox,
    DateInput,
    MultiSelect,
    NumberInput,
    Radio,
    SelectBox,
    SelectSlider,
    Slider,
    SurveyComponent,
    TextArea,
    TextInput,
    TimeInput,
)

PathLike = Union[str, bytes, os.PathLike]


class StreamlitSurvey:
    """
    StreamlitSurvey is a Streamlit component that allows you to create surveys. It is built on top of the Streamlit API and allows you to create surveys with a few lines of code.

    Survey questions and answers are stored in a JSON file that is automatically saved in the Streamlit session state. This means that you can save the survey data and reload it later. You can create conditional surveys to ask different questions based on the answers to previous questions. Answers to previous questions are always preserved, even if the user goes back to a previous question or if Streamlit input widgets are no longer displayed.

    Examples
    --------

    Basic functionality is similar to Streamlit's own input widgets:


    >>> import streamlit as st
    >>> from streamlit_survey import StreamlitSurvey
    >>>
    >>> survey = StreamlitSurvey("My Survey")
    >>>
    >>> name = survey.text_input("What is your name?")
    >>> age = survey.number_input("What is your age?", min_value=0, max_value=100)
    >>>
    >>> if st.button("Submit"):
    >>>     st.write(f"Hello {name}, you are {age} years old!")

    However, the `survey` object keeps track of survey questions and answers for easy access and analysis. You can save and load responses to a JSON file:

    >>> survey.to_json("data.json)
    >>> survey.from_json("data.json")
    >>>
    >>> # Or, if you want to load the data from a URL:
    >>> survey.from_json("https://example.com/data.json")

    You can also use the `auto_id` parameter to disable automatic numbering of questions:

    >>> survey = StreamlitSurvey("My Survey", auto_id=False)

    This will allow you to use custom IDs for each question:

    >>> name = survey.text_input("What is your name?", id="name")
    >>> age = survey.number_input("What is your age?", id="age", min_value=0, max_value=100)

    These IDs are particularly useful if you want to create conditional surveys. For example, you can ask a different question based on the answer to a previous question:

    >>> import streamlit as st
    >>> from streamlit_survey import StreamlitSurvey
    >>>
    >>> survey = StreamlitSurvey("My Survey")
    >>>
    >>> name = survey.text_input("What is your name?")
    >>> age = survey.number_input("What is your age?", min_value=0, max_value=100)
    >>>
    >>> if age < 18:
    >>>     survey.multiselect("What is your favorite color?", options=["Red", "Green", "Blue"], id="Q_color")
    >>> else:
    >>>     survey.text_input("What is your job?", id="Q_job")

    In contrast to Streamlit's own input widgets, StreamlitSurvey will always preserve the answers to previous questions, even when widgets are no longer displayed. This way, user can go back to previous questions, change their path in the survey, or even close and reopen the survey without losing their answers.
    """

    BASE_NAME = "__streamlit-survey-data"

    def __init__(self, label: str = "", data: dict = None, auto_id: bool = True):
        """
        Parameters
        ----------
        label: str
            Label of the survey
        data: dict
            Dictionary containing survey questions and answers
        auto_id: bool
            Whether to automatically number survey questions
        """
        self.data_name = self.BASE_NAME + "_" + label
        if data is None:
            if self.data_name not in st.session_state:
                st.session_state[self.data_name] = {}
            data = st.session_state[self.data_name]

        self.label = label
        self.auto_id = auto_id
        self.data = data

        self._components = []  # Active (currently displayed) survey components

    def _add_component(self, component: SurveyComponent):
        self._components.append(component)

    def _log(self, id: str, key: Hashable, value: Any):
        if id not in self.data:
            self.data[id] = defaultdict(lambda: None)

        self.data[id][key] = value

    def _get(self, id: str, key: Hashable):
        if id not in self.data:
            self.data[id] = defaultdict(lambda: None)

        return self.data[id][key]

    def _create_id(self, label: str):
        if self.auto_id:
            return label
        else:
            raise RuntimeError("An ID should be explicitely provided if `auto_id` is set to False.")

    def pages(self, index: Union[int, list], on_submit=None, progress_bar=False, label: str = ""):
        """
        Create a pages group

        Examples
        --------
        >>> import streamlit_survey as ss
        >>> survey = ss.StreamlitSurvey("My Survey")
        >>> with survey.pages(3) as pages:
        >>>     if pages.current == 0:
        >>>         name = survey.text_input("What is your name?")
        >>>     elif pages.current == 1:
        >>>         age = survey.number_input("What is your age?")
        >>>     elif pages.current == 2:
        >>>         st.write("Thank you!")

        Parameters
        ----------
        index: Union[int, list]
            Number of pages or list of page names
        on_submit: function
            Function to call when the user submits the survey.
        progress_bar: bool
            Whether to show a progress bar under the pages group. Default to False.
        label: str
            Label for the page group.

        Returns
        -------
        Pages
            Pages object
        """
        return Pages(index, key=self.data_name + "_Pages_" + label, on_submit=on_submit, progress_bar=progress_bar)

    def to_json(self, path: Optional[PathLike] = None) -> Optional[str]:
        """
        Save survey data to a JSON file

        Parameters
        ----------
        path: str
            Path to the JSON file. If None, the data will be returned as a string.

        Returns
        -------
        str
            JSON string containing survey data. Only returned if `path` is None.
        """
        if path is None:
            return json.dumps(self.data)
        else:
            with open(path, "w") as f:
                json.dump(self.data, f)

    def importer(self, label: str = "", **kwargs):
        """
        Import survey data from a JSON file using a widget

        Parameters
        ----------
        label: str
            Label of the widget
        """
        if "key" in kwargs:
            file_key = kwargs["key"]
        else:
            file_key = self.BASE_NAME + "_file_" + label

        def load_json():
            file = st.session_state[file_key]
            if file is None:
                return
            self.from_file(file)

        file = st.file_uploader(label, type="json", key=file_key, on_change=load_json, **kwargs)
        return file

    def download_button(self, label: str = "", file_name="survey.json", **kwargs):
        """
        Download survey data as a JSON file using a widget

        Parameters
        ----------
        label: str
            Label of the widget
        file_name: str
            Name of the downloaded file
        """
        download = st.download_button(label, data=self.to_json(), file_name=file_name, **kwargs)
        return download

    def from_json(self, path: PathLike):
        """
        Load survey data from a JSON file

        Parameters
        ----------
        path: str
            Path to the JSON file. Can also be a URL.
        """
        with open(path, "r") as f:
            self.from_file(f)

    def from_file(self, file):
        """
        Load survey data from a JSON file

        Parameters
        ----------
        file: file
            File object containing the JSON data
        """
        # Update survey data
        self.data.clear()
        self.data.update(json.load(file))

        # Update displayed Streamlit widgets values
        for _, data in self.data.items():
            if "widget_key" in data and data["widget_key"] in st.session_state:
                st.session_state[data["widget_key"]] = data["value"]

    def text_input(self, label: str = "", id: str = None, **kwargs) -> str:
        """
        Create a text input widget

        Parameters
        ----------
        label: str
            Label of the widget
        id: str
            ID of the widget. If None, the ID will be automatically generated.
        **kwargs
            Additional keyword arguments passed to `st.text_input`

        Returns
        -------
        str
            Value of the text input
        """
        return TextInput(self, label, id, **kwargs).display()

    def text_area(self, label: str = "", id: str = None, **kwargs) -> str:
        """
        Create a text area widget

        Parameters
        ----------
        label: str
            Label of the widget
        id: str
            ID of the widget. If None, the ID will be automatically generated.
        **kwargs
            Additional keyword arguments passed to `st.text_area`

        Returns
        -------
        str
            Value of the text area
        """
        return TextArea(self, label, id, **kwargs).display()

    def number_input(self, label: str = "", id: str = None, **kwargs) -> float:
        """
        Create a number input widget

        Parameters
        ----------
        label: str
            Label of the widget
        id: str
            ID of the widget. If None, the ID will be automatically generated.
        **kwargs
            Additional keyword arguments passed to `st.number_input`

        Returns
        -------
        float
            Value of the number input
        """
        return NumberInput(self, label, id, **kwargs).display()

    def multiselect(self, label: str = "", id: str = None, **kwargs) -> List[Any]:
        """
        Create a multi-select widget

        Parameters
        ----------
        label: str
            Label of the widget
        id: str
            ID of the widget. If None, the ID will be automatically generated.
        **kwargs
            Additional keyword arguments passed to `st.multiselect`

        Returns
        -------
        list
            List of selected options
        """
        return MultiSelect(self, label, id, **kwargs).display()

    def selectbox(self, label: str = "", id: str = None, **kwargs) -> str:
        """
        Create a select box widget

        Parameters
        ----------
        label: str
            Label of the widget
        id: str
            ID of the widget. If None, the ID will be automatically generated.
        **kwargs
            Additional keyword arguments passed to `st.selectbox`

        Returns
        -------
        str
            Selected option
        """
        return SelectBox(self, label, id, **kwargs).display()

    def radio(self, label: str = "", id: str = None, **kwargs) -> str:
        """
        Create a radio button widget

        Parameters
        ----------
        label: str
            Label of the widget
        id: str
            ID of the widget. If None, the ID will be automatically generated.
        **kwargs
            Additional keyword arguments passed to `st.radio`

        Returns
        -------
        str
            Selected option
        """
        return Radio(self, label, id, **kwargs).display()

    def slider(self, label: str = "", id: str = None, **kwargs) -> float:
        """
        Create a slider widget

        Parameters
        ----------
        label: str
            Label of the widget
        id: str
            ID of the widget. If None, the ID will be automatically generated.
        **kwargs
            Additional keyword arguments passed to `st.slider`

        Returns
        -------
        float
            Value of the slider
        """
        return Slider(self, label, id, **kwargs).display()

    def select_slider(self, label: str = "", id: str = None, **kwargs) -> str:
        """
        Create a select slider widget

        Parameters
        ----------
        label: str
            Label of the widget
        id: str
            ID of the widget. If None, the ID will be automatically generated.
        **kwargs
            Additional keyword arguments passed to `st.select_slider`

        Returns
        -------
        str
            Selected option
        """
        return SelectSlider(self, label, id, **kwargs).display()

    def checkbox(self, label: str = "", id: str = None, **kwargs) -> bool:
        """
        Create a checkbox widget

        Parameters
        ----------
        label: str
            Label of the widget
        id: str
            ID of the widget. If None, the ID will be automatically generated.
        **kwargs
            Additional keyword arguments passed to `st.checkbox`

        Returns
        -------
        bool
            Value of the checkbox
        """
        return CheckBox(self, label, id, **kwargs).display()

    def dateinput(self, label: str = "", id: str = None, **kwargs) -> datetime.date:
        """
        Create a date input widget

        Parameters
        ----------
        label: str
            Label of the widget
        id: str
            ID of the widget. If None, the ID will be automatically generated.
        **kwargs
            Additional keyword arguments passed to `st.date_input`

        Returns
        -------
        datetime.date
            Value of the date input
        """
        return DateInput(self, label, id, **kwargs).display()

    def timeinput(self, label: str = "", id: str = None, **kwargs) -> datetime.time:
        """
        Create a time input widget

        Parameters
        ----------
        label: str
            Label of the widget
        id: str
            ID of the widget. If None, the ID will be automatically generated.
        **kwargs
            Additional keyword arguments passed to `st.time_input`

        Returns
        -------
        datetime.time
            Value of the time input
        """
        return TimeInput(self, label, id, **kwargs).display()
