#!/bin/bash
echo "🐳 Checking Docker setup..."
echo ""
echo "Files:"
ls -la Dockerfile docker-compose.yml entrypoint.sh
echo ""
echo "Building image..."
docker build -t amakaziwatch-backend:latest .
echo ""
echo "Starting services..."
docker-compose up -d
echo ""
echo "Checking status..."
docker-compose ps
echo ""
echo "Logs:"
docker-compose logs --tail=20