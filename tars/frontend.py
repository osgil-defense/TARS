import streamlit as st
from openai import OpenAI
import time
import json
import sys
import os

from tars import Job

# Initialize the OpenAI client with an API key
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Session state initialization
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False
    st.session_state["messages"] = []
    st.session_state["website"] = ""
    st.session_state["sys_prompt"] = ""
    st.session_state["openai_model"] = "gpt-4-turbo"
    st.session_state["run_agents"] = False

# Page configuration and layout
st.set_page_config(page_title="Medusa - Beta")
st.markdown("<h1 style='text-align: center;'>Medusa</h1>", unsafe_allow_html=True)
# st.image(image="logo.jpg")

# User input form
if not st.session_state["submitted"]:
    with st.form("my_form"):
        st.session_state["website"] = st.text_input(
            "Website To Test", st.session_state["website"]
        )
        text = st.text_area("What Cybersecurity-Related Task Do You Want To Do?", "")
        submitted = st.form_submit_button("Submit")

    # Handle form submission
    if submitted and not st.session_state["submitted"]:
        st.session_state["submitted"] = True
        if not st.session_state["website"]:
            st.warning("ENTER A WEBSITE BEFORE ATTEMPTING!", icon="⚠️")
        else:
            first_prompt = f"""
Website to Analyze: {st.session_state["website"]}

Task Description:
{text}
"""
            st.session_state["sys_prompt"] = first_prompt
            st.session_state.messages.append(
                {"role": "system", "content": st.session_state["sys_prompt"]}
            )

    if st.session_state["submitted"]:
        st.session_state["run_agents"] = True
        st.rerun()


if st.session_state["run_agents"]:
    st.session_state["run_agents"] = False

    job_manager = Job()
    job_id = job_manager.start(st.session_state["sys_prompt"])
    # if job_id is not None:
    #     print(f"Job started with ID: {job_id}")
    # else:
    #     print("Failed to start job or job is already running.")

    st.session_state.messages.append(
        {"role": "system", "content": f"Started job {job_id}"}
    )

    while True:
        status = job_manager.status()
        st.session_state.messages.append(
            {"role": "system", "content": f"Current Job Status: {status['status']}"}
        )
        if status["status"] != "running":
            break
        time.sleep(10)

    if status["status"] == "not running":
        job_details = job_manager.get_history(job_id)
        if job_details:
            if "error" in job_details:
                st.session_state.messages.append(
                    {
                        "role": "system",
                        "content": f"Job Failed With Error: {job_details['error']}",
                    }
                )
            else:
                st.session_state.messages.append(
                    {
                        "role": "system",
                        "content": f"Job Failed With Error: {job_details['error']}",
                    }
                )

                # TODO: "print" final result(s)
                st.session_state.messages.append(
                    {
                        "role": "system",
                        "content": job_details["output"]["result"]["final_output"],
                    }
                )
        else:
            st.session_state.messages.append(
                {"role": "system", "content": "No details found for the completed job"}
            )


# Display messages from session state
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state["submitted"]:
    # Chat input for interaction
    prompt = st.chat_input("Ask about the commands executed")
    if prompt:
        # # TODO: remove after testing
        # print(st.session_state.messages)
        # print()

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call OpenAI's API to generate a response
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
