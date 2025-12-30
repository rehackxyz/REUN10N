#!/bin/sh

redis-server /usr/local/etc/redis/redis.conf &
REDIS_PID=$!

sleep 3

redis-cli SET flag "RE:CTF{fake_flag}"
redis-cli SET app_version "TechCorp Monitor v2.4.1"
redis-cli SET last_update "2024-03-15"

echo "[*] Redis initialized"

cat > /tmp/redis-protected.conf << 'EOF'
protected-mode no
bind 0.0.0.0
port 6379
rename-command DEL ""
rename-command UNLINK ""
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command SET ""
rename-command SETEX ""
rename-command SETNX ""
rename-command SETRANGE ""
rename-command MSET ""
rename-command MSETNX ""
rename-command GETSET ""
rename-command APPEND ""
rename-command RENAME ""
rename-command RENAMENX ""
rename-command MOVE ""
rename-command EXPIRE ""
rename-command EXPIREAT ""
rename-command PEXPIRE ""
rename-command PEXPIREAT ""
rename-command RESTORE ""
rename-command MIGRATE ""
rename-command CONFIG ""
rename-command SHUTDOWN ""
EOF

redis-cli SAVE

kill $REDIS_PID
sleep 1
exec redis-server /tmp/redis-protected.conf
