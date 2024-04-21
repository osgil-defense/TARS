import streamlit as st
import os
import main

st.set_page_config(page_title="MEDUSA DEMO")
st.title('MEDUSA DEMO')

os.environ['WEBSITE'] = st.sidebar.text_input('Enter website to test here')

st.image(image="bingus.webp")
with st.form('my_form'):
    text = st.text_area('Enter commands:', 'Enter text here')
    submitted = st.form_submit_button('Submit')  # This will return True when the form is submitted
    if submitted:  # Only run the following code if the form is submitted
        if not os.environ['WEBSITE']:
            st.warning('ENTER A WEBSITE BEFORE ATTEMPTING!', icon='⚠')
        else:
            st.warning("PROCESS HAS FINISHED:" + main.npmgod.kickoff())  # Now this only runs when the form is submitted
            
            print(os.environ["WEBSITE"])
 