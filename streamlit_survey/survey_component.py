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
from abc import ABC, abstractmethod
from typing import Any, Optional, Callable

import streamlit as st

date_encoder = lambda obj: obj.isoformat()
date_decoder = lambda obj: datetime.datetime.fromisoformat(obj)
time_encoder = lambda obj: obj.strftime("%H:%M:%S")
time_decoder = lambda obj: datetime.datetime.strptime(obj, "%H:%M:%S").time()


class SurveyComponent(ABC):
    COMPONENT_KEY_PREFIX = "__streamlit-survey-component"

    def __init__(self, survey, label: str = "", id: Optional[str] = None, **kwargs):
        """
        Parameters
        ----------

        survey: StreamlitSurvey
            Survey object
        label: str
            Label of the component
        id: str
            ID of the component
        **kwargs: dict
            Keyword arguments to pass to the Streamlit input widget
        """
        if id is None:
            id = survey._create_id(label)

        self.label = label
        self.id = id
        self.survey = survey
        self.kwargs = kwargs

        self.log_label(self.label)
        survey._add_component(self)

    def log_value(self, value: Any):
        """
        Parameters
        ----------
        value: Any
            Value to log
        """
        self.survey._log(self.id, "value", value)

    def get_value(self) -> Any:
        """
        Returns
        -------
        Any:
            Value of the component
        """
        return self.survey._get(self.id, "value")

    def log_label(self, label):
        """
        Parameters
        ----------
        label: str
            Label to log
        """
        self.survey._log(self.id, "label", label)

    @abstractmethod
    def register(self):
        """
        Register the component with Streamlit.
        """
        pass

    def display(self) -> Any:
        """
        Display the component.

        Returns
        -------
        Any
            Value of the component
        """
        self.register()
        return self.get_value()

    @classmethod
    def from_st_input(cls, Class: type, encoder: Callable = lambda x: x, decoder: Callable = lambda x: x):
        """
        This function automatically creates SurveyComponent subclasses for Streamlit inputs, allowing users to easily add new Streamlit inputs to the library.

        Parameters
        ----------
        Class:
            Streamlit input class
        encoder:
            Function to encode the value before logging it
        decoder:
            Function to decode the value after retrieving it

        Returns
        -------
        StreamlitInput
            SurveyComponent subclass
        """

        class StreamlitInput(SurveyComponent):
            def register(self):
                if "key" not in self.kwargs:
                    self.kwargs["key"] = f"{self.COMPONENT_KEY_PREFIX}_{self.survey.label}_{self.id}"
                if self.kwargs["key"] not in st.session_state and self.get_value() is not None:
                    # Note: Streamlit widget keys get automatically deleted from st.session_state. This restores widgets to their default value when they are no longer displayed. To get around this issue, we automatically restore widget values from the survey data when it is available.
                    st.session_state[self.kwargs["key"]] = decoder(self.get_value())

                value = Class(label=self.label, **self.kwargs)
                self.log_value(encoder(value))

        return StreamlitInput


# Define SurveyComponent subclasses for Streamlit inputs:
TextInput = SurveyComponent.from_st_input(st.text_input)
TextArea = SurveyComponent.from_st_input(st.text_area)
NumberInput = SurveyComponent.from_st_input(st.number_input)
MultiSelect = SurveyComponent.from_st_input(st.multiselect)
SelectBox = SurveyComponent.from_st_input(st.selectbox)
Radio = SurveyComponent.from_st_input(st.radio)
Slider = SurveyComponent.from_st_input(st.slider)
CheckBox = SurveyComponent.from_st_input(st.checkbox)
DateInput = SurveyComponent.from_st_input(st.date_input, encoder=date_encoder, decoder=date_decoder)
TimeInput = SurveyComponent.from_st_input(st.time_input, encoder=time_encoder, decoder=time_decoder)
