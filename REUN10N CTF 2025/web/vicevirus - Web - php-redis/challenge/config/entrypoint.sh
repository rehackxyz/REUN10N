#!/bin/bash

USERNAME="admin"
PASSWORD=$(openssl rand -hex 16)

htpasswd -bc /etc/apache2/.htpasswd "$USERNAME" "$PASSWORD"

echo "========================================"
echo "TechCorp Network Monitor - Starting"
echo "========================================"
echo "Admin credentials:"
echo "Username: $USERNAME"
echo "Password: $PASSWORD"
echo "========================================"

exec apache2ctl -D FOREGROUND
