# External Link Checker

External Link Checker is a Python-based tool designed to help website administrators maintain the integrity of their external links. It scrapes a website recursively from the homepage, identifies all external links, and periodically checks their validity to ensure they are not leading to malicious or inactive sites. This project aims to prevent potential security risks and protect brand reputation by ensuring that all external links remain safe and relevant over time.

## Features

- Recursively scrape links from a given base URL
- Identify and collect external links
- Save external links, their source pages, and safety status to a CSV file
- Disable SSL verification to handle sites with SSL/TLS issues
- Proxy support for network configurations
- Exclude non-http/https links from safety checks but include them in the CSV output

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `urllib3`
- `python-dotenv`
- `google-cloud-webrisk`

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

2. Create a `.env` file in the project root and add your Google API key:
    ```plaintext
    GOOGLE_API_KEY=your_api_key_here
    ```

3. Open the project in Visual Studio Code.

4. When prompted, select "Reopen in Container" to open the project in a devcontainer.

### Usage
1. Ensure you are in the root directory of the project.

2. Run the following command to scrape external links and save the results to a CSV file and screenshots in a specified directory:
    ```sh
    python external_link_checker.py https://yourcompanywebsite.com output
    ```

Replace `https://yourcompanywebsite.com` with the URL of the website you want to scrape, and `output` with the desired output directory name. The tool will save the external links and their details to `output/output.csv`, and screenshots of the external links to the `output/` directory.

To scrape external links without saving screenshots, use the `--no-screenshots` option:
    ```sh
    python external_link_checker.py https://yourcompanywebsite.com output --no-screenshots
    ```

In this case, only the CSV file (`output/output.csv`) will be saved, and no screenshots will be taken.

### Environment Variables
- `GOOGLE_API_KEY`: Your Google API key for accessing the Web Risk API.

## Project Structure
```
root/
├── .devcontainer/
│ ├── Dockerfile
│ └── devcontainer.json
├── requirements.txt
├── external_link_checker.py
└── .env (not included in version control)
└── .env.example
```

## Contributions
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License
This project is licensed under the MIT License.