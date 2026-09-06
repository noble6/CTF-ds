#!/usr/bin/env python3
"""
CTF Challenge Verification Script
Tests all challenges to ensure they work correctly before the event

Usage: python3 verify_challenges.py [--url http://localhost:8000] [--token YOUR_TOKEN]
"""

import requests
import json
import sys
import os
import subprocess
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from import_challenges import CHALLENGES

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def test_web_challenge(name, port, endpoint="/"):
    """Test if a web challenge is running"""
    url = f"http://localhost:{port}{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def test_challenge_files():
    """Verify all challenge files exist"""
    print(f"\n{Colors.BLUE}Testing Challenge Files...{Colors.END}")
    print("=" * 50)
    
    base_dir = Path(__file__).parent.parent
    issues = []
    
    for difficulty, challenges in CHALLENGES.items():
        for i, challenge in enumerate(challenges, 1):
            challenge_num = (["easy"] * 10 + ["medium"] * 10 + ["hard"] * 5).index(difficulty) + i
            challenge_dir = base_dir / difficulty / f"{challenge_num:02d}_{challenge['name'].lower().replace(' ', '_').replace("'", '')}"
            
            if not challenge_dir.exists():
                issues.append(f"Missing directory: {challenge_dir}")
                continue
            
            # Check for challenge.txt
            if not (challenge_dir / "challenge.txt").exists():
                issues.append(f"Missing challenge.txt in {challenge_dir}")
            
            # Check for app.py if it's a web challenge
            if "Web" in challenge.get('category', '') or any(x in challenge['name'].lower() for x in ['cookie', 'sql', 'auth', 'path', 'xss', 'idor', 'ssrf', 'padding']):
                if not (challenge_dir / "app.py").exists():
                    issues.append(f"Missing app.py in {challenge_dir}")
    
    if issues:
        print(f"{Colors.RED}Found {len(issues)} issues:{Colors.END}")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"{Colors.GREEN}✓ All challenge files present!{Colors.END}")
    
    return len(issues) == 0

def test_web_challenges():
    """Test all web challenges are running"""
    print(f"\n{Colors.BLUE}Testing Web Challenges...{Colors.END}")
    print("=" * 50)
    
    web_challenges = {
        "Cookie Monster": 5002,
        "SQL Rookie": 5003,
        "Broken Auth": 5004,
        "Path Traversal": 5005,
        "XSS Reflected": 5006,
        "IDOR": 5007,
        "SSRF Master": 5008,
        "Padding Oracle": 5009
    }
    
    running = 0
    stopped = 0
    
    for name, port in web_challenges.items():
        if test_web_challenge(name, port):
            print(f"  {Colors.GREEN}✓{Colors.END} {name} (port {port})")
            running += 1
        else:
            print(f"  {Colors.RED}✗{Colors.END} {name} (port {port}) - Not running")
            stopped += 1
    
    print(f"\n  Running: {running}, Stopped: {stopped}")
    return running

def test_ctfd_connection(url, token):
    """Test CTFd API connection"""
    print(f"\n{Colors.BLUE}Testing CTFd Connection...{Colors.END}")
    print("=" * 50)
    
    try:
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(f"{url}/api/v1/challenges", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  {Colors.GREEN}✓{Colors.END} Connected to CTFd")
            print(f"  {Colors.GREEN}✓{Colors.END} API working (found {len(data.get('data', []))} challenges)")
            return True
        else:
            print(f"  {Colors.RED}✗{Colors.END} API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  {Colors.RED}✗{Colors.END} Connection failed: {e}")
        return False

def test_flags():
    """Verify all flags are unique and properly formatted"""
    print(f"\n{Colors.BLUE}Testing Flags...{Colors.END}")
    print("=" * 50)
    
    all_flags = []
    issues = []
    
    for difficulty, challenges in CHALLENGES.items():
        for challenge in challenges:
            flag = challenge['flag']
            
            # Check flag format
            if not flag.startswith('flag{') or not flag.endswith('}'):
                issues.append(f"{challenge['name']}: Invalid flag format")
            
            # Check for duplicates
            if flag in all_flags:
                issues.append(f"{challenge['name']}: Duplicate flag")
            
            all_flags.append(flag)
    
    if issues:
        print(f"{Colors.RED}Found {len(issues)} issues:{Colors.END}")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"{Colors.GREEN}✓ All {len(all_flags)} flags are unique and properly formatted!{Colors.END}")
    
    return len(issues) == 0

def test_points():
    """Verify point values are correct"""
    print(f"\n{Colors.BLUE}Testing Points...{Colors.END}")
    print("=" * 50)
    
    expected_points = {
        'easy': (100, 200),
        'medium': (300, 400),
        'hard': (500, 800)
    }
    
    issues = []
    total_points = 0
    
    for difficulty, challenges in CHALLENGES.items():
        for challenge in challenges:
            points = challenge['value']
            min_pts, max_pts = expected_points[difficulty]
            
            if points < min_pts or points > max_pts:
                issues.append(f"{challenge['name']}: {points} pts (expected {min_pts}-{max_pts})")
            
            total_points += points
    
    if issues:
        print(f"{Colors.YELLOW}Point value warnings:{Colors.END}")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"{Colors.GREEN}✓ All point values within expected ranges!{Colors.END}")
    
    print(f"\n  Total points: {total_points}")
    return len(issues) == 0

def generate_report():
    """Generate verification report"""
    print("\n" + "=" * 50)
    print("  CTF CHALLENGE VERIFICATION REPORT")
    print("=" * 50)
    
    results = {
        'files': test_challenge_files(),
        'flags': test_flags(),
        'points': test_points(),
        'web': test_web_challenges() > 0
    }
    
    print("\n" + "=" * 50)
    print("  SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for test, passed in results.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if passed else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {test.upper():15} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print(f"  {Colors.GREEN}ALL TESTS PASSED!{Colors.END}")
        print("  Your CTF is ready to run!")
    else:
        print(f"  {Colors.YELLOW}SOME TESTS FAILED{Colors.END}")
        print("  Please fix the issues above before running the CTF.")
    print("=" * 50)
    
    return all_passed

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Verify CTF challenges')
    parser.add_argument('--url', help='CTFd URL for API test')
    parser.add_argument('--token', help='CTFd API token')
    parser.add_argument('--quick', action='store_true', help='Quick test (files only)')
    
    args = parser.parse_args()
    
    if args.quick:
        test_challenge_files()
        test_flags()
        test_points()
    else:
        success = generate_report()
        
        if args.url and args.token:
            test_ctfd_connection(args.url, args.token)
        
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
