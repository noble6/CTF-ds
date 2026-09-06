#!/usr/bin/env python3
"""
Hint Configuration for CTFd
Defines hints and their costs for all challenges
"""

HINTS = {
    # ==================== EASY CHALLENGES ====================
    "Welcome": [
        {
            "content": "Read the challenge description very carefully. Sometimes the answer is hiding in plain sight.",
            "cost": 0,
            "type": "standard"
        }
    ],
    "Base What?": [
        {
            "content": "This encoding is very common on the web. It uses A-Z, a-z, 0-9, +, and / characters.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Try searching for 'base64 decode' online.",
            "cost": 10,
            "type": "standard"
        }
    ],
    "Inspect Me": [
        {
            "content": "Right-click on the page and look for 'Inspect' or 'View Page Source'.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Check the HTML comments. They sometimes hide secrets.",
            "cost": 10,
            "type": "standard"
        }
    ],
    "Hex Dump": [
        {
            "content": "Each pair of characters represents one letter in ASCII.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "66 = 'f', 6c = 'l', 61 = 'a', 67 = 'g'... see the pattern?",
            "cost": 15,
            "type": "standard"
        }
    ],
    "Cookie Monster": [
        {
            "content": "Open Developer Tools (F12) and look at the Application/Storage tab.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "There's a cookie called 'role'. What happens if you change its value?",
            "cost": 15,
            "type": "standard"
        }
    ],
    "Caesar's Secret": [
        {
            "content": "Julius Caesar used a simple substitution cipher. Each letter is shifted by a fixed amount.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "ROT13 is a Caesar cipher with shift 13. Apply it again to decrypt.",
            "cost": 15,
            "type": "standard"
        }
    ],
    "File Type": [
        {
            "content": "File extensions are just labels. The actual file format is determined by magic bytes.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Try opening the file in a hex editor or use the 'file' command.",
            "cost": 15,
            "type": "standard"
        }
    ],
    "Hidden Message": [
        {
            "content": "Sometimes secrets are hidden among lots of noise.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Use the 'strings' command or grep for 'flag{'.",
            "cost": 20,
            "type": "standard"
        }
    ],
    "ROT13": [
        {
            "content": "ROT13 rotates each letter by 13 positions. A becomes N, B becomes O, etc.",
            "cost": 0,
            "type": "standard"
        }
    ],
    "SQL Rookie": [
        {
            "content": "Think about how SQL queries work. What happens if you add special characters?",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "The -- in SQL makes the rest of the line a comment.",
            "cost": 20,
            "type": "standard"
        },
        {
            "content": "Try: admin' -- as the username with any password.",
            "cost": 40,
            "type": "standard"
        }
    ],

    # ==================== MEDIUM CHALLENGES ====================
    "Stego 101": [
        {
            "content": "Images can hide data in their pixels or metadata.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Try using steghide or an online steganography tool.",
            "cost": 25,
            "type": "standard"
        },
        {
            "content": "The password might be something simple and common.",
            "cost": 50,
            "type": "standard"
        }
    ],
    "Broken Auth": [
        {
            "content": "JWT tokens have 3 parts: header.payload.signature",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Decode the JWT at jwt.io. What's in the payload?",
            "cost": 25,
            "type": "standard"
        },
        {
            "content": "The secret key is very weak. Try common secrets.",
            "cost": 50,
            "type": "standard"
        }
    ],
    "RSA Baby": [
        {
            "content": "RSA security relies on the difficulty of factoring N into p and q.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "This N is small. Try factoring it or searching for the primes.",
            "cost": 35,
            "type": "standard"
        },
        {
            "content": "p = 1000000007, q = 1000000009. These are well-known primes!",
            "cost": 70,
            "type": "standard"
        }
    ],
    "Path Traversal": [
        {
            "content": "What happens if you use ../ in the filename?",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Try: ../private/flag.txt",
            "cost": 35,
            "type": "standard"
        }
    ],
    "XSS Reflected": [
        {
            "content": "XSS means injecting JavaScript into a webpage.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Try putting <script>alert('test')</script> in the search box.",
            "cost": 30,
            "type": "standard"
        }
    ],
    "Pcap Analysis": [
        {
            "content": "Open the pcap file in Wireshark and look at the HTTP traffic.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Filter by 'http' and look at the request parameters.",
            "cost": 40,
            "type": "standard"
        }
    ],
    "Vigenere": [
        {
            "content": "The Vigenere cipher uses a keyword to shift each letter by different amounts.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "The key is related to this CTF event. What's the venue?",
            "cost": 30,
            "type": "standard"
        }
    ],
    "IDOR": [
        {
            "content": "IDOR stands for Insecure Direct Object Reference.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Look at the URL parameters. Can you change the user_id?",
            "cost": 35,
            "type": "standard"
        }
    ],
    "Strings++": [
        {
            "content": "The flag is obfuscated, not absent. Look for patterns in the binary.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Try a hex editor. Look for XOR patterns.",
            "cost": 40,
            "type": "standard"
        }
    ],
    "Weak Hash": [
        {
            "content": "MD5 is a hashing algorithm. Try to find what was hashed.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Use an online MD5 cracker or hashcat.",
            "cost": 40,
            "type": "standard"
        },
        {
            "content": "The password is something you'd find at this event.",
            "cost": 80,
            "type": "standard"
        }
    ],

    # ==================== HARD CHALLENGES ====================
    "SSRF Master": [
        {
            "content": "SSRF means making the server fetch URLs you specify.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "127.0.0.1 can be represented in many ways: decimal, hex, octal...",
            "cost": 50,
            "type": "standard"
        },
        {
            "content": "2130706433 in decimal equals 127.0.0.1",
            "cost": 100,
            "type": "standard"
        },
        {
            "content": "The internal service is on port 9999.",
            "cost": 150,
            "type": "standard"
        }
    ],
    "Padding Oracle": [
        {
            "content": "The server gives different errors for bad padding vs bad data.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "This is a classic Padding Oracle Attack on CBC mode.",
            "cost": 70,
            "type": "standard"
        },
        {
            "content": "Use padbuster or write a Python script to exploit the oracle.",
            "cost": 140,
            "type": "standard"
        }
    ],
    "Buffer Overflow": [
        {
            "content": "The 'authorized' variable needs to be non-zero to get the flag.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "The buffer is 64 bytes. What happens if you write more than 64 bytes?",
            "cost": 80,
            "type": "standard"
        },
        {
            "content": "Send 64 'A's followed by a non-zero value.",
            "cost": 160,
            "type": "standard"
        }
    ],
    "Memory Forensics": [
        {
            "content": "Use the 'strings' command and grep for 'flag{'.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Try Volatility for deeper analysis.",
            "cost": 60,
            "type": "standard"
        }
    ],
    "Obfuscated RE": [
        {
            "content": "The binary uses XOR encryption with a rolling key.",
            "cost": 0,
            "type": "standard"
        },
        {
            "content": "Look for the data section after the string 'Reverse engineer me...'",
            "cost": 70,
            "type": "standard"
        },
        {
            "content": "The XOR key seed is 0x42. The shuffle seed is 1337.",
            "cost": 140,
            "type": "standard"
        }
    ]
}

def get_hints_for_challenge(challenge_name):
    """Get hints for a specific challenge"""
    return HINTS.get(challenge_name, [])

def get_all_hints():
    """Get all hints"""
    return HINTS

if __name__ == '__main__':
    total_hints = sum(len(h) for h in HINTS.values())
    total_cost = sum(sum(h['cost'] for h in hints) for hints in HINTS.values())
    
    print(f"Total challenges with hints: {len(HINTS)}")
    print(f"Total hints: {total_hints}")
    print(f"Total possible hint cost: {total_cost} points")
    print()
    
    for challenge, hints in HINTS.items():
        print(f"{challenge}:")
        for i, hint in enumerate(hints, 1):
            print(f"  Hint {i} ({hint['cost']} pts): {hint['content'][:50]}...")
