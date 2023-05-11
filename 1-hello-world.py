import requests
from starlette.requests import Request
from typing import Dict
from ray import serve

@serve.deployment
class Hello:
    def __init__(self, msg: str):
        self._msg = msg

    def __call__(self, request: Request) -> Dict:
        return {"result": self._msg}

entrypoint = Hello.bind(msg="Hello world!")