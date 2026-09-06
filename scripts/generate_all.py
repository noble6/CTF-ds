#!/usr/bin/env python3

import os
import json
import subprocess
from pathlib import Path

def generate_challenge_files():

    base_dir = Path(__file__).parent.parent
    
    print("Generating Challenge Files...")
    print("=" * 50)
    
    print("\n[1/4] Generating Easy challenges...")
    easy_dir = base_dir / "easy"
    for challenge_dir in sorted(easy_dir.iterdir()):
        if challenge_dir.is_dir():
            print(f"  - {challenge_dir.name}")
    
    print("\n[2/4] Generating Medium challenges...")
    medium_dir = base_dir / "medium"
    for challenge_dir in sorted(medium_dir.iterdir()):
        if challenge_dir.is_dir():
            print(f"  - {challenge_dir.name}")
            gen_script = challenge_dir / "generate.py"
            if gen_script.exists():
                try:
                    subprocess.run(["python3", str(gen_script)], 
                                 cwd=str(challenge_dir), 
                                 check=True, 
                                 capture_output=True)
                    print(f"    Generated files")
                except subprocess.CalledProcessError as e:
                    print(f"    Warning: Could not run generator: {e}")
    
    print("\n[3/4] Generating Hard challenges...")
    hard_dir = base_dir / "hard"
    for challenge_dir in sorted(hard_dir.iterdir()):
        if challenge_dir.is_dir():
            print(f"  - {challenge_dir.name}")
            gen_script = challenge_dir / "generate.py"
            if gen_script.exists():
                try:
                    subprocess.run(["python3", str(gen_script)], 
                                 cwd=str(challenge_dir), 
                                 check=True, 
                                 capture_output=True)
                    print(f"    Generated files")
                except subprocess.CalledProcessError as e:
                    print(f"    Warning: Could not run generator: {e}")
    
    print("\n[4/4] Challenge file generation complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Start CTFd: cd ctfd_setup && ./setup.sh")
    print("2. Get API token from CTFd admin panel")
    print("3. Run: python3 scripts/import_challenges.py --url http://localhost:8000 --token YOUR_TOKEN")

def generate_challenge_json():

    from import_challenges import CHALLENGES
    
    output_file = Path(__file__).parent / "challenges.json"
    
    with open(output_file, 'w') as f:
        json.dump(CHALLENGES, f, indent=2)
    
    print(f"\nChallenge data exported to: {output_file}")
    print("You can use this file to manually import challenges into CTFd")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'json':
        generate_challenge_json()
    else:
        generate_challenge_files()
