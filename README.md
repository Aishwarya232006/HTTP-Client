# HTTP-Client
Raw HTTP/1.1 client built from scratch using Python sockets- no libraries
## Why I built this 
To understand how HTTP work at the transport layer - directly relevant for cloud infrastructure, REST API integration, and data pipeline debugging.

## Phases - What it covers?
1. Raw TCP socket + manual GET request 
2. Response parsing (status line , headers , body)
3. POST requests with JSON body 
4. Redirect following + error handling 
5. Also HTTPS via Python's ssl module 

## Run it 
''' bash
python src/phase1_get.py
'''

## Concepts
TCP sockets ' DNS resolution , HTTP/1.1 , header parsing , SSL/TLS

Phase 1: Basic GET Request
You manually asked a server for data using raw HTTP. This is the most basic way to talk to any website.

Phase 2: Response Parser
You wrote code that understands the server's response. The server doesn't just send "OK" - it sends a whole package with status codes (200=success, 404=not found), headers (what type of data), and the actual body (the webpage).

Phase 3: POST Request
Instead of just getting data (like loading a page), you SENT data to the server. This is how login forms, search boxes, and file uploads work.

Phase 4: HTTPS + Redirects
HTTPS: Encrypts everything so no one can spy on what you're doing

Redirects: When you go to a short link like bit.ly/xyz, it automatically sends you to the real page

The Browser Output You Saw:
text
127.0.0.1 - - [07/Apr/2026...] "GET /run/1 HTTP/1.1" 200 -
This is Flask (the web server you ran) logging that someone requested to run your Phase 1 code. The 200 means "success".

What you actually accomplished:
You built a mini browser engine that can:

Connect to any website

Send requests (GET to receive, POST to send)

Understand server responses

Handle encryption (HTTPS)

Follow redirects automatically

The Big Picture:
text
Normal User: Types URL → Chrome does magic → Sees page

You: Types URL → YOUR CODE opens socket, sends HTTP, parses response → Sees page

No magic. You built the magic.