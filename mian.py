import os
import re
import shutil
import subprocess
import sys
import webbrowser


def convert_markdown(input_path, output_path):
    # Read the content of the input Markdown file
    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regular expression to match admonition blocks in Markdown
    pattern = re.compile(
        r'> \[!(\w+)] (.*?)\n(> .*?(\n|$))*',
        re.DOTALL
    )

    # Dictionary for URL replacements
    replacements = {
        "https://im.example.com": "https://image.yourdomain.com"
    }
    for old, new in replacements.items():
        content = content.replace(old, new)

    # Replacement function to convert matched groups
    def replace_func(match):
        # match.group(1): Admonition type (e.g., tip, info, note, warning)
        # match.group(2): Admonition title, may be empty
        # match.group(3): Admonition content, may contain multiple lines
        type_ = match.group(1).strip()
        title = match.group(2).strip()
        content = match.group(3)
        if content is None:
            content = ""
        else:
            content = content.replace('>', '').strip()
        # Construct Hugo shortcodes, ensuring content is between two admonition tags
        return f"{{{{< admonition {type_} {title} true >}}}}\n{content}\n{{{{< /admonition >}}}}\n"

    # Apply the regex and replacement function
    converted_content = pattern.sub(replace_func, content)

    # Remove url and git_commit fields from the converted content
    converted_lines = converted_content.split('\n')
    new_lines = []
    in_front_matter = False
    front_matter_count = 0

    for line in converted_lines:
        if line.strip() == '---':
            in_front_matter = not in_front_matter
            front_matter_count += 1
            new_lines.append(line)
        elif in_front_matter and front_matter_count == 1:
            if not line.startswith("url:") and not line.startswith("git_commit:"):
                new_lines.append(line)
        else:
            new_lines.append(line)
    converted_content = '\n'.join(new_lines)

    # Write the converted content to the output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(converted_content)

def copy_to_wsl(source_path, destination_directory):
    # Check if the source file exists
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"The source file {source_path} does not exist.")
    
    # Convert Windows path to WSL path
    wsl_destination = convert_to_wsl_path(destination_directory)

    # Check if destination file exists in WSL
    dest_file = os.path.join(wsl_destination, os.path.basename(source_path))
    if os.path.exists(dest_file):
        print(f"Destination file {dest_file} already exists. Overwriting...")
    
    # Copy file to WSL using shutil.copyfile() for overwriting
    shutil.copyfile(source_path, dest_file)

def convert_to_wsl_path(windows_path):
    # Convert Windows path to WSL path format
    wsl_path = windows_path.replace("\\", "/").replace("G:/mydrive", "//wsl.localhost/Debian")
    return wsl_path

def extract_fields(input_path, field_names=['url', 'git_commit']):
    field_values = {}

    # Open and read the input Markdown file
    with open(input_path, 'r', encoding='utf-8') as file:
        # Check if the first line is "---"
        if file.readline().strip() != "---":
            return field_values

        for line in file:
            line = line.strip()
            if line == "---":
                break  # Stop reading at the second "---"

            for field_name in field_names:
                if line.startswith(f"{field_name}:"):
                    field_values[field_name] = line.split(":", 1)[1].strip()

    return field_values

def execute_in_wsl(commands):
    # Join the list of commands with "&&" to form a single command
    full_command = " && ".join(commands)
    try:
        # Execute the command in WSL
        subprocess.run(["wsl", "-e", "bash", "-c", full_command], check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        return False

def stop_hugo_server():
    # Command to stop any running Hugo server instances in WSL
    command = "pids=$(pgrep -f 'hugo server') && if [ -n \"$pids\" ]; then echo $pids | xargs kill -9; fi"
    try:
        subprocess.run(["wsl", "-e", "bash", "-c", command], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pass

if __name__ == "__main__":
    # Check for correct number of command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python main.py <vault_path> <file_path>")
        sys.exit(1)
    
    # Paths from command line arguments
    python_script = sys.argv[0]
    vault_path = sys.argv[1]
    file_path = sys.argv[2]

    abs_file_path = os.path.abspath(os.path.join(vault_path, file_path))

    # Check if the specified Markdown file exists
    if not os.path.exists(abs_file_path):
        sys.exit(1)

    print(f"This is the open file: {abs_file_path}")

    try:
        # Extract the URL, git_commit, and draft values
        field_values = extract_fields(abs_file_path, ["url", "git_commit", "draft"])
        url_value = field_values["url"]
        git_commit = field_values["git_commit"]
        draft = field_values["draft"].lower() == "true"  # Convert string to boolean
        
        # Define paths
        converted_file = os.path.join(vault_path, f"{url_value}.md")

        wsl_directory = "//wsl.localhost/Debian/Path/File/content/posts"  # Destination directory in WSL
        wsl_commands = [
            "cd /Path/File"
        ]

        # Conditionally add the hugo_algolia command based on the draft status
        # If GPG is configured, you need to go to WSL for verification before it can be completed. Otherwise, it will fail.
        # keychain --eval --agents gpg <sec   rsa4096/xxxxxx ,Please input xxxxxx here.>
        
        if draft:
            stop_hugo_server()
            wsl_commands.insert(1, f"/snap/bin/hugo server -D")
            # Open the browser and access http://localhost:1313/
            webbrowser.open("http://localhost:1313/")
        else:
            wsl_commands.insert(1, f"rm -rf public && /snap/bin/hugo --minify && git add . && git commit -m  \'{git_commit}\' && git push -u origin main && npm run algolia && npm run qcloudcdn")
        
        # Step 1: Convert the Markdown file
        convert_markdown(abs_file_path, converted_file)

        # Step 2: Copy the converted file to the WSL directory
        copy_to_wsl(converted_file, wsl_directory)

        if os.path.exists(converted_file):
            os.remove(converted_file)

        # Step 3: Execute commands in WSL
        execute_in_wsl(wsl_commands)
    
    except Exception as e:
        # Print detailed error message
        error_message = f"Error: {e}"
        print(error_message)

        # Optionally, log the error message to a file
        with open("error.log", "a", encoding="utf-8") as error_file:
            error_file.write(error_message + "\n")