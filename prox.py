import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Function to fetch the list of proxies from the given URL
def fetch_proxies(url):
    response = requests.get(url)
    proxies = response.text.split('\n')
    return [proxy.strip() for proxy in proxies if proxy.strip()]

# Function to check if a proxy is alive
def is_proxy_alive(proxy):
    test_url = 'http://www.example.com'  # A simple and reliable endpoint to test
    proxies = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}',
    }
    try:
        response = requests.get(test_url, proxies=proxies, timeout=5)
        if response.status_code == 200 and "Example Domain" in response.text:
            return proxy
        else:
            return None
    except Exception:
        return None

# Function to write alive proxies to a file
def write_alive_proxies(alive_proxies, filename):
    with open(filename, 'w') as f:
        for proxy in alive_proxies:
            f.write(proxy + '\n')

def main():
    url = 'https://raw.githubusercontent.com/r00tee/Proxy-List/main/Https.txt'  # Replace with your URL
    output_file = 'alive_proxies.txt'

    # Fetch the proxies
    print("Fetching proxies...")
    proxies = fetch_proxies(url)
    print(f"Total proxies fetched: {len(proxies)}")

    # Check the proxies
    alive_proxies = []
    checked_count = 0

    print("Checking proxies...")
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=200) as executor:
        future_to_proxy = {executor.submit(is_proxy_alive, proxy): proxy for proxy in proxies}
        for future in as_completed(future_to_proxy):
            checked_count += 1
            proxy = future_to_proxy[future]
            try:
                result = future.result()
                if result:
                    alive_proxies.append(result)
            except Exception as exc:
                print(f"{proxy} generated an exception: {exc}")
            print(f"Checked {checked_count}/{len(proxies)} proxies, Alive: {len(alive_proxies)}", end='\r')

    end_time = time.time()
    print(f"\nChecking completed in {end_time - start_time:.2f} seconds.")
    print(f"Total alive proxies: {len(alive_proxies)}")

    # Write alive proxies to a file
    write_alive_proxies(alive_proxies, output_file)
    print(f"Alive proxies saved to {output_file}")

if __name__ == '__main__':
    main()