import logging
import os
from flask import Flask
from threading import Thread

app = Flask('')

log = logging.getLogger("werkzeug")
log.disabled = True

@app.route('/')
def main():
  return "Your bot is alive!"

def run():
    os.environ["WERKZEUG_RUN_MAIN"] = "true"
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()