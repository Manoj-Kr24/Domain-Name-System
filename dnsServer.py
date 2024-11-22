
import socket
from collections import deque

class DnsNode:
    def __init__(self):
        self.records = []  # List of IPs associated with this node
        self.children = {}  # Children nodes for subdomains

class DnsTree:
    def __init__(self):
        self.root = DnsNode()  # Root of the DNS tree

    def insert_record(self, domain, ip):

        parts = domain.split(".")[::-1]
        current = self.root
        for part in parts:
            if part not in current.children:
                current.children[part] = DnsNode()
            current = current.children[part]
        current.records.append(ip)
        return f"Inserted: {domain} -> {ip}"

    def query_domain(self, domain):
        
        parts = domain.split(".")[::-1]
        current = self.root
        for part in parts:
            if part in current.children:
                current = current.children[part]
            else:
                return None  # Return None if the domain is not found
        return current.records if current.records else None


    def remove_record(self, domain, ip=None):
        """Remove a domain record (either all or specific IP)."""
        parts = domain.split(".")[::-1]

        current = self.root
        for part in parts:
            if part in current.children:
                current = current.children[part]
            else:
                return f"Domain {domain} not found."
        
        # If no specific IP is provided, remove all records
        if ip is None:
            current.records.clear()
            return f"Removed all records for {domain}"
        
        # If an IP is provided, remove that specific record
        if ip in current.records:
            current.records.remove(ip)
            return f"Removed {ip} from {domain}"
        else:
            return f"IP {ip} not found for domain {domain}"

    def get_all_records(self):
        """Get all records from the tree."""
        return self._get_all_records_from_node(self.root)

    def _get_all_records_from_node(self, node, domain_parts=None):
        """Recursively get all records from a node and its descendants."""
        domain_parts = domain_parts or []
        records = []
        
        # If the node has records, add them to the result
        if node.records:
            records.append(f"{'.'.join(domain_parts[::-1])}: {', '.join(node.records)}")

        # Recursively traverse child nodes
        for part, child in node.children.items():
            records.extend(self._get_all_records_from_node(child, domain_parts + [part]))
        
        return records

    def load_domains_from_file(self, filename):
        
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                try:
                    domain_name, ip_address = line.split()
                    self.insert_record(domain_name, ip_address)
                except ValueError:
                    print(f"Skipping invalid line in {filename}: {line}")

class DnsCache:
    def __init__(self, size=5):
        """Initialize cache with the given size."""
        self.cache = {}
        self.order = deque()  # Queue to maintain FIFO order
        self.size = size

    def get(self, domain):
        
        if domain in self.cache:
            return self.cache[domain]
        return None

    def put(self, domain, records):
        
        if len(self.cache) >= self.size:
            # Remove the oldest entry (FIFO)
            oldest = self.order.popleft()
            del self.cache[oldest]
        
        self.cache[domain] = records
        self.order.append(domain)

    def remove(self, domain):
        # Remove a record from the cache.
        if domain in self.cache:
            del self.cache[domain]
            self.order.remove(domain)

