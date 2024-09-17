# Facebook Automation Script

This project automates various tasks on Facebook such as commenting, liking posts, and following accounts using the `DrissionPage` library with Chromium browser.

## Features

- **autoComment**: Automatically posts a comment on a specified Facebook post.
- **autoLike**: Automatically likes a specified Facebook post.
- **autoFollow**: Automatically follows a specified Facebook account.
- **login**: Injects cookies for account login, bypassing the manual login process.

## Prerequisites

- Python 3.x
- Chromium browser
- `DrissionPage` library
- `loguru` for logging

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ubaii/vakubot
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up `account.json` with the following structure:
    ```json
    [
        {
            "id": "user1",
            "cookie": "your_cookie_string",
            "password": "your_password",
            "port": 9222
        }
    ]
    ```

## Usage

1. **Go to Menu**
    ```bash
    python3 vakubot.py
    ```

2. **With Configuration**
    ```bash
    python3 vakubot.py --configuration your-configuration-file.json
    ```

3. **Starting Driver**
    ```bash
    python3 vakubot.py --start-driver
    ```

4. **Stopping driver**
    ```bash
    python3 vakubot.py --stop-driver
    ```

## Disclaimer!
This script is intended for educational purposes only. It demonstrates the capabilities of web automation using Python and should not be used for any activities that violate the terms of service of any platform, including Facebook.
By using this tool, you assume full responsibility for your actions. The author is not liable for any misuse or damage caused by the use of this script. Always ensure you have proper authorization and comply with the rules and guidelines of the services you interact with.

## License

This project is licensed under the MIT License.
