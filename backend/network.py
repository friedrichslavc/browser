import socket

class NetworkManager:
    def send_request(self, url):
        # 简单实现，仅支持HTTP
        try:
            host = url.split('//')[1].split('/')[0]
            path = '/' + '/'.join(url.split('//')[1].split('/')[1:])
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, 80))
            
            request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
            s.send(request.encode())
            
            response = s.recv(4096).decode()
            s.close()
            
            return response
        except Exception as e:
            return f"Error: {str(e)}"
