import argparse
from crewai import Agent, Task, Crew, Process
import os
import json
import sys
import uuid
import time

import crews
import support


def write_json(path, data):
    with open(str(path), "w") as file:
        json.dump(data, file, indent=4)


def main(current_job_id, user_question, events_directory):
    if not os.path.exists(events_directory):
        os.makedirs(events_directory)

    raw_output_file_path = os.path.join(events_directory, f"{current_job_id}.txt")
    final_output_file_path = os.path.join(events_directory, f"{current_job_id}.json")

    if os.path.exists(raw_output_file_path):
        return
    if os.path.exists(final_output_file_path):
        return

    output = {}
    try:
        function_output, output_filename = support.execute_and_log(
            crews.call_crew,
            raw_output_file_path,
            user_question,
        )

        output = {
            "id": current_job_id,
            "output": function_output,
            "raw_output_file_path": raw_output_file_path,
            "completed": True,
            "error": None,
            "time": time.time(),
        }
    except Exception as e:
        output = {
            "id": current_job_id,
            "output": None,
            "raw_output_file_path": raw_output_file_path,
            "completed": False,
            "error": f"{e}",
            "time": time.time(),
        }

    write_json(final_output_file_path, output)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "--current_job_id",
        type=str,
        required=True,
        help="A unique identifier for the current job",
    )

    parser.add_argument(
        "--user_question", type=str, required=True, help="The user question to process"
    )

    parser.add_argument(
        "--events_directory",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "events"),
        help="Directory where event files will be stored",
    )

    args = parser.parse_args()

    main(args.current_job_id, args.user_question, args.events_directory)
