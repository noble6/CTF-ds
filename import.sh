#!/bin/bash

echo "=========================================="
echo "  CTF Challenge Import Tool"
echo "=========================================="
echo ""

CTFD_URL="http://localhost:8000"

echo "CTFd URL: $CTFD_URL"
echo ""

read -p "Enter your CTFd API token: " TOKEN

if [ -z "$TOKEN" ]; then
    echo "Error: No token provided!"
    exit 1
fi

echo ""
echo "Importing challenges..."
echo ""

python3 scripts/import_challenges.py --url "$CTFD_URL" --token "$TOKEN"

echo ""
echo "=========================================="
echo "  Import Complete!"
echo "=========================================="
echo ""
echo "Challenges are now visible at: http://192.168.31.217:8000"
echo ""
echo "Web challenges are accessible from the challenge descriptions."
echo "Participants will click the link in each challenge to access the web app."
