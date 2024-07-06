# Obsidian2HugoBridge

## Project Description

Simplify your knowledge management process by exporting from Obsidian and publishing to your Hugo website with one click. No manual conversion needed; automate all the details so you can focus on content creation. Supports the latest version of Obsidian and is compatible with various Hugo themes.

## Features

- **Markdown Conversion**: Converts Markdown files to Hugo-compatible format, including custom admonition blocks.
- **Content Replacement**: Replaces specified URLs within the Markdown content.
- **Front Matter Handling**: Removes `url` and `git_commit` fields from the Markdown file's front matter.
- **WSL Integration**: Copies converted Markdown files to a specified directory in the Hugo repository within WSL.
- **Command Execution**: Executes a series of commands, including previewing Hugo content, committing to the repository, updating CDN, and updating Algolia.

## Prerequisites

- Python 3.7+
- WSL (Windows Subsystem for Linux), Debian-based Linux distribution
- Hugo installed in WSL
- Node.js installed in WSL (for Algolia and Tencent cloud CDN commands)

## Installation

1. Clone the repository to your local machine:
    ```sh
    git clone https://github.com/raylanb/obsidian_to_hugo.git
    cd obsidian_to_hugo
    ```

2. Move the code to `.obsidian\scripts\python` directory:
    ```sh
    cp main.py Path\.obsidian\scripts\python
    ```

3. Ensure that WSL is installed and configured. Install Hugo and Node.js in the WSL environment if not already installed.

## Configuration

- **Paths and URLs**: Update paths and URLs in the script as needed. Ensure `wsl_directory` and `wsl_commands` match your WSL environment and project structure.
- **Configure Image Domains**: In `replacements`, set your private domain on the left and public domain on the right.
- **Change Path Prefix**: In `convert_to_wsl_path`, update the prefix address, such as `G:/mydrive` and `//wsl.localhost/Debian`.

## Usage

First, install obsidian-python-scripter.

Repository: [obsidian-python-scripter](https://github.com/nickrallison/obsidian-python-scripter)

Front Matter Template: (Try to include `draft`, `url`, `git_commit`. If not needed, you can remove them and adjust the code accordingly.)

```toml
---
title: "{{title}}"
date: "{{date}}"
lastmod: "{{date}}"
draft: true
ruby: false
fraction: false
math:
  enable: false
share:
  enable: true
summary: ""
tags: 
categories:
  - ""
featuredImagePreview: 
featuredImage: 
url: 
git_commit:
---
```

Then, run the script using obsidian-python-scripter.

## Detailed Script Description

### Functions

- **convert_markdown(input_path, output_path)**:
  - Reads the Markdown file from `input_path`, converts it to Hugo-compatible format with admonition blocks, and writes the result to `output_path`.

- **copy_to_wsl(source_path, destination_directory)**:
  - Copies the file from `source_path` to the `destination_directory` in the WSL environment, overwriting existing files.

- **convert_to_wsl_path(windows_path)**:
  - Converts a Windows file path to a WSL-compatible path.

- **extract_fields(input_path, field_names=['url', 'git_commit'])**:
  - Extracts specified fields from the front matter of the Markdown file.

- **execute_in_wsl(commands)**:
  - Executes a list of commands in the WSL environment.

- **stop_hugo_server()**:
  - Stops any running Hugo server instances in WSL.

### Main Script Workflow

1. **Argument Parsing**:
   - Parses command-line arguments to get the paths for the vault and the specific Markdown file.

2. **File Path Validation**:
   - Validates that the specified Markdown file exists.

3. **Field Extraction**:
   - Extracts `url`, `git_commit`, and `draft` values from the front matter of the Markdown file.

4. **Markdown Conversion**:
   - Converts the Markdown file to a Hugo-compatible format.

5. **File Copying**:
   - Copies the converted Markdown file to the specified directory in WSL.

6. **Command Execution**:
   - Executes appropriate WSL commands based on the `draft` status, including previewing or publishing.

## Error Handling

- The script includes detailed error handling to capture and log exceptions. Errors are printed to the console and optionally logged to an `error.log` file.

## Contribution

Contributions are welcome through issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.