#/home/student/nssa221_scripts python3

"""
Name: Noah Cosamano
Date: February 28th, 2026
"""

import subprocess   # used to run Linux commands from Python
import platform     # used to get OS and kernel info
import time         # used to print current date and time

# This dictionary converts CIDR numbers (like /24) to subnet masks
cidr_conversion = {
    "16": "255.255.0.0",
    "17": "255.255.128.0",
    "18": "255.255.192.0",
    "19": "255.255.224.0",
    "20": "255.255.240.0",
    "21": "255.255.248.0",
    "22": "255.255.252.0",
    "23": "255.255.254.0",
    "24": "255.255.255.0"
}

# Gets the name of the operating system (Linux, Windows, etc.)
os = platform.system()

def get_ip_and_netmask():
    # Runs "ip a" to get IP address info
    ip_a = subprocess.run(
        ["ip","a"], 
        capture_output=True, text=True
    )

    tokens = ip_a.stdout.split()

    # Loops through output to find the IP address
    for index, token in enumerate(tokens):
        if token == "inet":
            ip = tokens[index+1].split("/")[0]
            cidr = tokens[index+1].split("/")[1]
            netmask = cidr_conversion.get(cidr)

            # Skips the localhost address
            if ip == "127.0.0.1":
                continue

    return ip, netmask

def get_gateway():
    # Runs command to get default gateway
    result = subprocess.run(
        ["ip","route", "show", "default"], 
        capture_output=True, text=True
    )

    # The gateway IP is the third word in the output
    gateway = result.stdout.split()[2]

    return gateway

def get_dns():
    # Reads DNS info from resolv.conf file
    result = subprocess.run(
        ["cat", "/etc/resolv.conf"],
        capture_output=True, text=True
    )

    tokens = result.stdout.split()
    dns_addresses = []

    # Looks for lines that say "nameserver"
    for index, token in enumerate(tokens):
        if token == "nameserver":
            dns_addresses.append(tokens[index+1])

    return dns_addresses

def get_hostname_and_domain():
    # Gets the full hostname
    result = subprocess.run(
        ["hostname"], 
        capture_output=True, text=True
    )

    # Splits hostname into name and domain
    tokens = result.stdout.split(".")

    hostname = tokens[0]
    domain = tokens[1].strip()

    return hostname, domain

def get_os_and_kernel():
    # Gets kernel info using platform module
    kernel = f"{platform.system()} {platform.release()}"

    # Gets OS name from os-release file
    result = subprocess.run(
        ["grep", "PRETTY_NAME", "/etc/os-release"],
        capture_output=True, text=True
    )

    operating_system = result.stdout.split("=")[1].strip('"').strip()
    os_version = operating_system.split()[2]

    return operating_system, os_version, kernel

def get_storage_information():
    # Runs df -h to get disk usage in human readable format
    result = subprocess.run(
        ["df","-h"], capture_output=True, text=True
    )

    tokens = result.stdout.split()

    # Finds the row for the root directory "/"
    for index, token in enumerate(tokens):
        if token == "/":
            total = tokens[index-4]
            used = tokens[index-3]
            free = tokens[index-2]

    return total, free, used

def get_cpu_information():
    # Reads CPU info file
    result = subprocess.run(
        ["cat", "/proc/cpuinfo"], capture_output=True, text=True
    )

    processors = 0
    cores = set()  # using a set so we don't count duplicate cores
    current_core_id = None

    tokens = result.stdout.splitlines()

    # Goes through each line to find CPU info
    for token in tokens:
        if token.startswith("processor"):
            processors += 1
        elif token.startswith("core id"):
            current_core_id = token.split(":")[1].strip()
            cores.add(current_core_id)
        elif token[:10] == "model name":
            model = token[10:].strip().strip(":")

    return model, processors, len(cores)

def get_memory_information():
    # Runs free -h to get RAM info
    result = subprocess.run(
        ["free", "-h"], capture_output=True, text=True
    )

    tokens = result.stdout.splitlines()

    # Looks for the line that starts with "Mem:"
    for token in tokens:
        if token.startswith("Mem:"):
            parts = token.split()
            total = parts[1]
            available = parts[6]

    return total, available

# Helper function to print data nicely aligned
def print_row(label, value):
    print(f"{label:<25} {value}")

def create_display():
    # Calls all the functions to collect system info
    hostname, domain = get_hostname_and_domain()
    ip, netmask = get_ip_and_netmask()
    gateway = get_gateway()
    dns_addresses = get_dns()
    os, os_version, kernel = get_os_and_kernel()
    total, free, used = get_storage_information()
    model, processors, cores = get_cpu_information()
    ram_total, ram_free = get_memory_information()

    # Build output as one big string
    output = ""
    output += f"{time.ctime()}\n\n"

    output += "Device Information\n"
    output += f"Hostname: {hostname}\n"
    output += f"Domain: {domain}\n\n"

    output += "Network Information\n"
    output += f"IP Address: {ip}\n"
    output += f"Gateway: {gateway}\n"
    output += f"Network Mask: {netmask}\n"

    for index, dns in enumerate(dns_addresses):
        output += f"DNS{index+1}: {dns}\n"

    output += "\nOperating System Information\n"
    output += f"Operating System: {os}\n"
    output += f"OS Version: {os_version}\n"
    output += f"Kernel Version: {kernel}\n\n"

    output += "Storage Information\n"
    output += f"System Drive Total: {total}\n"
    output += f"System Drive Used: {used}\n"
    output += f"System Drive Free: {free}\n\n"

    output += "Processor Information\n"
    output += f"CPU Model: {model}\n"
    output += f"Number of Processors: {processors}\n"
    output += f"Number of Cores: {cores}\n\n"

    output += "Memory Information\n"
    output += f"Total RAM: {ram_total}\n"
    output += f"Available RAM: {ram_free}\n"

    # Print to screen
    print(output)

    # Save to log file in home directory (append mode)
    with open("/home/student/system_report.log", "a") as logfile:
        logfile.write(output)
        logfile.write("\n" + "-"*50 + "\n\n")

def main():
    # Clears the terminal screen before printing info
    subprocess.run([ "clear"])
    create_display()
    

# Runs main only if this file is executed directly
if __name__ == "__main__":
    main()