import socket
import ssl
from urllib.parse import urlparse


class HTTPClient:
    def __init__(self):
        pass

    def make_request(self, url, redirects=5):
        parsed = urlparse(url)
        host = parsed.hostname
        port = 443 if parsed.scheme == 'https' else 80
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query

        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: go2web/1.0\r\nAccept: text/html,application/json\r\nConnection: close\r\n\r\n"

        with socket.create_connection((host, port)) as sock:
            if parsed.scheme == 'https':
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
            sock.sendall(request.encode())
            response = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk

        header_data, _, body = response.partition(b"\r\n\r\n")
        headers = header_data.decode(errors='ignore')
        status = int(headers.split()[1])

        if status in (301, 302, 303, 307, 308) and redirects > 0:
            for line in headers.splitlines():
                if line.lower().startswith("location:"):
                    new_url = line.split(":", 1)[1].strip()
                    if not new_url.startswith("http"):
                        new_url = f"{parsed.scheme}://{host}{new_url}"
                    return self.make_request(new_url, redirects - 1)
        return headers, body.decode(errors='ignore')