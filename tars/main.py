from crewai import Agent, Task, Crew, Process
import threading
import uuid
import time
import json
import sys
import os

import crews
import support


class Job:
    def __init__(self):
        events_directory = os.path.join(
            str("/".join(__file__.split("/")[:-1])), "events"
        )
        if not os.path.exists(events_directory):
            os.makedirs(events_directory)

        self.events_directory = events_directory
        self.thread = None
        self.is_running = False
        self.jobs_history = []
        self.current_job_id = None
        self.output_file_path = None
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.last_error = None  # track the last error message if any

    def start(self, user_question):
        with self.lock:
            if not self.is_running:
                self.current_job_id = f"{uuid.uuid4()}_{int(time.time())}"
                self.output_file_path = os.path.join(
                    self.events_directory, f"{self.current_job_id}.txt"
                )
                self.stop_event.clear()
                self.thread = threading.Thread(target=self.run, args=(user_question,))
                self.is_running = True
                self.thread.start()
                return self.current_job_id
            else:
                return None

    def run(self, user_question):
        try:
            function_output, output_filename = support.execute_and_log(
                crews.call_crew, self.output_file_path, user_question
            )
            with self.lock:
                self.jobs_history.append(
                    {
                        "id": self.current_job_id,
                        "output": function_output,
                        "output_file_path": self.output_file_path,
                        "status": "Completed",
                    }
                )
        except Exception as e:
            with self.lock:
                self.last_error = str(e)
                self.jobs_history.append(
                    {
                        "id": self.current_job_id,
                        "error": self.last_error,
                        "status": "Failed",
                    }
                )
        finally:
            with self.lock:
                self.is_running = False

    def status(self):
        with self.lock:
            status = "running" if self.is_running else "not running"
            return {"status": status, "last_error": self.last_error}

    def get_history(self, id=None):
        with self.lock:
            if id is not None:
                for entry in self.jobs_history:
                    if entry.get("id") == id:
                        return entry
            return self.jobs_history

    def get_file(self, id):
        filepath = None
        for entry in self.jobs_history:
            if entry.get("id") == id:
                filepath = entry.get("output_file_path")
                break

        if filepath == None:
            return filepath

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return file.read()
        except:
            return None

    def stop(self):
        with self.lock:
            if not self.is_running:
                return None
            try:
                self.stop_event.set()
                self.thread.join()
                self.is_running = False
                return True
            except:
                return False


# # TODO: remove after testing!!!
# job_manager = Job()
# job_id = job_manager.start("Is my network secure for: https://notifycyber.com/")
# if job_id is not None:
#     print(f"Job started with ID: {job_id}")
# else:
#     print("Failed to start job or job is already running.")
#     sys.exit(1)
# while True:
#     status = job_manager.status()
#     print(f"Current status: {status['status']}")
#     if status["status"] != "running":
#         print("Job is no longer running.")
#         break
#     time.sleep(2)  # Check every 2 seconds
# if status["status"] == "not running":
#     job_details = job_manager.get_history(job_id)
#     if job_details:
#         if "error" in job_details:
#             print(f"Job failed with error: {job_details['error']}")
#         else:
#             print_it = json.dumps(job_details, indent=4)
#             print(f"Job completed successfully. Output: {print_it}")
#     else:
#         print("No details found for the completed job.")
# else:
#     print("Job status unclear.")
