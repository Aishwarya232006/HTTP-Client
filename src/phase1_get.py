import socket
HOST = "httpbin.org" 
#host is the website that we are connecting to
PORT = 80 #it is the universal port for http.Basically every computer knows http lives on port 80
PATH = "/get" #the path is the specific page we want to access on the website. In this case, we want to access the /get page on httpbin.org

#HTTP request is a string that follows a specific format. It consists of a method (in this case, GET), the path, and the HTTP version (HTTP/1.1). The request also includes headers, which provide additional information about the request. In this case, we are including the Host header, which tells the server which website we are trying to access, and the Connection header, which tells the server to close the connection after the response is sent. Finally, we include a blank line to indicate the end of the headers.
request = (
    f"GET {PATH} HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    f"Connection: close\r\n"
    f"\r\n"
)
# Create a socket and connect to the server
print(f"Connecting to {HOST}:{PORT}...")
with socket.create_connection((HOST, PORT),timeout=10) as sock:
    print("Request sent!")

#Recieve the response from the server
raw_response = b""  #
while True:
    chunk = sock.recv(4096)
    if not chunk:
        break
    raw_response += chunk
# Parse and print the response
response_text = raw_respponse.decode("utf-8")
header_section, _, body = response_text.partition("\r\n\r\n" \")
                            