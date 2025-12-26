import os
import json

def ensure_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    details_path = os.path.join(current_dir, "details.json")

    # 1️⃣ If file doesn't exist, create default
    if not os.path.exists(details_path):
        config = {"path": ""}
        with open(details_path, "w") as f:
            json.dump(config, f, indent=4)
    else:
        with open(details_path, "r") as f:
            config = json.load(f)

    path_value = config.get("path", "")
    needs_reload = not path_value

    if needs_reload:
        while True:
            path = input(
                f"Current directory path: {current_dir}\n\n"
                "Enter the path of the directory to be organized OR * for current directory: "
            ).strip()

            if not path:
                print("Path cannot be empty. Please try again.\n")
                continue

            if path != "*" and not os.path.exists(path):
                print("The entered path does not exist. Please try again.\n")
                continue

            break

        if path == "*":
            path = current_dir

        config["path"] = path

        with open(details_path, "w") as f:
            json.dump(config, f, indent=4)
