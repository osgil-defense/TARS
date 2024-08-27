"""
Dear Programmer:

When I wrote this code, only God and I knew how it worked.
Now, only God knows!

Streamlit is a bad product, don't use it. But we are too,
deep into this now to switch. Maybe in another life.

So if you are trying to optimize this routine and fail,
(very likely) please increase the following counter
as a warning to the next developer:

total_hours_lost_here = 22
"""

from openai import OpenAI
import streamlit as st
import subprocess
import random
import shlex
import time
import json
import uuid
import sys
import os
import re

config_file_path = os.path.join(str("/".join(__file__.split("/")[:-2])), "tars")
sys.path.append(config_file_path)
import config


def replace_local_urls(text):
    # regex to match the URLs with localhost, 127.0.0.1, with optional http(s) and www
    pattern = re.compile(
        r"(https?:\/\/)?(www\.)?(localhost|127\.0\.0\.1)(:[0-9]+)?", re.IGNORECASE
    )

    # replace all matching patterns
    return pattern.sub(r"\1\2host.docker.internal\4", text)


def run_agents(user_question):
    user_question = replace_local_urls(user_question)
    events_dir = config.events_dir
    cli_filepath = config.cli_filepath

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


def generate_loading_screen(total_boxes=100):
    assets = "⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿"
    assets = list(assets)
    return "".join(random.sample(assets, total_boxes))


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
    st.session_state["agent_words_gened"] = 0
    st.session_state["job_failed"] = False
    st.session_state["start_time"] = 0


st.markdown("<h1 style='text-align: center;'>TARS</h1>", unsafe_allow_html=True)

st.write("\n")
st.image(
    image=os.path.join("/".join(os.path.abspath(__file__).split("/")[:-1]), "logo.png")
)
st.write("\n")

if st.session_state["agent_running"]:
    aid = st.session_state["init_agent_output"]["id"]
    astatus = agent_running(aid)
    print("===> astatus: ", astatus)
    if astatus["status"] == True:
        print(f"Agent id {aid} is still running...")
        text_file_path = st.session_state["init_agent_output"]["paths"]["text"]
        if os.path.exists(text_file_path):
            with open(text_file_path, "r") as file:
                text_content = file.read()
            ascii_loading_text = generate_loading_screen()
            text_content = (
                ascii_loading_text + "\n\n" + text_content + "\n\n" + ascii_loading_text
            )
            st.code(remove_color_codes(text_content))
        time.sleep(1)

        st.rerun()
    else:
        print(f"Agent id {aid} is DONE!")
        st.session_state["agent_running"] = False
        docs = load_agent_content(
            st.session_state["init_agent_output"]["paths"]["text"],
            st.session_state["init_agent_output"]["paths"]["json"],
        )

        # print final result
        try:
            runtime = time.time() - st.session_state["start_time"]

            # add raw output from agents running (saved stdout outputs)
            reformated_docs_text = (
                f"```\n" + str(docs["text"]).replace("```", '"""') + f"\n```"
            )
            reformated_docs_text = f"""
## Job's ID
                 
{aid}

## Runtime

{runtime} seconds

## Raw Agent(s) Output

{reformated_docs_text}
"""
            st.session_state.messages.append(
                {"role": "system", "content": reformated_docs_text}
            )

            final_report = clean_text(docs["json"]["output"]["result"]["final_output"])
            st.session_state.messages.append(
                {"role": "system", "content": final_report}
            )
        except Exception as err:
            print("---> ERROR LOADING FINAL REPORT:", err)
            text_file_path = st.session_state["init_agent_output"]["paths"]["text"]
            if os.path.exists(text_file_path):
                with open(text_file_path, "r") as file:
                    text_content = file.read()
                if len(text_content) > 0:
                    st.session_state.messages.append(
                        {"role": "system", "content": text_content}
                    )
            try:
                error_msg = docs["json"]["error"]
            except:
                error_msg = str(err)

            st.session_state.messages.append(
                {
                    "role": "system",
                    "content": f"Job Completely Failed Due To: {error_msg}",
                }
            )

            st.session_state.messages.append(
                {"role": "system", "content": f"🚨 Try Again By Refreshing The Page 🚨"}
            )

            st.session_state["job_failed"] = True

        st.session_state["agent_done"] = True
        st.rerun()

# User input form
if not st.session_state["submitted"] and not st.session_state["run_agent"]:
    with st.form("my_form"):
        st.session_state["website"] = st.text_input(
            "What's Your Target Website/Network Address?", st.session_state["website"]
        )
        text = st.text_area("What Cybersecurity-Related Task Do You Want To Do?", "")
        submitted = st.form_submit_button("Submit")

    # Handle form submission
    if (
        submitted
        and not st.session_state["submitted"]
        and not st.session_state["run_agent"]
    ):
        if not st.session_state["website"]:
            st.warning("Please Enter A Valid Website (URL)", icon="⚠️")
        else:
            first_prompt = f"""
### Website to Analyze:

{st.session_state["website"]}

### Task Description:

{text}
"""
            st.session_state["sys_prompt"] = first_prompt
            st.session_state.messages.append(
                {"role": "system", "content": st.session_state["sys_prompt"]}
            )
            st.session_state["submitted"] = True
            st.session_state["run_agent"] = True
            st.rerun()

if st.session_state["run_agent"] == True:
    st.session_state["start_time"] = time.time()
    init_agent_output = run_agents(st.session_state["sys_prompt"])
    print(f"Started new agent session: {init_agent_output['id']}")
    st.session_state["init_agent_output"] = init_agent_output
    st.session_state["run_agent"] = False
    print(st.session_state["agent_running"])
    st.session_state["agent_running"] = True
    print(st.session_state["agent_running"])
    print()
    st.rerun()

# Display messages from session state
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if (
    st.session_state["submitted"]
    and st.session_state["agent_done"]
    and not st.session_state["job_failed"]
):
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