class DnsServer:
    def __init__(self, host="127.0.0.1", port=8080, ipv4_file="domains_databaseIPV4.txt", ipv6_file="domains_databaseIPV6.txt"):
        self.tree_ipv4 = DnsTree()  # Tree for IPv4
        self.tree_ipv6 = DnsTree()  # Tree for IPv6
        self.cache_ipv4 = DnsCache()  # Cache for IPv4 records
        self.cache_ipv6 = DnsCache()  # Cache for IPv6 records
        self.host = host
        self.port = port
        self.ipv4_file = ipv4_file
        self.ipv6_file = ipv6_file
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Load domain data during initialization
        print(f"Loading domains from {ipv4_file} for IPv4...")
        self.tree_ipv4.load_domains_from_file(self.ipv4_file)
        print(f"Loading domains from {ipv6_file} for IPv6...")
        self.tree_ipv6.load_domains_from_file(self.ipv6_file)
        print("Domain data loaded successfully.")

    def start_server(self):
        
        self.server_socket.bind((self.host, self.port))
        print(f"DNS Server started on {self.host}:{self.port}")

        while True:
            data, addr = self.server_socket.recvfrom(1024)
            request = data.decode().strip()
            print(f"Received request from {addr}: {request}")

            response = self.process_request(request)
            # print(response)
            self.server_socket.sendto(response.encode(), addr)

    def process_request(self, request):
        # Process the incoming request based on command type.
        command, *args = request.split(" ", 1)
        command = command.upper()

        if command == "QUERY_IPV4":
            return self.query_tree(self.tree_ipv4, self.cache_ipv4, args[0], 'A')
        elif command == "QUERY_IPV6":
            return self.query_tree(self.tree_ipv6, self.cache_ipv6, args[0], 'AAAA')
        elif command == "QUERY_BOTH":
            domain = args[0]
            ipv4_records = self.query_tree(self.tree_ipv4, self.cache_ipv4, domain, 'A')
            ipv6_records = self.query_tree(self.tree_ipv6, self.cache_ipv6, domain, 'AAAA')
            response = self.combine_records(domain, ipv4_records, ipv6_records)
            return response
        elif command == "INSERT_IPV4":
            domain, ip = args[0].split()
            return self.insert_record(self.tree_ipv4, domain, ip)
        elif command == "INSERT_IPV6":
            domain, ip = args[0].split()
            return self.insert_record(self.tree_ipv6, domain, ip)
        elif command == "REMOVE_IPV4":
            domain, *ip = args[0].split()
            ip = ip[0] if ip else None
            return self.remove_record(self.tree_ipv4, self.cache_ipv4, domain, ip)
        elif command == "REMOVE_IPV6":
            domain, *ip = args[0].split()
            ip = ip[0] if ip else None
            return self.remove_record(self.tree_ipv6, self.cache_ipv6, domain, ip)
        elif command == "GET_ALL_IPV4":
            return self.get_all_records(self.tree_ipv4)
        elif command == "GET_ALL_IPV6":
            return self.get_all_records(self.tree_ipv6)
        else:
            return "Invalid command."

    def query_tree(self, tree, cache, domain, record_type):
        
        # Check if domain is already in the cache
        cached_records = cache.get(domain)
        if cached_records:
            print(f"Cache Hit for {domain}: {', '.join(cached_records)}")  
            return f"Cache Hit: Records for {domain}: {', '.join(cached_records)}"

        # Query the tree if not found in cache
        records = tree.query_domain(domain)
        if records:
            cache.put(domain, records)  # Store records in cache
            print(f"Cache Miss for {domain}: {', '.join(records)}")  
            return f"Records for {domain}: {', '.join(records)}"
        
        return f"Domain {domain} not found."

    def combine_records(self, domain, ipv4_records, ipv6_records):

        
        
        response = f"Domain: {domain}\n"
        if ipv4_records:
            response += f"IPv4: {''.join(ipv4_records.split(': ')[-1])}\n"
        else:
            response += "IPv4: None\n"
        if ipv6_records:
            response += f"IPv6: {''.join(ipv6_records.split(': ')[-1])}\n"
        else:
            response += "IPv6: None\n"
        return response

    def insert_record(self, tree, domain, ip):
        
        return tree.insert_record(domain, ip)

    def remove_record(self, tree, cache, domain, ip):
        
        cache.remove(domain)
        return tree.remove_record(domain, ip)

    def get_all_records(self, tree):
        
        records = tree.get_all_records()
        return "\n".join(records) if records else "No records found."



if __name__ == "__main__":
    # Set up the server host and port
    host = "127.0.0.1"  
    port = 8080
    
    
    ipv4_file = "domains_databaseIPV4.txt"
    ipv6_file = "domains_databaseIPV6.txt"
    
    # Create and start the DNS server
    dns_server = DnsServer(host=host, port=port, ipv4_file=ipv4_file, ipv6_file=ipv6_file)
    dns_server.start_server()
