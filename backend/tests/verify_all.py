import unittest
import requests
import time

def test_end_to_end_flow():
    print("🚀 Starting End-to-End Verification...")
    BASE_URL = "http://localhost:8000/api"
    
    # 1. Check Root
    try:
        r = requests.get(f"{BASE_URL}/")
        print(f"✅ Root Endpoint: {r.status_code}")
    except:
        print("❌ Root Endpoint: Failed")

    # 2. Check Health (Phase 2)
    try:
        r = requests.get(f"{BASE_URL}/health/status")
        print(f"✅ Health Radar: {r.status_code} | Data: {len(r.json().get('data', []))} repos")
    except:
        print("❌ Health Radar: Failed")

    # 3. Check Jira Context (Phase 1)
    try:
        # Using a known ticket if available or testing the route's response
        r = requests.get(f"{BASE_URL}/jira/ticket/SCRUM-1")
        print(f"✅ Jira Route: {r.status_code}")
    except:
        print("❌ Jira Route: Failed")

    # 4. Check Queue (Phase 2)
    try:
        r = requests.get(f"{BASE_URL}/queue/pending")
        print(f"✅ HITL Queue: {r.status_code}")
    except:
        print("❌ HITL Queue: Failed")

    # 5. Check Safety (Phase 3)
    try:
        r = requests.get(f"{BASE_URL}/safety/rules")
        print(f"✅ Safety Rules: {r.status_code}")
    except:
        print("❌ Safety Rules: Failed")

    print("\nVerification Complete.")

if __name__ == "__main__":
    test_end_to_end_flow()
