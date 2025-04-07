import uvicorn
from fastapi import FastAPI, HTTPException
from subprocess import Popen, PIPE
import socket

app = FastAPI()

# Get your machine's actual IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Define the paths for your tool servers
tool_servers = {
    "filesystem": ["uvx", "mcp-server-fs"],
    "git": ["uvx", "mcp-server-git"],
    "memory": ["uvx", "mcp-server-memory"]
}

# Start each tool server as a subprocess
for name, command in tool_servers.items():
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    setattr(app.state, f"{name}_process", process)

@app.get("/fs")
async def filesystem_tool():
    return {"message": "Filesystem Tool Accessed"}

@app.get("/git")
async def git_tool():
    return {"message": "Git Tool Accessed"}

@app.get("/memory")
async def memory_tool():
    return {"message": "Memory Tool Accessed"}

if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"Server will run on: http://{local_ip}:8000")
    uvicorn.run(app, host=local_ip, port=8000)