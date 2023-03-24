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

from collections import defaultdict
import streamlit as st
import json
from streamlit_survey.survey_component import (
    TextInput,
    TextArea,
    MultiSelect,
    SelectBox,
    Radio,
    Slider,
    CheckBox,
    DateInput,
    TimeInput,
    NumberInput,
)


class StreamlitSurvey:
    DEFAULT_DATA_NAME = "__streamlit-survey-data"

    def __init__(self, label="", data=None, auto_id=True):
        if data is None:
            self.data_name = self.DEFAULT_DATA_NAME + "_" + label
            if self.data_name not in st.session_state:
                st.session_state[self.data_name] = {}
            data = st.session_state[self.data_name]

        self.label = label
        self.auto_id = auto_id
        self.data = data

        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def log(self, id, key, value):
        if id not in self.data:
            self.data[id] = defaultdict(lambda: None)

        self.data[id][key] = value

    def get(self, id, key):
        if id not in self.data:
            self.data[id] = defaultdict(lambda: None)

        return self.data[id][key]

    def create_id(self, label):
        if self.auto_id:
            return f"Q{len(self.components)+1}"
        else:
            return label

    def to_json(self):
        return json.dumps(self.data, default=str)

    def from_json(self, path):
        with open(path, "r") as f:
            self.data.clear()
            self.data.update(json.load(f))

    def text_input(self, label="", id=None, **kwargs):
        return TextInput(self, label, id, **kwargs).display()

    def text_area(self, label="", id=None, **kwargs):
        return TextArea(self, label, id, **kwargs).display()

    def number_input(self, label="", id=None, **kwargs):
        return NumberInput(self, label, id, **kwargs).display()

    def multiselect(self, label="", id=None, **kwargs):
        return MultiSelect(self, label, id, **kwargs).display()

    def selectbox(self, label="", id=None, **kwargs):
        return SelectBox(self, label, id, **kwargs).display()

    def radio(self, label="", id=None, **kwargs):
        return Radio(self, label, id, **kwargs).display()

    def slider(self, label="", id=None, **kwargs):
        return Slider(self, label, id, **kwargs).display()

    def checkbox(self, label="", id=None, **kwargs):
        return CheckBox(self, label, id, **kwargs).display()

    def dateinput(self, label="", id=None, **kwargs):
        return DateInput(self, label, id, **kwargs).display()

    def timeinput(self, label="", id=None, **kwargs):
        return TimeInput(self, label, id, **kwargs).display()
