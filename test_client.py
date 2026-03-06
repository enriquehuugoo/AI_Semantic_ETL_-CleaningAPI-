import requests
import json
import os
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    print("Testing /health...")
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(f"Status: {r.status_code}")
        if r.status_code != 200:
            return False
    except Exception as e:
        print(f"Error connecting: {e}")
        return False
    return True

def test_clean(filename):
    print(f"\nTesting /v1/clean with {filename}...")
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return None
        
    files = {'file': open(filename, 'rb')}
    
    try:
        r = requests.post(f"{BASE_URL}/v1/clean", files=files)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print("Metadata:", json.dumps(data['metadata'], indent=2))
            return data
        else:
            print("Error:", r.text)
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_chunk(markdown_text):
    print("\nTesting /v1/chunk...")
    payload = {"markdown": markdown_text}
    
    try:
        r = requests.post(f"{BASE_URL}/v1/chunk", json=payload)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Successfully created {len(data['chunks'])} chunks.")
            return True
        else:
            print("Error:", r.text)
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

def wait_for_server():
    print("Waiting for server to start...")
    for i in range(10):
        if test_health():
            print("Server is up!")
            return True
        time.sleep(2)
    print("Server failed to come up.")
    return False

if __name__ == "__main__":
    if not wait_for_server():
        sys.exit(1)
        
    clean_result = test_clean("sample.html")
    
    if clean_result and "markdown" in clean_result:
        test_chunk(clean_result["markdown"])
    else:
        print("Clean failed, skipping chunk test.")

    print("\nTests completed.")
