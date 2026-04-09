import requests
import os
import time
import subprocess

def test_app():
    # Start the app in the background
    print("Starting Flask app...")
    env = os.environ.copy()
    env['SERVER_ACCESS_TOKEN'] = 'test-token'
    env['ADMIN_PASSWORD'] = 'admin'
    
    # We need to make sure the app uses our test token
    process = subprocess.Popen(['python', 'app.py'], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3) # Wait for app to start
    
    BASE_URL = "http://localhost:5000"
    HEADERS = {"X-Access-Token": "test-token"}
    
    try:
        # 1. Test Availability Check (should check ZIP first)
        print("Testing /api/check/730...")
        resp = requests.get(f"{BASE_URL}/api/check/730", headers=HEADERS)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.json()}")
        
        # 2. Test Serving Lua
        print("\nTesting /lua/730...")
        resp = requests.get(f"{BASE_URL}/lua/730", headers=HEADERS)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"Content length: {len(resp.text)} bytes")
            print(f"Content preview: {resp.text[:50]}...")
        else:
            print(f"Error: {resp.text}")

        # 3. Test Non-existent file
        print("\nTesting /lua/nonexistent...")
        resp = requests.get(f"{BASE_URL}/lua/nonexistent", headers=HEADERS)
        print(f"Status: {resp.status_code} (Expected 404)")
        
    finally:
        print("\nStopping Flask app...")
        process.terminate()

if __name__ == "__main__":
    test_app()
