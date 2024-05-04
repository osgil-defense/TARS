from crewai_tools import tool
import subprocess


ROOT_ZAP_DOCKER_CMD = "docker run -t ghcr.io/zaproxy/zaproxy:stable"


@tool("ZAPFullScan")
def zap_full_scan(
    target: str,
    mins: int = None,
    include_alpha: bool = False,
    debug: bool = False,
    port: int = None,
    delay_secs: int = None,
    info_by_default: bool = False,
    no_fail_on_warn: bool = False,
    use_ajax_spider: bool = False,
    output_level: str = None,
    short_output: bool = False,
    max_time: int = None,
    user: str = None,
) -> str:
    """
    Run a ZAP Full Scan which performs a comprehensive security test on the specified target. This includes using the ZAP spider, optional Ajax spider, and a full active scan. This scan may perform actual ‘attacks’ and can run for a prolonged period of time.

    Parameters:
    - target (str): Target URL including the protocol, eg https://www.example.com.
    - mins (int, optional): Number of minutes to run the spider; defaults to no limit.
    - include_alpha (bool, optional): Include alpha quality active and passive scan rules.
    - debug (bool, optional): Enable debug messages.
    - port (int, optional): Specify the listening port.
    - delay_secs (int, optional): Delay in seconds before passive scanning.
    - info_by_default (bool, optional): Set rules not specified in the config to INFO level.
    - no_fail_on_warn (bool, optional): Do not fail the scan on warnings.
    - use_ajax_spider (bool, optional): Use the Ajax spider in addition to the traditional one.
    - output_level (str, optional): Set the minimum output level (PASS, IGNORE, INFO, WARN, FAIL).
    - short_output (bool, optional): Use a shorter output format, omitting PASSes and example URLs.
    - max_time (int, optional): Maximum time in minutes to allow for the entire scan process.
    - user (str, optional): Username for authenticated scans.

    Returns:
    - str: The results of the ZAP Full Scan or an error message.
    """

    base_command = f"{ROOT_ZAP_DOCKER_CMD} zap-full-scan.py -t {target}"

    # Add optional parameters to the command
    if mins:
        base_command += f" -m {mins}"
    if include_alpha:
        base_command += " -a"
    if debug:
        base_command += " -d"
    if port:
        base_command += f" -P {port}"
    if delay_secs:
        base_command += f" -D {delay_secs}"
    if info_by_default:
        base_command += " -i"
    if no_fail_on_warn:
        base_command += " -I"
    if use_ajax_spider:
        base_command += " -j"
    if output_level:
        base_command += f" -l {output_level}"
    if short_output:
        base_command += " -s"
    if max_time:
        base_command += f" -T {max_time}"
    if user:
        base_command += f" -U {user}"

    print(f"Running Zaproxy command: {base_command}")

    # Execute the command using subprocess
    process = subprocess.Popen(
        base_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    # # TODO: find a better solution for this
    # if process.returncode != 0:
    #     return f"Error executing ZAP Full scan: {stderr.decode('utf-8')}"

    return stdout.decode("utf-8")


@tool("ZAPAPIScan")
def zap_api_scan(
    target: str,
    format: str,
    include_alpha: bool = False,
    debug: bool = False,
    port: int = None,
    delay_secs: int = None,
    info_by_default: bool = False,
    no_fail_on_warn: bool = False,
    output_level: str = None,
    safe_mode: bool = False,
    max_time: int = None,
    user: str = None,
    hostname_override: str = None,
) -> str:
    """
    Run a ZAP API Scan which imports an API definition and then runs an Active Scan against the URLs found. This tool is specially tuned for APIs defined by OpenAPI, SOAP, or GraphQL.

    Parameters:
    - target (str): API definition (OpenAPI, SOAP) URL or file, or GraphQL endpoint URL.
    - format (str): Type of API definition, options are 'openapi', 'soap', 'graphql'.
    - include_alpha (bool, optional): Include alpha quality passive scan rules.
    - debug (bool, optional): Enable debug messages.
    - port (int, optional): Specify the listening port.
    - delay_secs (int, optional): Delay in seconds before passive scanning.
    - info_by_default (bool, optional): Set rules not specified in the config file to INFO level.
    - no_fail_on_warn (bool, optional): Do not fail the scan on warnings.
    - output_level (str, optional): Set the minimum output level (PASS, IGNORE, INFO, WARN, FAIL).
    - safe_mode (bool, optional): Skip the active scan and perform a baseline scan instead.
    - max_time (int, optional): Maximum time in minutes to allow for the entire scan process.
    - user (str, optional): Username for authenticated scans.
    - hostname_override (str, optional): Hostname to override in the API definition.

    Returns:
    - str: The results of the ZAP API scan or an error message.
    """

    base_command = f"{ROOT_ZAP_DOCKER_CMD} zap-api-scan.py -t {target} -f {format}"

    supported_formats = ["openapi", "soap", "graphql"]
    if str(format) not in supported_formats:
        raise Exception(f"format {format} is NOT a valid format ({supported_formats})")

    # Add optional parameters to the command
    if include_alpha:
        base_command += " -a"
    if debug:
        base_command += " -d"
    if port:
        base_command += f" -P {port}"
    if delay_secs:
        base_command += f" -D {delay_secs}"
    if info_by_default:
        base_command += " -i"
    if no_fail_on_warn:
        base_command += " -I"
    if output_level:
        base_command += f" -l {output_level}"
    if safe_mode:
        base_command += " -S"
    if max_time:
        base_command += f" -T {max_time}"
    if user:
        base_command += f" -U {user}"
    if hostname_override:
        base_command += f" -O {hostname_override}"

    print(f"Running Zaproxy command: {base_command}")

    # Execute the command using subprocess
    process = subprocess.Popen(
        base_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    # # TODO: find a better solution for this
    # if process.returncode != 0:
    #     return f"Error executing ZAP API scan: {stderr.decode('utf-8')}"

    return stdout.decode("utf-8")


@tool("ZAPBaselineScan")
def zap_baseline_scan(
    target: str,
    minutes: int = 1,
    include_alpha: bool = False,
    debug: bool = False,
    port: int = None,
    delay_secs: int = None,
    info_by_default: bool = False,
    no_fail_on_warn: bool = False,
    use_ajax_spider: bool = False,
    output_level: str = None,
    max_time: int = None,
    user: str = None,
    zap_options: str = None,
) -> str:
    """
    Run a ZAP Baseline Scan which operates by running the ZAP spider against a target for about a minute, following up with passive scanning, and then reporting results, primarily as WARNings, though settings can be adjusted via a config file. Designed for CI/CD environments, it is safe for production sites and completes its process in just a few minutes without performing real attacks.

    Parameters:
    - target (str): The target URL, including protocol, eg https://www.example.com.
    - minutes (int, optional): Duration in minutes to run the spider (default is 1).
    - include_alpha (bool, optional): Whether to include alpha passive scan rules.
    - debug (bool, optional): Enable debug messages.
    - port (int, optional): Specify the listen port.
    - delay_secs (int, optional): Delay in seconds to wait for passive scanning.
    - info_by_default (bool, optional): Set default rules not in the config file to INFO.
    - no_fail_on_warn (bool, optional): Do not return failure on warning.
    - use_ajax_spider (bool, optional): Use the Ajax spider in addition to the traditional one.
    - output_level (str, optional): Minimum level to show: PASS, IGNORE, INFO, WARN, or FAIL.
    - max_time (int, optional): Maximum time in minutes to wait for ZAP to start and the passive scan to run.
    - user (str, optional): Username for authenticated scans.
    - zap_options (str, optional): Additional ZAP command line options.

    Returns:
    - str: The results of the ZAP Baseline scan or an error message.
    """

    base_command = f"{ROOT_ZAP_DOCKER_CMD} zap-baseline.py -t {target}"

    if minutes:
        base_command += f" -m {minutes}"
    if include_alpha:
        base_command += " -a"
    if debug:
        base_command += " -d"
    if port:
        base_command += f" -P {port}"
    if delay_secs:
        base_command += f" -D {delay_secs}"
    if info_by_default:
        base_command += " -i"
    if no_fail_on_warn:
        base_command += " -I"
    if use_ajax_spider:
        base_command += " -j"
    if output_level:
        base_command += f" -l {output_level}"
    if max_time:
        base_command += f" -T {max_time}"
    if user:
        base_command += f" -U {user}"
    if zap_options:
        base_command += f" -z '{zap_options}'"

    print(f"Running Zaproxy command: {base_command}")

    # Execute the command using subprocess
    process = subprocess.Popen(
        base_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    # # TODO: find a better solution for this
    # if process.returncode != 0:
    #     return f"Error executing ZAP Baseline scan: {stderr.decode('utf-8')}"

    return stdout.decode("utf-8")


@tool("ZAPGeneralUse")
def zap_general_use(
    target: str,
    low_mem: bool = False,
    silent: bool = False,
    quick_url: str = None,
    zap_it: str = None,
) -> str:
    """
    Execute a ZAP CLI command where you can configure certain parameters of the scan though the CLI

    Parameters:
    - target (str): The URL address of the website that will be targeted for an attack.
    - low_mem (bool, optional): Use low memory options.
    - silent (bool, optional): Run ZAP without making unsolicited requests.
    - quick_url (str, optional): URL for quick attack.
    - zap_it (str, optional): URL for a quick reconnaissance scan.

    Returns:
    - str: The results of the ZAP operation or an error message.
    """

    base_command = f"zaproxy -cmd"

    if low_mem:
        base_command += " -lowmem"
    if silent:
        base_command += " -silent"
    if quick_url:
        base_command += f" -quickurl {quick_url}"
    if zap_it:
        base_command += f" -zapit {zap_it}"

    base_command += f" {target}"

    print(f"Running Zaproxy command: {base_command}")

    # Execute the command using subprocess
    process = subprocess.Popen(
        base_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error executing ZAP: {stderr.decode('utf-8')}")

    return stdout.decode("utf-8")
