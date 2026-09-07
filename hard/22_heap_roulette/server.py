#!/usr/bin/env python3

import socket
import subprocess
import threading
import sys
import os

def handle_client(conn, addr):
    try:
        proc = subprocess.Popen(
            ['python3', '/home/DeAd_SeC/ctfd_niw/ctf_college/hard/22_heap_roulette/heap_service.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0
        )
        
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            proc.stdin.write(data)
            proc.stdin.flush()
            
            output = proc.stdout.read1(4096) if hasattr(proc.stdout, 'read1') else proc.stdout.read(4096)
            if output:
                conn.send(output)
            
            if proc.poll() is not None:
                break
    except Exception as e:
        pass
    finally:
        conn.close()
        if proc:
            proc.terminate()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 1337))
    server.listen(5)
    
    print(f"Heap Roulette listening on port 1337")
    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == '__main__':
    main()
