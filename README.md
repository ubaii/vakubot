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

1. **Auto Comment:**
    ```python
    autoComment('https://facebook.com/target_post_url', 'Your comment text')
    ```

2. **Auto Like:**
    ```python
    autoLike('https://facebook.com/target_post_url')
    ```

3. **Auto Follow:**
    ```python
    autoFollow('https://facebook.com/target_account_url')
    ```

4. **Login:**
    ```python
    login()
    ```

## License

This project is licensed under the MIT License.
