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

import streamlit as st
from abc import ABC, abstractmethod


class SurveyComponent(ABC):

    COMPONENT_KEY_PREFIX = "__streamlit-survey-component"

    def __init__(self, survey, label="", id=None, **kwargs):
        if id is None:
            id = survey.create_id(label)

        self.label = label
        self.id = id
        self.survey = survey
        self.kwargs = kwargs

        self.log_label(self.label)
        survey.add_component(self)

    def log_value(self, value):
        self.survey.log(self.id, "value", value)

    def get_value(self):
        return self.survey.get(self.id, "value")

    def log_label(self, label):
        self.survey.log(self.id, "label", label)

    @abstractmethod
    def register(self):
        pass

    def display(self):
        self.register()
        return self.get_value()

    @classmethod
    def from_st_input(cls, Class, serializer=lambda x: x):
        class StreamlitInput(SurveyComponent):
            def register(self):                
                if "key" not in self.kwargs:
                    self.kwargs["key"] = f"{self.COMPONENT_KEY_PREFIX}_{self.survey.label}_{self.id}"
                if self.kwargs["key"] not in st.session_state and self.get_value() is not None: 
                    # Note: Streamlit widget keys get automatically deleted from st.session_state, restoring widgets to their default value when they are no longer displayed. To get around this issue, we automatically restore widget values from the survey data when it is available.
                    st.session_state[self.kwargs["key"]] = self.get_value()
                
                value = Class(label=self.label, **self.kwargs)
                self.log_value(serializer(value))

        return StreamlitInput

TextInput = SurveyComponent.from_st_input(st.text_input)
TextArea = SurveyComponent.from_st_input(st.text_area)
NumberInput = SurveyComponent.from_st_input(st.number_input)
MultiSelect = SurveyComponent.from_st_input(st.multiselect)
SelectBox = SurveyComponent.from_st_input(st.selectbox)
Radio = SurveyComponent.from_st_input(st.radio)
Slider = SurveyComponent.from_st_input(st.slider)
CheckBox = SurveyComponent.from_st_input(st.checkbox)
DateInput = SurveyComponent.from_st_input(st.date_input, serializer=str)
TimeInput = SurveyComponent.from_st_input(st.time_input, serializer=str)
