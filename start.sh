# Quick Start Script

echo "🚀 Starting Stellar Application..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Stop any existing containers
echo "📦 Cleaning up old containers..."
docker-compose down --remove-orphans 2>/dev/null || true

echo ""
echo "🔨 Building and starting services..."
echo "   This may take 5-10 minutes on first run..."
echo ""

# Build and start in detached mode
docker-compose up --build -d

# Wait a bit for services to start
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Show status
echo ""
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   Admin:    http://localhost:8000/admin"
echo ""
echo "📝 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop:"
echo "   docker-compose down"
echo ""
