import requests

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload={
  'scope': 'GIGACHAT_API_PERS'
}
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': 'c76fea73-bd66-46a6-8263-2a9ea1cc33bf',
  'Authorization': 'Basic MDFhMDE0MzMtZjFkOS03MTRmLWE5ZTMtOGIxNGUxNTRjYTY1OjcwNTliMzRiLWJlMDYtNGZlNS1hMTNmLTZjYTE2ZDU1ZDEyMg=='
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)
