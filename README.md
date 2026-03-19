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

