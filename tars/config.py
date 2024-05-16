import os

events_dir = os.path.join(os.path.dirname(__file__), "events")

cli_filepath = os.path.join(os.path.dirname(__file__), "cli.py")

best_gpt_model = "gpt-4o"

router_model_name = best_gpt_model

router_config = {
    "default_none": "None",
    "options": {
        "Network": ["protocols", "ports", "encryption", "VPN"],
        "Web Application": [
            "HTML/CSS",
            "JavaScript",
            "SQL injection",
            "cross-site",
        ],
        "Wireless": ["Wi-Fi", "Bluetooth", "NFC", "security protocols"],
        "Social Engineering": [
            "phishing",
            "pretexting",
            "baiting",
            "tailgating",
        ],
        "Physical": [
            "locks",
            "security badges",
            "surveillance",
            "alarm systems",
        ],
        "Cloud": ["SaaS", "IaaS", "PaaS", "multi-tenancy"],
        "IoT": ["sensors", "smart devices", "connectivity", "home automation"],
    },
}
