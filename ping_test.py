"""
This program allows the user to test local, remote, and DNS connectivity dynamically
through the command line.

Author: Noah Cosamano
Date: February 6, 2026
"""

import subprocess
import platform # to get operating system

os: str = platform.system()

def show_menu() -> None: # Prompts the user for options on startup
    print("\nPlease select an option below\n"
          "1. Display the default gateway\n"
          "2. Test local connectivity\n"
          "3. Test remote connectivity\n"
          "4. Test DNS resolution\n"
          "5. Exit/quit the program")
    
def get_instruction() -> None:
    """
    This function takes user input and calls the corresponding function depending
    on what the user inputs.
    """
    while True:
        show_menu() # displays command menu
        try:
            user_input: int = int(input(">> ").strip())
            if user_input not in range(1,6):
                print(" Error: Invalid instruction")
            elif user_input == 1:
                gateway: str = get_gateway()
                print(f"\nDefault gateway: {gateway}")
            elif user_input == 2:
                test_local()
            elif user_input == 3:
                test_remote()
            elif user_input == 4:
                test_dns()
            elif user_input == 5:
                break # exits out of input loop when user wants to exit
                
        except (ValueError, UnboundLocalError):
            print(" Error: Invalid instruction") # For when user enters an input
            # such as 'a' or '7'
            
    print("\nExiting... ")

def clear_terminal():
    subprocess.run("cls" if os == "Windows" else "clear")
        
def get_gateway() -> str:
    """
    This function returns the default gateway of the device.
    Dependning on the operating system, it will change the argument vector
    to suit the operating systems command line.

    Raises:
        OSError: for incorrect operating system.

    Returns:
        str: This is the default gateway
    """
    if os == "Windows":
        response = subprocess.run(["ipconfig"], capture_output=True, text=True)
        for line in response.stdout.splitlines():
            if "Default Gateway" in line:
                gateway = line.split(":")[-1].strip()
        
    elif os == "Darwin":
        response = subprocess.run(["route", "-n", "get", "default"], 
                                  capture_output=True, text=True) 
        for line in response.stdout.splitlines():
            if line.strip().startswith("gateway:"):
                gateway: str = line.strip("gateway: ") # keeps just the gateway
                 
    elif os == "Linux":
        response = subprocess.run(["ip", "r"], capture_output=True, text=True)
        gateway: str = response.stdout.split()[2] # gets just the gateway token
        
    else:
        raise OSError(" Error: Unsupported operating system")
        
    return gateway
    
def test_local() -> None:
    """
    This function tests a ping on the local machines default gateway.
    Depending on the OS, it will change argument vector to match the 
    operating systems command line

    Raises:
        OSError: for unsupported operating system.
    """
    gateway: str = get_gateway()
    
    print(f"\nTesting gateway '{gateway}'...")
    
    if os == "Windows":
        response = subprocess.run(["ping", gateway], 
                                  capture_output=True, text=True)
    elif os in ("Darwin", "Linux"):
        response = subprocess.run(["ping", "-c", "4", gateway],
                                  capture_output=True, text=True)
    else:
        raise OSError(" Error: Unsupported operating system")
        
    print(response.stdout)
    
def test_remote():
    """
    This function tests the connection to RIT's DNS server. Argument vectors
    are customized to fit the operating systems command line.
    
    Raises:
        OSError: for unsupported operating system.
    """
    if os == "Windows":
        response = subprocess.run(["ping", "129.21.3.17"], 
                                  capture_output=True, text=True)
    elif os in ("Darwin", "Linux"):
        response = subprocess.run(["ping", "-c", "4", "129.21.3.17"],
                                  capture_output=True, text=True)
    else:
        raise OSError(" Error: Unsupported operating system")
        
    print(response.stdout)
    
def test_dns():
    """
    This function tests connection to Google's DNS server. This also 
    has custom argument vectors to fit operating systems command line.

    Raises:
        OSError: for unsupported operating system.
    """
    print(f"\nTesting google.com DNS...")
    if os == "Windows":
        response = subprocess.run(["ping", "8.8.8.8"], 
                                  capture_output=True, text=True)
    elif os in ("Darwin", "Linux"):
        response = subprocess.run(["ping", "-c", "4", "8.8.8.8"],
                                  capture_output=True, text=True)
    else:
        raise OSError(" Error: Unsupported operating system")
        
    print(response.stdout)

def main():
    clear_terminal()
    get_instruction() # begins input loop
    
if __name__ == "__main__":
    main()