# coding: utf-8
import requests
url = ''
data = {"text":"Hello, World! from python request"}
requests.post(url, json=data)
