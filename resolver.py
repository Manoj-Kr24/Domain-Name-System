
import socket

class DnsClient:
    def __init__(self, server_host="127.0.0.1", server_port=8080):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(5)  # Set a timeout for the server response

    def send_request(self, command):
       
        try:
            self.client_socket.sendto(command.encode(), (self.server_host, self.server_port))
            response, _ = self.client_socket.recvfrom(1024)
            return response.decode()
        except socket.timeout:
            return "Error: Server response timed out."
        except Exception as e:
            return f"Error: {e}"

def resolve_domain(domain):
    
    if not domain:
        print("Invalid domain. Please enter a valid domain name.")
        return

    client = DnsClient()

    # Send query for IPv4 record
    response_ipv4 = client.send_request(f"QUERY_IPV4 {domain}")
    if "not found" not in response_ipv4:
        print(f"IPv4 Record for {domain}: {response_ipv4.split(': ')[-1]}")
    else:
        print(f"{domain} has no IPv4 record.")

    # Send query for IPv6 record
    response_ipv6 = client.send_request(f"QUERY_IPV6 {domain}")
    if "not found" not in response_ipv6:
        print(f"IPv6 Record for {domain}: {response_ipv6.split(': ')[-1]}")
    else:
        print(f"{domain} has no IPv6 record.")

if __name__ == "__main__":
    while True:
        domain = input("Enter domain name to resolve (or type 'exit' to quit): ").strip()
        if domain.lower() == 'exit':
            print("Exiting resolver...")
            break
        resolve_domain(domain)
