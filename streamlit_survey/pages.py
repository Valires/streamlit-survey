import streamlit as st

class Pages(object):
    def __init__(self, n_pages, key="current", on_submit=None):
        self.n_pages = n_pages
        self.current_page_key = key
        self.on_submit = on_submit

    @property
    def current(self):
        if self.current_page_key not in st.session_state:
            st.session_state[self.current_page_key] = 0
        return st.session_state[self.current_page_key]
    
    @current.setter
    def current(self, value):
        st.session_state[self.current_page_key] = value

    def previous(self):
        if self.current > 0:
            self.current -= 1

    def next(self):
        if self.current < self.n_pages - 1:
            self.current += 1

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        left, _, right = st.columns([2, 4, 2])
        with left:
            st.button("Previous", use_container_width=True, disabled=self.current == 0, on_click=self.previous)
        with right:
            if self.current == self.n_pages - 1 and self.on_submit is not None:
                st.button("Submit", type="primary", use_container_width=True, on_click=self.on_submit)
            else:
                st.button("Next", type="primary", use_container_width=True, on_click=self.next, disabled=self.current == self.n_pages - 1)
