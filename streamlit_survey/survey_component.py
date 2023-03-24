import streamlit as st
from abc import ABC, abstractmethod


class SurveyComponent(ABC):
    def __init__(self, survey, label="", id=None, **kwargs):
        if id is None:
            id = survey.create_id(label)

        self.label = label
        self.id = id
        self.survey = survey
        self.kwargs = kwargs

        self.log_label(self.label)

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
                value = Class(label=self.label, key=f"{self.id}", **self.kwargs)

                if value is not None:
                    self.log_value(serializer(value))

        return StreamlitInput


class Thumbs(SurveyComponent):
    def register(self):
        st.write(self.label)

        col1, col2 = st.columns([1, 15])
        with col1:
            up = st.button("👍", key=f"{self.id}_up", **self.kwargs)
        with col2:
            down = st.button("👎", key=f"{self.id}_down")

        if up:
            self.log_value(True)
        elif down:
            self.log_value(False)


class Faces(SurveyComponent):
    def register(self):
        st.write(self.label)

        columns = st.columns([1, 1, 1, 1, 10])
        emojis = ["😞", "🙁", "😐", "🙂", "😀"]
        emoji_values = [1, 2, 3, 4, 5]
        buttons = [False] * 5

        for i, col in enumerate(columns):
            with col:
                buttons[i] = st.button(
                    emojis[i], key=f"{self.id}_{emoji_values[i]}", **self.kwargs
                )

        if any(buttons):
            self.log_value(buttons.index(True) + 1)


TextInput = SurveyComponent.from_st_input(st.text_input)
TextArea = SurveyComponent.from_st_input(st.text_area)
MultiChoice = SurveyComponent.from_st_input(st.multiselect)
SelectBox = SurveyComponent.from_st_input(st.selectbox)
Radio = SurveyComponent.from_st_input(st.radio)
Slider = SurveyComponent.from_st_input(st.slider)
CheckBox = SurveyComponent.from_st_input(st.checkbox)
DateInput = SurveyComponent.from_st_input(st.date_input, serializer=str)
TimeInput = SurveyComponent.from_st_input(st.time_input, serializer=str)
