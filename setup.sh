#!/bin/bash

echo "🌟 Stellar Application Setup Script"
echo "===================================="
echo ""

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Copy .env file if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Backend .env file created"
else
    echo "✓ Backend .env file already exists"
fi

cd ..

# Frontend setup
echo ""
echo "📦 Setting up frontend..."
cd frontend

# Copy .env file if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Frontend .env file created"
else
    echo "✓ Frontend .env file already exists"
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application with Docker:"
echo "  docker-compose up --build"
echo ""
echo "Or to start manually:"
echo "  Backend:  cd backend && python manage.py runserver"
echo "  Frontend: cd frontend && npm start"
echo ""
echo "🚀 Happy coding with Stellar!"
