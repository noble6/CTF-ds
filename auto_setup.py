#!/usr/bin/env python3

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def get_csrf_token(session):
    resp = session.get(f"{BASE_URL}/register")
    for line in resp.text.split('\n'):
        if 'csrfNonce' in line:
            start = line.find('"') + 1
            end = line.find('"', start)
            return line[start:end]
    return None

def register_admin(session, name, email, password):
    csrf = get_csrf_token(session)
    if not csrf:
        print("Failed to get CSRF token")
        return False
    
    data = {
        'name': name,
        'email': email,
        'password': password,
        'nonce': csrf
    }
    
    resp = session.post(f"{BASE_URL}/register", data=data, allow_redirects=True)
    
    if resp.status_code == 200:
        return True
    return False

def login(session, name, password):
    resp = session.get(f"{BASE_URL}/login")
    csrf = None
    for line in resp.text.split('\n'):
        if 'csrfNonce' in line:
            start = line.find('"') + 1
            end = line.find('"', start)
            csrf = line[start:end]
            break
    
    if not csrf:
        print("Failed to get CSRF token for login")
        return False
    
    data = {
        'name': name,
        'password': password,
        'nonce': csrf
    }
    
    resp = session.post(f"{BASE_URL}/login", data=data, allow_redirects=True)
    return resp.status_code == 200

def get_api_token(session):
    resp = session.get(f"{BASE_URL}/api/v1/token")
    if resp.status_code == 200:
        try:
            data = resp.json()
            return data.get('data', {}).get('token') or data.get('token')
        except:
            pass
    
    resp = session.get(f"{BASE_URL}/admin/config")
    if 'api_token' in resp.text.lower() or 'token' in resp.text.lower():
        import re
        match = re.search(r'token["\s:=]+([a-f0-9]+)', resp.text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def main():
    print("=" * 50)
    print("CTFd Auto Setup & Import Tool")
    print("=" * 50)
    print()
    
    admin_user = "admin"
    admin_email = "admin@college-ctf.local"
    admin_pass = "admin123"
    
    session = requests.Session()
    
    print("[*] Registering admin account...")
    if register_admin(session, admin_user, admin_email, admin_pass):
        print(f"[+] Admin account created: {admin_user}")
    else:
        print("[*] Registration may have failed, trying to login...")
    
    print("[*] Logging in...")
    if login(session, admin_user, admin_pass):
        print("[+] Logged in successfully")
    else:
        print("[!] Login failed. Please register manually at http://192.168.31.217:8000/register")
        print(f"    Username: {admin_user}")
        print(f"    Email: {admin_email}")
        print(f"    Password: {admin_pass}")
        print()
        print("Then run this script again or import manually.")
        return
    
    print("[*] Getting API token...")
    token = get_api_token(session)
    
    if not token:
        print("[!] Could not get API token automatically.")
        print("[*] Go to: http://192.168.31.217:8000/admin/config")
        print("[*] Look for API section and copy the token")
        print()
        token = input("Enter API token manually: ").strip()
    
    if not token:
        print("[!] No token provided. Exiting.")
        return
    
    print(f"[+] API Token: {token}")
    print()
    print("[*] Importing challenges...")
    
    import subprocess
    result = subprocess.run([
        sys.executable, 
        "scripts/import_challenges.py",
        "--url", BASE_URL,
        "--token", token
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    if result.returncode == 0:
        print()
        print("=" * 50)
        print("[+] SETUP COMPLETE!")
        print("=" * 50)
        print()
        print(f"CTFd URL: http://192.168.31.217:8000")
        print(f"Admin User: {admin_user}")
        print(f"Admin Pass: {admin_pass}")
        print()
        print("All 25 challenges imported!")
        print("Web challenges are linked in their descriptions.")
    else:
        print("[!] Import failed. Try running manually.")

if __name__ == '__main__':
    main()
