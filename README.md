# External Link Checker

External Link Checker is a Python-based tool designed to help website administrators maintain the integrity of their external links. It scrapes a website recursively from the homepage, identifies all external links, and periodically checks their validity to ensure they are not leading to malicious or inactive sites. This project aims to prevent potential security risks and protect brand reputation by ensuring that all external links remain safe and relevant over time.

## Features

- Recursively scrape links from a given base URL
- Identify and collect external links
- Save external links and their source pages to a CSV file
- Disable SSL verification to handle sites with SSL/TLS issues

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `urllib3`

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Visual Studio Code with Remote - Containers extension installed
- WSL (Windows Subsystem for Linux) set up

### Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/ShutoYamada/external-link-checker.git
    cd external-link-checker
    ```

2. Open the project in Visual Studio Code.

3. When prompted, select "Reopen in Container" to open the project in a devcontainer.

### Usage
1. Ensure you are in the root directory of the project.

2. Run the following command to scrape external links and save the results to a CSV file:
    ```sh
    python external_link_checker.py https://yourcompanywebsite.com output.csv
    ```

    Replace `https://yourcompanywebsite.com` with the URL of the website you want to scrape, and `output.csv` with the desired output file name.

## Project Structure
```
root/
├── .devcontainer/
│ ├── Dockerfile
│ └── devcontainer.json
├── requirements.txt
└── external_link_checker.py
```

## Contributions
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License
This project is licensed under the MIT License.