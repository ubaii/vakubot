import json, os, time, sys, argparse, random
from loguru import logger
from lib.banner import show
from lib import bot
from DrissionPage.errors import PageDisconnectedError
from DrissionPage import ChromiumPage, ChromiumOptions

logger.add("console.log")

def checkData(options: ChromiumOptions):
    """
    This function checks if the required directories for each account exist.
    If they don't, it creates them using the account information from 'account.json'.
    It also initializes the Chromium options for each account.

    Parameters:
    options (ChromiumOptions): The Chromium options to be set for each account.
    """
    try:
        with open('account.json', 'r') as account_file:
            account = json.load(account_file)
            for cer in account:
                if not os.path.isdir(f'data/{cer["id"]}'):
                    logger.info(f'Creating for {cer["id"]}')
                    options.set_user_data_path(f"data/{cer['id']}")
                    page = ChromiumPage(options)
                    page.quit()
    except FileNotFoundError:
        print("account.json not found. Please create this file and place with your account list credentials.")
        return
    
def startDriver(options: ChromiumOptions):
    """
    This function starts a Chromium driver with the given options and initializes the accounts.
    It checks if the 'account.json' file exists and loads the account credentials.
    For each account, it sets the user data path and retrieves the 'c_user' cookie value.
    The function returns a list of 'c_user' cookie values for the initialized accounts.

    Parameters:
    options (ChromiumOptions): The options for the Chromium driver.

    Returns:
    List[str]: A list of 'c_user' cookie values for the initialized accounts.
    """
    try:
        logger.info('Checking cookies...')
        c_user = []
        with open('account.json', 'r') as account_file:
            account = json.load(account_file)
            for cer in account:
                options.headless(on_off=True)
                options.set_paths(local_port=cer['port'], user_data_path=f"data/{cer['id']}")
                page = ChromiumPage(options)
                page.get('https://mbasic.facebook.com/')
                cookies = page.cookies()
                cookie_c_user = next((cookie for cookie in cookies if cookie['name'] == 'c_user'), None)
                if cookie_c_user:
                    if page.wait.ele_displayed('#mbasic-composer-form', timeout=2) and page.ele('#mbasic-composer-form'):
                        c_user.append(cookie_c_user['value'])
                        logger.success(f' [{cookie_c_user["value"]}] Ready! ')
                    else:
                        logger.error(f' [{cer["id"]}] Composer not found. Please check your credentials.')
                else:
                    logger.error(f' [{cer["id"]}] Cookie not found. Please check your credentials.')
            return c_user
    except FileNotFoundError:
        print("account.json not found. Please create this file with your login credentials.")
        return
    except PageDisconnectedError:
        logger.error('Driver unexpectedly disconnected')
        return
    
def stopDriver():
    """
    This function stops the Chromium driver by terminating all Chrome processes.

    It logs the process and handles any errors that may occur during termination.
    """
    logger.info('Stopping driver...')
    try:
        os.system("killall -9 chrome")
        logger.success('Driver stopped')
    except Exception as e:
        logger.error(f'Error stopping driver: {str(e)}')

def menu(account):
    """
    This function presents a menu to the user for selecting automation actions such as auto-comment, auto-like, and auto-follow.

    It handles user input and executes the corresponding bot actions based on the selection.

    Parameters:
    account (List): A list of accounts to be displayed and used.
    """
    try:
        print(show())
        print(f'Available account: {len(account)}\n')
        print("1. Auto Comment")
        print("2. Auto Like")
        print("3. Auto Follow")
        print("0. Exit")

        choice = int(input("Choice what you want: "))
        if choice == 1:
            target = input("Enter url of post: ")
            comment = input("Enter comment: ")
            bot.autoComment(target, comment)
            time.sleep(2)
            menu(account)
        elif choice == 2:
            target = input("Enter url of post: ")
            bot.autoLike(target)
            time.sleep(2)
            menu(account)
        elif choice == 3:
            target = input("Enter url of account: ")
            bot.autoFollow(target)
            time.sleep(2)
            menu(account)
        elif choice == 0:
            logger.info("Stopping driver...")
            stopDriver()
            logger.info('Exiting...')
            exit()
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)
            menu(account)
    except KeyboardInterrupt:
        logger.info("Stopping driver...")
        stopDriver()
        logger.info('Exiting...')
        sys.exit(0)
    except ValueError:
        print("Invalid choice. Please try again.")
        time.sleep(1)
        menu(account)
    except Exception as e:
        logger.error(f'An error occurred: {str(e)}')
        time.sleep(5)
        menu(account)

