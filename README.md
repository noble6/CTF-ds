# College CTF 2026

A Capture The Flag (CTF) competition for college students.

## Overview

- **25 Challenges** across 3 difficulty levels
- **Categories**: Web, Crypto, Forensics, Reverse, Pwn, Misc
- **Duration**: 4-6 hours (one day event)
- **Platform**: CTFd

## Challenge Breakdown

| Difficulty | Count | Points Range | Total Points |
|------------|-------|--------------|--------------|
| Easy | 10 | 100-200 | 1,450 |
| Medium | 10 | 300-400 | 3,500 |
| Hard | 5 | 500-800 | 3,400 |
| **Total** | **25** | - | **8,350** |

## Directory Structure

```
ctf_college/
├── easy/                    # 10 Easy challenges (100-200 pts)
│   ├── 01_welcome/
│   ├── 02_base_what/
│   ├── 03_inspect_me/
│   ├── 04_hex_dump/
│   ├── 05_cookie_monster/
│   ├── 06_caesar_secret/
│   ├── 07_file_type/
│   ├── 08_hidden_message/
│   ├── 09_rot13/
│   └── 10_sql_rookie/
├── medium/                  # 10 Medium challenges (300-400 pts)
│   ├── 11_stego_101/
│   ├── 12_broken_auth/
│   ├── 13_rsa_baby/
│   ├── 14_path_traversal/
│   ├── 15_xss_reflected/
│   ├── 16_pcap_analysis/
│   ├── 17_vigenere/
│   ├── 18_idor/
│   ├── 19_strings_pp/
│   └── 20_weak_hash/
├── hard/                    # 5 Hard challenges (500-800 pts)
│   ├── 21_ssrf_master/
│   ├── 22_padding_oracle/
│   ├── 23_buffer_overflow/
│   ├── 24_memory_forensics/
│   └── 25_obfuscated_re/
├── ctfd_setup/              # CTFd Docker setup
│   ├── docker-compose.yml
│   └── setup.sh
├── scripts/                 # Utility scripts
│   ├── import_challenges.py
│   └── generate_all.py
└── README.md
```

## Quick Start

### 1. Generate Challenge Files

```bash
cd scripts
python3 generate_all.py
```

### 2. Set Up CTFd

```bash
cd ctfd_setup
chmod +x setup.sh
./setup.sh
```

Access CTFd at: http://localhost:8000

### 3. Import Challenges

1. Get API token from CTFd Admin Panel → Config → API
2. Run import script:

```bash
cd scripts
python3 import_challenges.py --url http://localhost:8000 --token YOUR_API_TOKEN
```

### 4. Deploy Web Challenges

Start the Flask applications for web challenges:

```bash
# Easy Web Challenges
cd easy/05_cookie_monster && python3 app.py &  # Port 5002
cd easy/10_sql_rookie && python3 app.py &      # Port 5003

# Medium Web Challenges
cd medium/12_broken_auth && python3 app.py &   # Port 5004
cd medium/14_path_traversal && python3 app.py & # Port 5005
cd medium/15_xss_reflected && python3 app.py &  # Port 5006
cd medium/18_idor && python3 app.py &          # Port 5007

# Hard Web Challenges
cd hard/21_ssrf_master && python3 app.py &     # Port 5008
cd hard/22_padding_oracle && python3 app.py &  # Port 5009
```

### 5. Make Publicly Accessible (Optional)

Use Cloudflare Tunnel to expose your local server:

```bash
# Install cloudflared
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
chmod +x cloudflared

# Create tunnel
./cloudflared tunnel --url http://localhost:8000
```

## Challenge Details

### Easy (100-200 pts)
1. **Welcome** - Flag in description (Misc)
2. **Base What?** - Base64 decoding (Crypto)
3. **Inspect Me** - HTML inspection (Web)
4. **Hex Dump** - Hex decoding (Crypto)
5. **Cookie Monster** - Cookie manipulation (Web)
6. **Caesar's Secret** - Caesar cipher (Crypto)
7. **File Type** - File extension fix (Forensics)
8. **Hidden Message** - String extraction (Forensics)
9. **ROT13** - ROT13 cipher (Crypto)
10. **SQL Rookie** - Basic SQL injection (Web)

### Medium (300-400 pts)
11. **Stego 101** - Image steganography (Forensics)
12. **Broken Auth** - JWT manipulation (Web)
13. **RSA Baby** - Small RSA primes (Crypto)
14. **Path Traversal** - Directory traversal (Web)
15. **XSS Reflected** - Cross-site scripting (Web)
16. **Pcap Analysis** - Network forensics (Forensics)
17. **Vigenere** - Vigenere cipher (Crypto)
18. **IDOR** - Insecure direct object reference (Web)
19. **Strings++** - Obfuscated strings (Reverse)
20. **Weak Hash** - MD5 cracking (Crypto)

### Hard (500-800 pts)
21. **SSRF Master** - Server-side request forgery (Web)
22. **Padding Oracle** - CBC padding attack (Crypto)
23. **Buffer Overflow** - Stack overflow (Pwn)
24. **Memory Forensics** - Volatility analysis (Forensics)
25. **Obfuscated RE** - Anti-disassembly (Reverse)

## Scoring

- **First Blood Bonus**: +50 points for first solve
- **Hints**: Available for Easy/Medium (-50 points per hint)
- **Time Bonus**: Faster solves = more points (optional)

## Requirements

- Docker & Docker Compose
- Python 3.8+
- Linux/macOS (Windows with WSL2)

## Event Tips

1. **Test everything** before the event
2. **Have backup challenges** in case of issues
3. **Monitor the scoreboard** for suspicious activity
4. **Keep challenge files secure** until event starts
5. **Document solutions** for post-event writeups

## License

Free to use for educational purposes.

Good luck with your CTF event! 🎯
# CTF-ds
