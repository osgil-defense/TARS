import sys


def crewai_result_to_json(result):
    try:
        output = {"final_output": result["final_output"], "tasks_outputs": []}
        for task_output in result["tasks_outputs"]:
            output["tasks_outputs"].append(
                {
                    "description": task_output.description,
                    "summary": task_output.summary,
                    "exported_output": task_output.exported_output,
                }
            )
        return output
    except:
        return result


def execute_and_log(func, output_filename, *args, **kwargs):
    original_stdout = sys.stdout

    with open(output_filename, "w") as f:

        class DualOutput:
            def __init__(self, terminal, file):
                self.terminal = terminal
                self.file = file

            def write(self, message):
                self.terminal.write(message)
                self.file.write(message)
                self.file.flush()

            def flush(self):
                self.terminal.flush()
                self.file.flush()

        sys.stdout = DualOutput(original_stdout, f)

        try:
            function_output = func(*args, **kwargs)
        finally:
            sys.stdout = original_stdout

    return function_output, output_filename
