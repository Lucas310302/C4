# C4 Command And Control Tool [SERVER]

---

The C4 Command & Control (C4-CC) is a simple command and control server and client system built on top of asyncio. It allows you to manage multiple clients (zombies) from a central server using a command-line interface (CLI). The clients can execute various commands sent from the server, such as sending files, performing UDP flood attacks, and more.

## Server (`c4_server.py`)
The C4-CC server (`c4_server.py`) acts as a central command hub for managing connected clients (zombies). It provides an interactive CLI menu with various options to control the connected zombies.

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

## Building the client
The C4-CC client (`c4_client.py`) comes as a python script, but I recommend building it with pyinstaller since it will make execution and hiding much easier.

1. **In the terminal, write `pip install pyinstaller`** to install the pyinstaller component.
2. **On Windows systems `pyinstaller --onefile --noconsole c4-worm.py`** to build the executable and make it run with no console windows.
3. **On Unix systems `pyinstaller --onefile c4-worm.py`** to build the executable and make it run with no console windows.

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
2. **`SYNTACK`:** Start a TCP SYN packet attack (SYN flood) on the specified IP and port. Usage: `SYNTACK -a [ip_addr] -p [port]`
3. **`bot_size`:** Print the number of currently connected clients (zombies).
4. **`help`:** Get help on available commands.
5. **`exit`:** Go back to the main server menu.

**Note:** The C4-CC system can be expanded with additional commands and functionalities based on your specific requirements.

## Disclaimer
The C4-CC system is intended for **educational and ethical purposes** only. Unauthorized use of this tool for malicious or illegal activities is strictly prohibited. The developers of this tool are not responsible for any misuse or damage caused by the usage of this software. Use it responsibly and only with explicit permission from the owners of the targeted systems.

---

# C4 Command And Control Tool [CLIENT]

---

The C4-CC client (`c4_client.py`) is designed to run on targeted machines (zombies) and connect to the C4-CC server. However, it is important to note that the client itself cannot execute on a target machine autonomously without explicit user interaction.

### Changing Registry Keys and Cron Jobs
On Windows systems, the client attempts to set itself to run on startup and with elevated administrator privileges by modifying registry keys accordingly. On Unix systems, it adds itself to the user's crontab to run at startup and attempts to run with elevated privileges using `sudo`.

### Disclaimer
The C4-CC client and server tools are for **educational and research purposes only**. The client's capability to modify registry keys and add itself to startup mechanisms is purely for demonstration purposes and should never be used for malicious or unauthorized activities. Unauthorized use of this tool for any harmful actions on target systems is strictly prohibited. The developers of this tool are not responsible for any misuse or damage caused by the usage of this software. Use it responsibly and only with explicit permission from the owners of the targeted systems.

---