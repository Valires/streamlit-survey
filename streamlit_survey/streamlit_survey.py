from collections import defaultdict
import streamlit as st
import json
from streamlit_survey.survey_component import (
    Thumbs,
    Faces,
    TextInput,
    TextArea,
    MultiChoice,
    SelectBox,
    Radio,
    Slider,
    CheckBox,
    DateInput,
    TimeInput,
)


class StreamlitSurvey:
    DEFAULT_DATA_NAME = "__streamlit-survey-data"

    def __init__(self, data=None, auto_id=True):
        if data is None:
            if self.DEFAULT_DATA_NAME not in st.session_state:
                st.session_state[self.DEFAULT_DATA_NAME] = {}
            data = st.session_state[self.DEFAULT_DATA_NAME]

        self.auto_id = auto_id
        self.id_counter = 0
        self.data = data

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
            self.id_counter += 1
            return f"Q{self.id_counter}"
        else:
            return label

    def to_json(self):
        return json.dumps(self.data)

    def from_json(self, path):
        with open(path, "r") as f:
            self.data = json.load(f)

    def thumbs(self, label="", id=None, **kwargs):
        return Thumbs(self, label, id, **kwargs).display()

    def faces(self, label="", id=None, **kwargs):
        return Faces(self, label, id, **kwargs).display()

    def text_input(self, label="", id=None, **kwargs):
        return TextInput(self, label, id, **kwargs).display()

    def text_area(self, label="", id=None, **kwargs):
        return TextArea(self, label, id, **kwargs).display()

    def multichoice(self, label="", id=None, **kwargs):
        return MultiChoice(self, label, id, **kwargs).display()

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
