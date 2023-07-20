# C4 Command & Control (C4-CC) Server and Clients

## Overview
C4 Command & Control (C4-CC) is a **simple command and control server and client system** built on top of asyncio. It allows you to manage multiple clients (zombies) from a central server using a **command-line interface (CLI)**. The clients can execute various commands sent from the server, such as sending files, performing UDP flood attacks, and more.

## Server (`c4_server.py`)
The C4-CC server (`c4_server.py`) acts as a central command hub for managing connected clients (zombies). It provides an **interactive CLI menu** with various options to control the connected zombies.

### Dependencies
- Python 3.7 or higher
- `aioconsole`: For asynchronous console input/output
- `c4_server_commands`: A custom module containing utility functions for handling commands

### Usage
1. **Start the server** by running `c4_server.py`.
2. The server will bind to `HOST` and `PORT`, and the C4-CC CLI menu will be displayed.
3. From the CLI menu, you can choose options to interact with connected clients:
   - **[1] Terminal:** Access the command-line interface of the connected clients.
   - **[2] Overview:** View the list of currently connected clients.
   - **[3] Exit:** Terminate the server and close all client connections.

## Client (`c4_client.py`)
The C4-CC client (`c4_client.py`) runs on the targeted machines (zombies) and connects to the C4-CC server. It waits for commands from the server and executes them accordingly.

### Dependencies
- Python 3.7 or higher
- `asyncio`: For asynchronous communication with the server

### Usage
1. **Modify the `HOST` and `PORT` variables** in `c4_client.py` to match the IP address and port of your C4-CC server.
2. **Start the client script `c4_client.py`** on the targeted machine(s).
3. The client will automatically attempt to connect to the C4-CC server and wait for commands.

## Custom Commands
The C4-CC system comes with several built-in commands that can be executed on connected clients. The server sends commands to clients, and the clients execute the corresponding actions. Here are some available commands:

1. **`send`:** Send files to connected clients. Usage: `send -f [filepath] -n [filename] -e [file_extension]`
2. **`SYNTACK`:** Start a TCP SYN packet attack (SYN flood) on specified IP and port. Usage: `SYNTACK -a [ip_addr] -p [port]`
3. **`bot_size`:** Print the number of currently connected clients (zombies).
4. **`help`:** Get help on available commands.
5. **`exit`:** Go back to the main server menu.

**Note:** The C4-CC system can be expanded with additional commands and functionalities based on your specific requirements.

## License
This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it as per the terms of the MIT License. See `LICENSE` file for more details.

## Disclaimer
The C4-CC system is intended for **educational and ethical purposes** only. Unauthorized use of this tool for malicious or illegal activities is strictly prohibited. The developers of this tool are not responsible for any misuse or damage caused by the usage of this software. Use it responsibly and only with explicit permission from the owners of the targeted systems.