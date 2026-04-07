import socket
import ssl    # built-in Python module for encrypted connections
import json

# ── PHASE 4A: HANDLE REDIRECTS ──────────────────────────────
# Sometimes servers don't give you the data directly.
# Instead they reply with status 301 or 302 meaning "go look over there"
# and include a "Location" header with the new URL.
# A real HTTP client must follow these redirects automatically.
# Example: http://httpbin.org/redirect/1 redirects once to /get

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

def send_get(host, path, port=80, use_ssl=False):
    """Send a GET request and return the parsed response."""
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"Accept: */*\r\n"
        f"\r\n"
    )

    with socket.create_connection((host, port), timeout=10) as sock:

        if use_ssl:
            # ── PHASE 4B: HTTPS ────────────────────────────
            # HTTPS is just HTTP with an encrypted layer (TLS) on top.
            # ssl.create_default_context() sets up a secure SSL context
            # It verifies the server's certificate (like checking an ID)
            # wrap_socket() wraps our regular socket in encryption
            # server_hostname is needed so the certificate can be verified
            context = ssl.create_default_context()
            sock    = context.wrap_socket(sock, server_hostname=host)
            print("  SSL handshake complete — connection is encrypted")

        sock.sendall(request.encode("utf-8"))

        raw_response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            raw_response += chunk

    return parse_response(raw_response)

def get_with_redirects(host, path, port=80, use_ssl=False, max_redirects=5):
    """
    Follow redirects automatically up to max_redirects times.
    Each redirect gives us a new Location header to follow.
    We stop when we get a non-redirect status code.
    """
    for attempt in range(max_redirects):
        print(f"  Request {attempt + 1}: GET {host}{path}")
        response = send_get(host, path, port, use_ssl)
        code     = response["status_code"]

        # 301 = Moved Permanently, 302 = Found (temporary redirect)
        # Both mean "go to the Location header instead"
        if code in (301, 302):
            location = response["headers"].get("location", "")
            print(f"  → Redirected ({code}) to: {location}")

            # The Location header can be a full URL like https://example.com/page
            # or just a path like /new-page
            # We need to parse it to extract host and path separately
            if location.startswith("https://"):
                location = location[8:]   # strip "https://"
                use_ssl  = True
                port     = 443
            elif location.startswith("http://"):
                location = location[7:]   # strip "http://"
                use_ssl  = False
                port     = 80

            # Everything before the first / is the host, rest is the path
            if "/" in location:
                host, path = location.split("/", 1)
                path = "/" + path
            else:
                host = location
                path = "/"
        else:
            # Not a redirect — this is the final response
            return response

    # If we've followed max_redirects and still getting redirects, give up
    raise Exception(f"Too many redirects (more than {max_redirects})")

# ── TEST 1: REDIRECT FOLLOWING ──────────────────────────────
# httpbin.org/redirect/2 redirects twice before giving you /get
print("TEST 1 — Following redirects")
print("-" * 40)
response = get_with_redirects("httpbin.org", "/redirect/2")
print(f"Final status: {response['status_code']} {response['reason']}")
print()

# ── TEST 2: HTTPS ───────────────────────────────────────────
# Same request but over HTTPS (port 443, encrypted)
print("TEST 2 — HTTPS request")
print("-" * 40)
response = send_get("httpbin.org", "/get", port=443, use_ssl=True)
print(f"Status: {response['status_code']} {response['reason']}")

# Parse and show the URL httpbin reports we connected to
data = json.loads(response["body"])
print(f"Connected URL: {data.get('url', 'unknown')}")
print()

# ── TEST 3: ERROR HANDLING ──────────────────────────────────
# A good HTTP client handles error codes gracefully
print("TEST 3 — Error handling")
print("-" * 40)
response = send_get("httpbin.org", "/status/404")
code = response["status_code"]

# Handle different error families
if code == 200:
    print("Success!")
elif code == 404:
    print("ERROR 404 — The page you requested doesn't exist")
elif code == 403:
    print("ERROR 403 — You don't have permission to access this")
elif code == 500:
    print("ERROR 500 — The server had an internal error")
elif 400 <= code < 500:
    print(f"ERROR {code} — Problem with our request")
elif 500 <= code < 600:
    print(f"ERROR {code} — Problem on the server side")
else:
    print(f"Got status: {code}")