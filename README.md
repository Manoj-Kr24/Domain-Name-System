# **DNS Resolver and Manager**

A Python-based DNS resolver and manager project that simulates a DNS server. This project provides functionality for querying domain names (IPv4 and IPv6 records), adding/removing DNS records, and resolving domain names efficiently.

---

## **Features**


  - Resolve domain names to their corresponding IPv4 and IPv6 addresses.
  - Handle both valid and invalid queries gracefully.


  - Add new domain records to the DNS tree.
  - Remove existing domain records.


  - IPv4 and IPv6 address resolution.


---



## **How to Use**

### **1. Setting up the Project**
1. Clone the repository:
   ```bash
   git clone https://github.com/Manoj-Kr24/Domain-Name-System.git
   cd Domain-Name-System
   ```

2. Ensure Python is installed on your system (Python 3.6+ recommended).

### **2. Running the Server**
Start the DNS server to begin handling queries:
```bash
python dnsServer.py
```

### **3. Using the DNS Client**
Run the client to query domain records:
```bash
python resolver.py
```


### **4. Managing DNS Records**
Run the DNS manager to add or remove records:
```bash
python dnsManager.py
```


---



## **Technologies Used**

- **Python**:
  - `socket` for networking (client-server communication).
  - Core programming for DNS tree implementation.

- **Git**:
  - Version control system to manage project files.

---

## **How It Works**

1. **DNS Server**:
   - Maintains a DNS tree that maps domain names to their respective IP addresses.
   - Listens for client requests, processes queries, and returns results.

2. **DNS Client**:
   - Sends domain queries to the server.
   - Displays resolved IPv4/IPv6 addresses or error messages.

3. **DNS Manager**:
   - Updates the DNS tree by adding or removing domain records.

---

## **To-Do and Future Enhancements**

- Add better cache mechanism for faster resolution of frequently queried domains.
- Implement error handling for malformed or unsupported requests.
- Build a GUI for user-friendly management of DNS records.

---





