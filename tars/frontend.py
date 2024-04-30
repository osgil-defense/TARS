import streamlit as st
from openai import OpenAI
import subprocess
import time
import json
import uuid
import shlex
import sys
import os
import re


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
            "json": os.path.join(events_dir, f"{cli_id}.json"),
        },
    }


def agent_running(id):
    command = f"ps aux | grep {id} | grep 'python' | grep -v 'grep'"

    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    output = result.stdout

    pid = None
    try:
        pid = int([item for item in output.split(" ") if item][1])
    except:
        pass

    running = True
    if len(output) == 0:
        running = False

    return {"pid": pid, "status": running}


def load_agent_content(text_path=None, json_path=None):
    output = {"text": None, "json": None}

    if text_path != None and os.path.exists(text_path):
        with open(text_path, "r") as file:
            output["text"] = file.read()

    if json_path != None and os.path.exists(json_path):
        with open(json_path, "r") as f:
            output["json"] = json.load(f)

    return output


def clean_text(text):
    cleaned_text = re.sub(r"^(```markdown|```md|```)\s*", "", text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r"```$", "", cleaned_text)
    return cleaned_text.strip()


# source: https://stackoverflow.com/a/14693789
def remove_color_codes(text):
    ansi_escape = re.compile(
        r"""
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    """,
        re.VERBOSE,
    )
    return ansi_escape.sub("", text)


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
    st.session_state["stream_max_i"] = -1


# TODO: this needs refinement!
def stream_data():
    aid = st.session_state.get("init_agent_output", {}).get("id", None)
    text_file_path = (
        st.session_state.get("init_agent_output", {}).get("paths", {}).get("text", None)
    )

    if text_file_path and os.path.exists(text_file_path):
        with open(text_file_path, "r") as file:
            text_content = file.read().split()

        max_i = st.session_state.get("stream_max_i", 0)
        if agent_running(aid)["status"]:
            for i in range(max_i, len(text_content) - 1):
                yield remove_color_codes(text_content[i] + " ")
                time.sleep(0.02)

                # update max_i safely within the bounds of text_content
                st.session_state["stream_max_i"] = min(i + 1, len(text_content) - 1)

            # reset the stream_max_i to allow repeating or restarting the stream if needed
            st.session_state["stream_max_i"] = 0
    else:
        # log or handle the case where the file path does not exist
        yield "Waiting for text data..."


# Page configuration and layout
st.set_page_config(page_title="Medusa - Beta")
st.markdown("<h1 style='text-align: center;'>Medusa</h1>", unsafe_allow_html=True)
st.image(image="logo.jpg")

# User input form
if not st.session_state["submitted"] and not st.session_state["run_agent"]:
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

        # TODO: this needs refinement!
        col1, col2, col3 = st.columns([1, 1, 12])
        with col3:
            with st.status("Processing..."):
                # st.write("Crew(s) can take anywhere from 30 seconds to 10 minutes to run")
                st.write_stream(stream_data)
                # time.sleep(10)

        st.rerun()
    else:
        print(f"Agent id {aid} is DONE!")
        st.session_state["agent_running"] = False
        docs = load_agent_content(
            st.session_state["init_agent_output"]["paths"]["text"],
            st.session_state["init_agent_output"]["paths"]["json"],
        )

        # print final result
        final_report = docs["json"]["output"]["result"]["final_output"]
        final_report = clean_text(final_report)
        st.session_state.messages.append({"role": "system", "content": final_report})

        st.session_state["agent_done"] = True
        st.rerun()

if st.session_state["submitted"] and st.session_state["agent_done"]:
    # Chat input for interaction
    prompt = st.chat_input("Ask about the commands executed")
    if prompt:
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
