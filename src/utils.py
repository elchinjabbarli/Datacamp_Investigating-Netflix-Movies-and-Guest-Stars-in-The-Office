import logging
import os
import json
from datetime import datetime

def setup_logger():
    """
    Configures the logging system.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "app.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("AI_Presentation_Agent")

def log_interaction(prompt, response, metadata=None):
    """
    Logs prompts and responses to a JSON file for security/audit.
    """
    log_dir = "logs"
    log_file = os.path.join(log_dir, "interactions.json")

    entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response,
        "metadata": metadata or {}
    }

    try:
        data = []
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                data = json.load(f)

        data.append(entry)

        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Failed to log interaction: {e}")
