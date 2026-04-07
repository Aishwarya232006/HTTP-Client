import socket

# ── CONFIGURATION ──────────────────────────────────────────
HOST = "httpbin.org"
PORT = 80
PATH = "/get"

# ── BUILD REQUEST ───────────────────────────────────────────
request = (
    f"GET {PATH} HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    f"Connection: close\r\n"
    f"Accept: */*\r\n"
    f"\r\n"
)

# ── SEND REQUEST ────────────────────────────────────────────
print(f"Connecting to {HOST}:{PORT}...")

with socket.create_connection((HOST, PORT), timeout=10) as sock:
    sock.sendall(request.encode("utf-8"))
    print("Request sent!")

    raw_response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        raw_response += chunk

# ── PHASE 2: PROPER RESPONSE PARSER ────────────────────────
# We now wrap the parsing logic into a reusable function.
# This is the same logic as Phase 1 but structured cleanly
# so we can call it from any phase going forward.

def parse_response(raw_bytes):
    # Step 1: convert bytes to string
    text = raw_bytes.decode("utf-8", errors="replace")

    # Step 2: split at the blank line separating headers from body
    header_section, _, body = text.partition("\r\n\r\n")

    # Step 3: pull out the status line (always the very first line)
    header_lines = header_section.split("\r\n")
    status_line  = header_lines[0]

    # Step 4: parse the status line into its three parts
    # format is always: "HTTP/1.1 200 OK"
    parts       = status_line.split(" ", 2)  # split into max 3 pieces
    version     = parts[0]                   # "HTTP/1.1"
    status_code = int(parts[1])             # 200  (as an integer so we can compare)
    reason      = parts[2]                  # "OK"

    # Step 5: parse headers into a dictionary
    headers = {}
    for line in header_lines[1:]:
        if ":" in line:
            name, _, value = line.partition(":")
            headers[name.strip().lower()] = value.strip()
            # .lower() so we can always do headers["content-type"]
            # regardless of how the server capitalised it

    # Step 6: return everything as a structured dictionary
    return {
        "status_code": status_code,  # e.g. 200
        "reason":      reason,        # e.g. "OK"
        "headers":     headers,       # e.g. {"content-type": "application/json"}
        "body":        body           # the raw response body as a string
    }

# ── USE THE PARSER ──────────────────────────────────────────
response = parse_response(raw_response)

print("\n" + "=" * 50)
print(f"STATUS CODE : {response['status_code']}")
print(f"REASON      : {response['reason']}")

# Now we can check the status code as a number
# which lets us handle errors properly
if response["status_code"] == 200:
    print("SUCCESS — server returned 200 OK")
elif response["status_code"] == 404:
    print("ERROR — page not found (404)")
elif response["status_code"] >= 500:
    print("ERROR — server had a problem (5xx)")
else:
    print(f"Got status: {response['status_code']}")

print("\nHEADERS:")
for name, value in response["headers"].items():
    print(f"  {name}: {value}")

# content-type tells us what format the body is in
content_type = response["headers"].get("content-type", "unknown")
print(f"\nContent type is: {content_type}")

print("\nBODY:")
print(response["body"][:500])
print("=" * 50)