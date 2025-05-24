import requests

BASE_URL = "http://localhost:8080/"

def make_request(method, page, user=None, body={}):
    user = str(user)
    
    req = None

    match method.lower():
        case "get":
            return requests.get(BASE_URL + page, headers={"Authorization": user}, json=body)
        case "post":
            return requests.post(BASE_URL + page, headers={"Authorization": user}, json=body)
        case "put":
            return requests.put(BASE_URL + page, headers={"Authorization": user}, json=body)
        case "delete":
            return requests.delete(BASE_URL + page, headers={"Authorization": user}, json=body)

def get_data(req):
    if req.ok:
        try:
            return (True, req.json())
        except:
            return (True, req.text)
    else:
        return (False, str(req.status_code) + " " + req.reason)

rq = lambda method, page, user=None, body={}: get_data(make_request(method, page, user, body))