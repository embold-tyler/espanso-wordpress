# WordPress CLI Update Command Generator

Generate a command from WP CLI output to update and commit a plugin or theme.

## Requirements

- Python 3.x
- [`pyperclip`](https://pypi.org/project/pyperclip/) (`pip install pyperclip`)
- [Espanso](https://espanso.org/) 2.2.3+

## Installation

### Option 1: Install the Full `espanso-wordpress` Package

You can install the entire package, which includes this and other related plugins.

**Method A: Using Espanso CLI**
1. In a terminal, run:  
   `espanso install espanso-wordpress --git git@github.com:emboldagency/espanso-wordpress.git --external`

**Method B: Manual Clone**
1. Download or clone the [`espanso-wordpress`](https://github.com/emboldagency/espanso-wordpress) repository into your Espanso `match/packages` directory.

After either method, **restart Espanso**.

---

### Option 2: Manual Installation (Single Plugin)

If you only want this plugin or wish to customize it:

1. Copy the `wp-cli-update-cmd` folder into your Espanso `match/packages` directory, in an espanso-wordpress folder:
    ```
    <espanso-config>/match/packages/espanso-wordpress/wp-cli-update-cmd/
    ```
2. Ensure `process_wp_cli_update_output.py` is present in the plugin folder.
3. Restart Espanso.

## Usage

1. **Copy** the relevant line from your WP CLI output, for example:
    ```
    | advanced-custom-fields-pro | active | available | 6.4.0.1 | 6.4.0.1 | off |
    ```
2. **Trigger the snippet** in any app by typing:

    - `:wp_up_plugin` — for plugin updates
    - `:wp_up_theme` — for theme updates

    (Alternate triggers can be added in `package.yml` as needed.)

3. The snippet will expand to a git command, e.g.:
    ```shell
    git add wp-content/plugins/advanced-custom-fields-pro;git commit -m "PLUGIN: Update advanced-custom-fields-pro from 6.4.0.1 to 6.4.0.1"
    ```

## Customization

- You can add more triggers or modify the script path in `package.yml` as needed.
- The script expects the WP CLI output to be in a pipe-delimited format.

## Troubleshooting

- If nothing happens, ensure Python and `pyperclip` are installed and available in your PATH.
- Check Espanso logs for errors if the snippet does not expand as expected.

# Espanso WordPress WP-CLI Update Automation

This package provides Espanso triggers and a Python script to automate the process of updating WordPress plugins/themes and generating ready-to-run git commit commands.

## Triggers and Workflow

### 1. `:wp_plugin_cmd:`
- **Purpose:** Generate a one-liner command to update a plugin, stage its files, and commit the change.
- **How to use:**
  1. Type `:wp_plugin_cmd:` in any text field.
  2. Enter the plugin slug (e.g. `wordpress-seo`).
  3. The output will be a command like:
     ```sh
     wp plugin update wordpress-seo && git add wp-content/plugins/wordpress-seo && git commit -m "PLUGIN: Update wordpress-seo from 25.1 to 25.4"
     ```
  4. Copy and run this command in your terminal/SSH session.

### 2. `:wp_plugin_json:`
- **Purpose:** Generate the update+git+commit command from JSON output (useful if you already have plugin/theme info in JSON format).
- **How to use:**
  1. Run `wp plugin get <slug> --format=json` or `wp theme get <slug> --format=json` and copy the JSON output to your clipboard.
  2. Type `:wp_plugin_json:` and select plugin or theme.
  3. The output will be the ready-to-run update+git+commit command for that item.

### 3. `:clipdebug:`
- **Purpose:** Debug utility to output the current clipboard contents.
- **How to use:**
  1. Type `:clipdebug:` to see what is currently in your clipboard.

## Python Script: `process_wp_cli_update_output.py`
- Accepts either a plugin/theme slug (and queries WP-CLI for info) or a JSON blob (from WP-CLI output).
- Outputs a single-line command to update, stage, and commit the plugin/theme update.
- Handles errors and missing data gracefully.

## Example Workflow
1. **Get plugin info as JSON:**
   ```sh
   wp plugin list --format=json --name=wordpress-seo
   # or
   wp plugin get wordpress-seo --format=json
   ```
2. **Copy the JSON output.**
3. **Trigger `:wp_plugin_json:` in Espanso.**
4. **Paste the JSON if prompted, or let Espanso use the clipboard.**
5. **Copy and run the generated command in your terminal.**

## Notes
- All commands are designed to be run on your server or in an environment where WP-CLI and git are available.
- The triggers are flexible and can be extended for themes or other workflows.
- For custom plugin slugs, simply enter the slug when prompted.

---

**Maintained by:** You!
