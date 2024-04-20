import streamlit as st

st.set_page_config(page_title="Bingus Bingus Bingus")
st.title('Bingus Bingus Bingus')

openai_api_key = st.sidebar.text_input('Give Bingus a Key')

st.image(image="bingus.webp")
with st.form('my_form'):
  text = st.text_area('Enter text:', 'bingussy bingussy bingussy')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('REMEMBER TO FEED BINGUS BEFORE SPEAKING WITH HIM!', icon='⚠')
 