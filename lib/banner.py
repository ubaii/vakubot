import random, os
banner = """
 _____ _____ _____ _____ _____ _____ _____ 
|  |  |  _  |  |  |  |  | __  |     |_   _|
|  |  |     |    -|  |  | __ -|  |  | | |  
 \___/|__|__|__|__|_____|_____|_____| |_|  
    Developed by Zyon || Version: 1.0
"""

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def getRandomVersion():
    return random.randint(1, 2)

def show():
    clearConsole()
    return banner