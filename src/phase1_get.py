import socket

# ── CONFIGURATION ──────────────────────────────────────────
HOST = "httpbin.org"  # the website we are connecting to
PORT = 80             # port 80 = universal door for plain HTTP
PATH = "/get"         # the specific page we want on that server

# ── BUILD THE HTTP REQUEST ──────────────────────────────────
# An HTTP request is just a carefully formatted string.
# Every line ends with \r\n (carriage return + newline).
# The blank line at the end (\r\n alone) tells the server
# "headers are done" — without it the server waits forever.
request = (
    f"GET {PATH} HTTP/1.1\r\n"  # method + path + version
    f"Host: {HOST}\r\n"          # required: tells server which site we want
    f"Connection: close\r\n"     # ask server to close after replying
    f"Accept: */*\r\n"           # we'll accept any type of response
    f"\r\n"                      # blank line = end of headers
)

# ── OPEN TCP CONNECTION AND SEND ────────────────────────────
# socket.create_connection() does three things automatically:
#   1. DNS lookup  →  "httpbin.org" becomes an IP address
#   2. TCP handshake  →  SYN / SYN-ACK / ACK
#   3. Returns a connected socket object we can read/write
# timeout=10 means: give up if server doesn't respond in 10 seconds
# The "with" block closes the socket automatically when we're done

print(f"Connecting to {HOST}:{PORT}...")

with socket.create_connection((HOST, PORT), timeout=10) as sock:

    # encode() converts our string into bytes — sockets only speak bytes
    # sendall() makes sure every single byte is sent, even over slow connections
    sock.sendall(request.encode("utf-8"))
    print("Request sent!")

    # ── RECEIVE THE RESPONSE ────────────────────────────────
    # The response arrives as a stream of bytes, possibly in many chunks.
    # b"" is an empty bytes object (the b prefix means bytes, not a string)
    # We keep reading 4096 bytes at a time until the server closes the connection
    # An empty chunk means the server is done sending — that's our stop signal

    raw_response = b""
    while True:
        chunk = sock.recv(4096)  # read up to 4096 bytes at a time
        if not chunk:            # empty chunk = server closed connection
            break
        raw_response += chunk    # glue each chunk onto what we have so far

# ── PARSE THE RESPONSE ──────────────────────────────────────
# decode() converts bytes back into a readable string (reverse of encode)
response_text = raw_response.decode("utf-8")

# The response has two parts separated by a blank line (\r\n\r\n):
#   BEFORE the blank line = headers
#   AFTER  the blank line = body (the actual data)
# partition() splits at the first match and returns 3 parts:
#   (before, separator, after) — we ignore the separator with _
header_section, _, body = response_text.partition("\r\n\r\n")

# Split headers into individual lines
header_lines = header_section.split("\r\n")

# The very first line is always the status: e.g. "HTTP/1.1 200 OK"
status_line = header_lines[0]

# All remaining lines are headers in "Name: Value" format
# We store them in a dictionary so they're easy to look up
headers = {}
for line in header_lines[1:]:
    if ":" in line:
        name, _, value = line.partition(":")
        headers[name.strip()] = value.strip()

# ── PRINT RESULTS ───────────────────────────────────────────
print("\n" + "=" * 50)
print("STATUS:", status_line)
print("\nHEADERS:")
for name, value in headers.items():
    print(f"  {name}: {value}")
print("\nBODY:")
print(body[:500])   # only print first 500 chars so terminal doesn't flood
print("=" * 50)