import streamlit as st
from openai import OpenAI
import subprocess
import time
import json
import uuid
import shlex
import sys
import os

def run_agents(user_question):
    # TODO: this might not be that good...
    events_dir = os.path.join(os.path.dirname(__file__), "events")

    cli_filepath = os.path.join(os.path.dirname(__file__), "cli.py")
    clid = f"{uuid.uuid4()}_{int(time.time())}"
    cli_id = shlex.quote(f"{clid}")
    user_question = shlex.quote(user_question)
    
    cmd = f"python3 {cli_filepath} --current_job_id {cli_id} --user_question {user_question} --events_directory {events_dir} &"

    os.system(cmd)

    return {
        "id": clid,
        "paths": {
            "text": os.path.join(events_dir, f"{cli_id}.txt"),
            "json": os.path.join(events_dir, f"{cli_id}.json")
        }
    }

def agent_running(id):
    command = f"ps aux | grep {id} | grep 'python' | grep -v 'grep'"

    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    output = result.stdout

    pid = None
    try:
        pid = int(
            [item for item in output.split(" ") if item][1]
        )
    except:
        pass

    running = True
    if len(output) == 0:
        running = False

    return {
        "pid": pid,
        "status": running
    }

def load_agent_content(text_path=None, json_path=None):
    output = {
        "text": None,
        "json": None
    }

    if text_path != None and os.path.exists(text_path):
        with open(text_path, "r") as file:
            output["text"] = file.read()
    
    if json_path != None and os.path.exists(json_path):
        with open(json_path, 'r') as f:
            output["json"] = json.load(f)
    
    return output


# Initialize the OpenAI client with an API key
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Session state initialization
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False
    st.session_state["messages"] = []
    st.session_state["website"] = ""
    st.session_state["sys_prompt"] = ""
    st.session_state["openai_model"] = "gpt-4-turbo"
    st.session_state["run_agent"] = False
    st.session_state["agent_running"] = False
    st.session_state["init_agent_output"] = {}
    st.session_state["agent_done"] = False

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
        st.session_state["run_agent"] = True
        st.rerun()


# Display messages from session state
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state["run_agent"] == True:
    init_agent_output = run_agents(st.session_state["sys_prompt"])
    print(f"Started new agent session: {init_agent_output['id']}")
    st.session_state["init_agent_output"] = init_agent_output
    st.session_state["run_agent"] = False
    print(st.session_state["agent_running"])
    st.session_state["agent_running"] = True
    print(st.session_state["agent_running"])
    print()
    st.rerun()

if st.session_state["agent_running"]:
    aid = st.session_state["init_agent_output"]["id"]
    astatus = agent_running(aid)
    print("===> astatus: ", astatus)
    if astatus["status"] == True:
        print(f"Agent id {aid} is still running...")
        st.session_state.messages.append(
            {"role": "system", "content": "Running..."}
        )
        time.sleep(2)
        st.rerun()
    else:
        print(f"Agent id {aid} is DONE!")
        st.session_state["agent_running"] = False
        docs = load_agent_content(
            st.session_state["init_agent_output"]["paths"]["text"],
            st.session_state["init_agent_output"]["paths"]["json"]
        )

        print("====FINAL_REPORT=====")
        print(docs["json"]["output"]["result"])
        print("====FINAL_REPORT=====")
        
        # print final result
        st.session_state.messages.append(
            {"role": "system", "content": docs["json"]["output"]["result"]["final_output"]}
        )

        st.session_state["agent_done"] = True
        st.rerun()

if st.session_state["submitted"] and st.session_state["agent_done"]:
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
