import sys
import argparse
import subprocess
import json

import os


def main():
    parser = argparse.ArgumentParser(
        description="Generate WP-CLI update and git commit commands from JSON, plugin name, or file."
    )
    parser.add_argument(
        "update_type",
        choices=["plugin", "theme"],
        help="Type of update (plugin or theme)",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--json",
        dest="json_input",
        help="Paste the JSON output from 'wp <type> list <name> --format=json'",
    )
    group.add_argument(
        "--name",
        dest="item_name",
        help="Plugin or theme slug to query via WP-CLI",
    )
    group.add_argument(
        "--file",
        dest="json_file",
        help="Path to a file containing JSON output from 'wp <type> list --format=json --name=<slug>'",
    )
    args = parser.parse_args()

    type_word = args.update_type

    if args.json_input:
        try:
            item = json.loads(args.json_input)
            if isinstance(item, list):
                if not item:
                    print("Error: JSON list is empty.", file=sys.stderr)
                    sys.exit(1)
                item = item[0]
        except json.JSONDecodeError:
            print(
                "Error: Failed to parse JSON input. Please provide valid JSON output from WP-CLI.",
                file=sys.stderr,
            )
            sys.exit(1)
    elif args.json_file:
        try:
            with open(args.json_file, "r") as f:
                items = json.load(f)
        except Exception as e:
            print(
                f"Error reading or parsing file '{args.json_file}': {e}",
                file=sys.stderr,
            )
            sys.exit(1)
        if not items or not isinstance(items, list):
            print(f"No items found in file '{args.json_file}'.", file=sys.stderr)
            sys.exit(1)
        item = items[0]
        # Delete the file after reading
        try:
            os.remove(args.json_file)
        except Exception as e:
            print(
                f"Warning: Could not delete file '{args.json_file}': {e}",
                file=sys.stderr,
            )
    elif args.item_name:
        # Run wp <type> list --format=json --name=<slug>
        cmd = ["wp", type_word, "list", "--format=json", f"--name={args.item_name}"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        except FileNotFoundError:
            print(
                "Error: 'wp' command not found. Please run this script in an environment where WP-CLI is available.",
                file=sys.stderr,
            )
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Error running {' '.join(cmd)}: {e.stderr}", file=sys.stderr)
            sys.exit(1)
        try:
            items = json.loads(result.stdout)
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON output from WP-CLI.", file=sys.stderr)
            sys.exit(1)
        if not items or not isinstance(items, list):
            print(
                f"No {type_word} found with name '{args.item_name}'.", file=sys.stderr
            )
            sys.exit(1)
        item = items[0]
    else:
        print("Error: Must provide either --json, --name, or --file.", file=sys.stderr)
        sys.exit(1)

    item_name = item.get("name") or item.get("slug") or "unknown"
    old_version = item.get("version", "unknown")
    new_version = item.get("update_version", "unknown")

    content_path = f"wp-content/{type_word}s/{item_name}"
    commit_prefix = type_word.upper()
    wp_command = f"wp {type_word} update {item_name}"

    # Output as a single line with &&
    output_string = (
        f"{wp_command} && "
        f"git add {content_path} && "
        f'git commit -m "{commit_prefix}: Update {item_name} from {old_version} to {new_version}"'
    )
    print(output_string)


if __name__ == "__main__":
    main()
