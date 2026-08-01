from flask import Flask
import psutil
import platform

app = Flask(__name__)

@app.route("/")
def home():

    ram = round(psutil.virtual_memory().percent, 1)

    cpu = round(psutil.cpu_percent(), 1)

    return f"""
    <h1>🤖 CloudAI Dashboard</h1>

    <h2>🟢 Online</h2>

    <p><b>OS:</b> {platform.system()}</p>

    <p><b>CPU:</b> {cpu}%</p>

    <p><b>RAM:</b> {ram}%</p>

    <p><b>AI:</b> Gemini</p>

    <p><b>Version:</b> V5</p>
    """
