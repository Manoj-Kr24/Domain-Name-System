import socket

class DnsClient:
    def __init__(self, server_host="127.0.0.1", server_port=8080):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_request(self, command):
        try:
            self.client_socket.sendto(command.encode(), (self.server_host, self.server_port))
            response, _ = self.client_socket.recvfrom(1024)
            return response.decode()
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    client = DnsClient()

    while True:
        print("\nCommands:")
        print("1. Insert IPv4 Record: INSERT_IPV4 domain ip")
        print("2. Insert IPv6 Record: INSERT_IPV6 domain ip")
        print("3. Query IPv4: QUERY_IPV4 domain")
        print("4. Query IPv6: QUERY_IPV6 domain")
        print("5. Remove IPv4 Record: REMOVE_IPV4 domain [ip]")
        print("6. Remove IPv6 Record: REMOVE_IPV6 domain [ip]")
        print("7. Get All IPv4 Records: GET_ALL_IPV4")
        print("8. Get All IPv6 Records: GET_ALL_IPV6")
        print("9. Query Both IPv4 and IPv6: QUERY_BOTH domain")
        print("10. Exit")
        
        command = input("Enter command: ").strip()
        if command.upper() == "EXIT":
            break
        response = client.send_request(command)
        print(f"Response: {response}")
