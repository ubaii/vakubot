import json, os
from loguru import logger
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.errors import ElementNotFoundError
from DrissionPage.common import Keys

def autoComment(target, comment):
    """
    Automates the process of commenting on a specified post.

    Parameters:
    target (str): The URL of the target post.
    comment (str): The comment text to be posted.
    """
    try:
        # Load account details from account.json
        with open('account.json', 'r') as account_file:
            account = json.load(account_file)
            options = ChromiumOptions()

            # Iterate over each account in the file
            for cer in account:
                try:
                    # Set options for headless mode and specify the user data path
                    options.headless(on_off=True)
                    options.set_paths(local_port=cer['port'], user_data_path=f"./data/{cer['id']}")
                    page = ChromiumPage(options)

                    # Load the target URL and ensure the page is fully loaded
                    page.get(target)
                    page.wait.doc_loaded()

                    # Redirect to the mobile (mbasic) version of the page for easier automation
                    redirect = page.url.replace('www', 'mbasic')
                    page.get(redirect)
                    page.wait.doc_loaded()

                    # Wait for the comment input form to be displayed
                    page.wait.ele_displayed('#composerInput', timeout=3)
                    formComment = page.ele('#composerInput')

                    if formComment is not None:
                        # Input the comment and submit the form
                        formComment.input(comment)
                        elevate = formComment.parent(6)
                        sbt = elevate.next()
                        sbt.ele('tag:input').click()

                        logger.success(f' [{cer["id"]}] Comment posted successfully!')
                except ElementNotFoundError:
                    logger.error(f' [{cer["id"]}] Comment form not found on the page.')
                except Exception as e:
                    logger.error(f' [{cer["id"]}] Unknown error: {e}')

    except FileNotFoundError:
        # Handle case when account.json is not found
        print("account.json not found. Please create this file with your login credentials.")
        return
    
def autoLike(target):
    """
    Automates the process of liking a specified post.

    Parameters:
    target (str): The URL of the target post.
    """
    try:
        # Load account details from account.json
        with open('account.json', 'r') as account_file:
            account = json.load(account_file)
            options = ChromiumOptions()

            # Iterate over each account in the file
            for cer in account:
                try:
                    # Set options for headless mode and specify the user data path
                    options.headless(on_off=True)
                    options.set_paths(local_port=cer['port'], user_data_path=f"./data/{cer['id']}")
                    page = ChromiumPage(options)

                    # Load the target URL and ensure the page is fully loaded
                    page.get(target)
                    page.wait.doc_loaded()

                    # Redirect to the mobile (mbasic) version of the page for easier automation
                    redirect = page.url.replace('www', 'mbasic')
                    page.get(redirect)
                    page.wait.doc_loaded()

                    # Locate and click the like button
                    likeBtn = page.ele('xpath:/html/body/div/div/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr/td[1]/a')
                    likeBtn.click()

                    logger.success(f' [{cer["id"]}] Post liked successfully!')
                except ElementNotFoundError:
                    logger.error(f' [{cer["id"]}] Like button not found on the page.')
                except Exception as e:
                    logger.error(f' [{cer["id"]}] Unknown error: {e}')

    except FileNotFoundError:
        # Handle case when account.json is not found
        print("account.json not found. Please create this file with your login credentials.")
        return

def autoFollow(target):
    """
    Automates the process of following a specified account.

    Parameters:
    target (str): The URL of the target account.
    """
    try:
        # Load account details from account.json
        with open('account.json', 'r') as account_file:
            account = json.load(account_file)
            options = ChromiumOptions()

            # Iterate over each account in the file
            for cer in account:
                try:
                    # Set options for headless mode and specify the user data path
                    options.headless(on_off=True)
                    options.set_paths(local_port=cer['port'], user_data_path=f"./data/{cer['id']}")
                    page = ChromiumPage(options)

                    # Load the target URL and ensure the page is fully loaded
                    page.get(target)
                    page.wait.doc_loaded()

                    # Redirect to the mobile (mbasic) version of the page for easier automation
                    redirect = page.url.replace('www', 'mbasic')
                    page.get(redirect)
                    page.wait.doc_loaded()

                    # Locate and click the follow button
                    followBtn = page.ele('xpath:/html/body/div/div/div[2]/div/div[1]/div[1]/div[3]/table/tbody/tr/td[2]/a')
                    followBtn.click()

                    logger.success(f' [{cer["id"]}] Followed successfully!')
                except ElementNotFoundError:
                    logger.error(f' [{cer["id"]}] Follow button not found on the page.')
                except Exception as e:
                    logger.error(f' [{cer["id"]}] Unknown error: {e}')

    except FileNotFoundError:
        # Handle case when account.json is not found
        print("account.json not found. Please create this file with your login credentials.")
        return

def login():
    """
    Handles login and cookie injection for the specified accounts.

    This function reads the account credentials from account.json, navigates to the Facebook login page, and injects cookies to bypass the login form.
    """
    try:
        # Load account details from account.json
        with open('account.json', 'r') as account_file:
            account = json.load(account_file)
            options = ChromiumOptions()

            # Iterate over each account in the file
            for cer in account:
                try:
                    # Check if user data directory exists, if not, perform login
                    if os.path.isdir(f'./data/{cer["id"]}') is False:
                        logger.info(f'[{cer["id"]}] Preparing for login')
                        options.set_paths(local_port=cer['port'], user_data_path=f"./data/{cer['id']}")
                        page = ChromiumPage(options)

                        # Navigate to Facebook and inject cookies
                        page.get('https://www.facebook.com/')
                        page.run_js_loaded(f'function setCookie(o){{...}}; var cookie="{cer["cookie"]}"; setCookie(cookie);')

                        logger.success(f"[{cer['id']}] Cookie injected successfully!")
                except Exception as e:
                    logger.error(f' [{cer["id"]}] Unknown error: {e}')

    except FileNotFoundError:
        # Handle case when account.json is not found
        print("account.json not found. Please create this file with your login credentials.")
        return
