from celery import Celery
from xmlrpc.client import ServerProxy

server = ServerProxy('http://localhost:9001/RPC2')
app = Celery('tasks', broker='redis://localhost')

print(server.supervisor.getState())

@app.task
def start_restream(name):
    print(name)

@app.task
def stop_restream(name):
    print(name)
