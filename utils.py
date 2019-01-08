import requests_utils
import json


# utils for the requests
def get_request(address):
    """return the content of a selected request in a json format"""
    request = requests_utils.get(address)
    content = request.content.decode('utf-8')
    ordered_content = json.loads(content)
    return ordered_content