def main():
    """
    This is the main function that initializes the Chromium driver options, checks account data,
    and starts the menu for user interaction.

    It handles missing settings files and uses default settings if necessary.
    """
    options = ChromiumOptions()
    try:
        with open('settings.json', 'r') as settings_file:
            settings = json.load(settings_file)
            for opt in settings['chrome']:
                options.set_argument(opt)
    except FileNotFoundError:
        print("settings.json not found. Using default settings.")

    logger.info('Checking data...')
    checkData(options)

    logger.info('Starting Driver and initialize account...')
    account = startDriver(options)

    menu(account)

if __name__ == "__main__":
    """
    This is the entry point of the program, which handles command-line arguments and starts the main process.

    It provides options for starting and stopping the driver, logging in, and performing automation tasks.
    """
    parser = argparse.ArgumentParser(description='Facebook automation bot')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-sD', '--start-driver', action='store_true', help="Run the driver")
    parser.add_argument('-stD', '--stop-driver', action='store_true', help="Stop the driver")
    parser.add_argument('-l', '--login', action='store_true', help="Login and save cookie of facebook account")
    parser.add_argument('-aC', '--auto-comment', type=str, help="Url of post for auto-comment")
    parser.add_argument('-aL', '--auto-like', type=str, help="Url of post for auto-like")
    parser.add_argument('-aF', '--auto-follow', type=str, help="Url of account for auto-follow")
    parser.add_argument('-cM', '--comment', type=str, help="Comment value for auto-comment")
    parser.add_argument('-c', '--configuration', type=str, help="Configuration file")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        main()

    if args.login:
        print(show())
        bot.login()
        exit()

    if args.stop_driver:
        stopDriver()
        exit()

    if args.start_driver:
        options = ChromiumOptions()
        try:
            with open('settings.json', 'r') as settings_file:
                settings = json.load(settings_file)
                for opt in settings['chrome']:
                    options.headless(on_off=True)
                    options.set_argument(opt)
        except FileNotFoundError:
            print("settings.json not found. Using default settings.")

        logger.info('Checking data...')
        checkData(options)

        logger.info('Starting Driver and initialize account...')
        account = startDriver(options)

    if args.auto_comment:
        if args.comment is None:
            print("Error: --comment is required for auto-comment")
        else:
            print(show())
            bot.autoComment(args.auto_comment, args.comment)
        exit()

    if args.auto_like:
        print(show())
        bot.autoLike(args.auto_like)
        exit()

    if args.auto_follow:
        print(show())
        bot.autoFollow(args.auto_follow)
        exit()

    if args.configuration:
        try:
            with open(args.configuration, 'r') as config_file:
                config = json.load(config_file)
                if config['mode'] == 'auto-comment':
                    print(show())
                    if config['isSingleComment']:
                        comment = random.choice(config['comment'])
                    else:
                        comment = config['comment'][config['selectedComment'] - 1]
                    
                    if config['isSingleTarget']:
                        target = config['target'][config['selectedTarget']]
                        logger.info(f"Commenting on {target} with '{comment}'...")
                        bot.autoComment(target, comment)
                    else:
                        for target in config['target']:
                            logger.info(f"Commenting on {target} with '{comment}'...")
                            bot.autoComment(target, comment)
                            logger.success(f"Successfully commented on {target} with '{comment}'")
                elif config['mode'] == 'auto-like':
                    print(show())
                    for target in config['target']:
                        logger.info(f"Liking {target}")
                        bot.autoLike(target)
                        logger.success(f"Successfully Liked {target} posts")
                elif config['mode'] == 'auto-follow':
                    print(show())
                    for target in config['target']:
                        logger.info(f"Following {target}")
                        bot.autoFollow(target)
                        logger.success(f"Successfully Following {target} account")

        except FileNotFoundError:
            print(f"Error: Configuration file '{args.configuration}' not found.")
        except Exception as e:
            print(f"Error: Failed to load configuration file: {str(e)}")
