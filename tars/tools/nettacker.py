from langchain_community.tools import DuckDuckGoSearchRun
from subprocess import Popen, PIPE
from crewai_tools import tool
import subprocess
import os


def load_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


NETTACKER_DOCS = load_file(
    os.path.join(str("/".join(__file__.split("/")[:-1])), "assets/nettacker_docs.md")
)


@tool("NettackerDocs")
def get_nettacker_docs() -> str:
    """
    Grab the entire Nettacker documentation

    Returns:
    - str: Latest Nettacker documentation with examples
    """
    return NETTACKER_DOCS


@tool("Nettacker")
def nettacker(
    targets: str,
    profiles: str = None,
    modules: str = None,
    usernames: str = None,
    passwords: str = None,
    ports: str = None,
    user_agent: str = None,
    parallel_module_scan: int = 1,
    retries: int = 3,
    verbose_mode: bool = False,
    verbose_event: bool = False,
) -> str:
    """
    Executes an OWASP Nettacker scan and returns the results.

    Parameters:
    - targets (str): The IP address, hostname, or network to scan, separated by commas.
    - output_format (str, optional): Format of the output file ('txt', 'csv', 'html', 'json'), default is 'html'.
    - profiles (str, optional): Predefined set of modules (e.g., 'all', 'vuln', 'cve2021').
    - modules (str, optional): Specific module(s) to run, defaults to None which will use Nettacker's default module settings.
    - usernames (str, optional): List of usernames to use during the scan, separated by commas.
    - passwords (str, optional): List of passwords to use during the scan, separated by commas.
    - ports (str, optional): List of ports to scan, separated by commas.
    - user_agent (str, optional): Specify a user agent for HTTP requests, or use 'random_user_agent'.
    - parallel_module_scan (int, optional): Number of modules to scan in parallel.
    - retries (int, optional): Number of retries for a failed connection attempt.
    - verbose_mode (boolean, optional): verbose mode (more detailed information/logs)
    - verbose_event (boolean, optional): enable verbose event to see state of each thread (more detailed information/logs)

    Returns:
    - str: The results of the Nettacker scan or an error message.
    """

    if not targets:
        raise ValueError("Targets are required for scanning.")

    # build the command with basic and optional parameters
    base_command = f"nettacker -i {targets} "
    if modules:
        base_command += f" -m {modules}"
    if profiles:
        base_command += f" --profile {profiles}"
    if usernames:
        base_command += f" -u {usernames}"
    if passwords:
        base_command += f" -p {passwords}"
    if ports:
        base_command += f" -g {ports}"
    if user_agent:
        base_command += f" --user-agent '{user_agent}'"
    if parallel_module_scan != 1:
        base_command += f" -M {parallel_module_scan}"
    if retries != 3:
        base_command += f" --retries {retries}"
    if verbose_mode:
        base_command += f" --verbose"
    if verbose_event:
        base_command += f" --verbose-event"

    # execute the command using subprocess
    process = subprocess.Popen(
        base_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error executing Nettacker: {stderr.decode('utf-8')}")

    return stdout.decode("utf-8")


@tool("NettackerRunAllProfiles")
def nettacker_profile_all(target: str) -> str:
    """
    Run all the profiles in Nettacker where each profile is a set of modules/tools

    Parameters:
    - targets (str): The IP address, hostname, or network to scan, separated by commas.

    Returns:
    - str: The results of the Nettacker scan or an error message.
    """

    # TODO: make this into a function parameter
    verbose_mode = False
    cmd = f"nettacker -i {target} --profile all"
    if verbose_mode:
        cmd += " --verbose-event --verbose"

    # execute the command using subprocess
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error executing Nettacker: {stderr.decode('utf-8')}")

    return stdout.decode("utf-8")


@tool("NettackerRunAllModules")
def nettacker_module_all(target: str) -> str:
    """
    Run all modules in Nettacker where each module is a type of scan/tool

    Parameters:
    - targets (str): The IP address, hostname, or network to scan, separated by commas.

    Returns:
    - str: The results of the Nettacker scan or an error message.
    """

    # TODO: make this into a function parameter
    verbose_mode = False
    cmd = f"nettacker -i {target} -m all"
    if verbose_mode:
        cmd += " --verbose-event --verbose"

    # execute the command using subprocess
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error executing Nettacker: {stderr.decode('utf-8')}")

    return stdout.decode("utf-8")
