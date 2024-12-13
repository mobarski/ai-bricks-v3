from .client import Client
from .config import load_config
from .connection import connect

def client(model=None, **kwargs):
    return Client(connect, model, **kwargs)
