import socket
import json   # built-in Python module for working with JSON data

# ── CONFIGURATION ──────────────────────────────────────────
HOST = "httpbin.org"
PORT = 80
PATH = "/post"   # httpbin's /post endpoint accepts POST requests

# ── THE DATA WE WANT TO SEND ────────────────────────────────
# POST requests send data TO the server (unlike GET which just asks for data)
# Common use cases: login forms, submitting search queries, sending data to an API
# We represent our data as a Python dictionary first
data = {
    "name":    "Aishwarya",
    "project": "HTTP Client from Scratch",
    "phase":   3
}

# json.dumps() converts the Python dictionary into a JSON string
# e.g. {"name": "Aishwarya", "project": "HTTP Client from Scratch", "phase": 3}
json_body = json.dumps(data)

# We need to know the exact byte length of the body
# because we have to tell the server in the Content-Length header
body_bytes  = json_body.encode("utf-8")  # convert to bytes
body_length = len(body_bytes)            # count the bytes

# ── BUILD THE POST REQUEST ──────────────────────────────────
# POST is different from GET in two ways:
#   1. Method is POST instead of GET
#   2. We include two extra headers + the actual body after the blank line
#      Content-Type  → tells server the body is JSON (not a form, not plain text)
#      Content-Length → tells server exactly how many bytes to read for the body
#                       without this the server doesn't know when the body ends

request = (
    f"POST {PATH} HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    f"Connection: close\r\n"
    f"Content-Type: application/json\r\n"     # body format = JSON
    f"Content-Length: {body_length}\r\n"      # body size in bytes
    f"\r\n"                                    # blank line = end of headers
    + json_body                                # the actual body comes after
)

# ── REUSABLE PARSER FROM PHASE 2 ───────────────────────────
def parse_response(raw_bytes):
    text = raw_bytes.decode("utf-8", errors="replace")
    header_section, _, body = text.partition("\r\n\r\n")
    header_lines = header_section.split("\r\n")
    status_line  = header_lines[0]
    parts        = status_line.split(" ", 2)
    status_code  = int(parts[1])
    reason       = parts[2]
    headers = {}
    for line in header_lines[1:]:
        if ":" in line:
            name, _, value = line.partition(":")
            headers[name.strip().lower()] = value.strip()
    return {
        "status_code": status_code,
        "reason":      reason,
        "headers":     headers,
        "body":        body
    }

# ── SEND THE POST REQUEST ───────────────────────────────────
print(f"Sending POST to {HOST}{PATH}...")

with socket.create_connection((HOST, PORT), timeout=10) as sock:
    # For POST we encode the whole request + body together as bytes
    sock.sendall(request.encode("utf-8"))
    print("POST request sent!")

    raw_response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        raw_response += chunk

# ── PARSE AND PRINT ─────────────────────────────────────────
response = parse_response(raw_response)

print("\n" + "=" * 50)
print(f"STATUS: {response['status_code']} {response['reason']}")

# httpbin echoes back the JSON we sent inside response["json"]
# We parse the body string back into a Python dictionary so we can
# read specific fields from it
if response["status_code"] == 200:
    response_data = json.loads(response["body"])
    print("\nData we sent (echoed back by httpbin):")
    # response_data["json"] is the body we sent, now parsed
    for key, value in response_data.get("json", {}).items():
        print(f"  {key}: {value}")
else:
    print("Something went wrong:", response["body"][:200])

print("=" * 50)