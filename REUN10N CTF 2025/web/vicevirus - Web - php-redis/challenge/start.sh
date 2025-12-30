#!/bin/bash

echo "🚀 TechCorp Network Monitor"
echo "============================"
echo ""

echo "[*] Starting services..."
docker-compose up -d

echo "[*] Waiting for initialization..."
sleep 5

if docker-compose ps | grep -q "Up"; then
    echo "✅ Services are running!"
    echo ""
    echo "🌐 Application URL: http://localhost:8080"
    echo ""
    echo "To stop services: ./stop.sh"
    echo ""
else
    echo "❌ Failed to start services"
    docker-compose logs
    exit 1
fi
