# Gmail CLI Project

## Overview

This project is a command-line interface (CLI) tool written in Python for interacting with a user's Gmail account. It uses the official Gmail API to read and send emails.

## Features

*   **List Emails:** Fetches and displays the most recent emails from the inbox. (Implemented)
*   **Send Emails:** Composes and sends emails from the command line. (Planned)

## Setup Instructions

1.  **Prerequisites:**
    *   Python 3

2.  **Install Dependencies:**
    Install the required Google API client libraries using pip:
    ```bash
    pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
    ```

3.  **Google Cloud Project Setup:**
    *   Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
    *   Enable the **Gmail API** for your project.
    *   Navigate to **APIs & Services > OAuth consent screen**.
        *   Set the **Publishing status** to **"Testing"**.
        *   Under **"Test users"**, add your own Gmail address.
    *   Navigate to **APIs & Services > Credentials**.
        *   Click **"+ CREATE CREDENTIALS"** and select **"OAuth client ID"**.
        *   Choose **"Desktop app"** as the application type.
        *   Click **"Download JSON"** to download your client secrets and rename the file to `credentials.json`.
    *   Place the `credentials.json` file in the root of the `gmail-cli` directory.

## Usage

To run the tool, navigate to the `gmail-cli` directory in your terminal.

### List Emails

To list the 10 most recent emails:
```bash
python3 gmail_cli.py list
```

To specify the number of emails to list:
```bash
python3 gmail_cli.py list --count 5
```

### First-Time Authentication

The first time you run a command, a browser window will open, asking you to authorize the application. You may see a warning screen titled "Google hasn't verified this app". 

1.  Click on **"Advanced"**.
2.  Click on **"Go to [your app name] (unsafe)"**.
3.  Grant the requested permissions.

This will create a `token.json` file that securely stores your authorization for future sessions.
