#!/bin/bash

# EV Management Backend Setup Script
# This script helps you set up the EV Management System backend quickly

echo "🚗 EV Management System Backend Setup"
echo "======================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js v16 or higher."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version 16 or higher is required. Current version: $(node --version)"
    exit 1
fi

echo "✅ Node.js $(node --version) detected"

# Check if MongoDB is running
if ! command -v mongod &> /dev/null; then
    echo "⚠️  MongoDB is not installed or not in PATH"
    echo "   Please install MongoDB and ensure it's running"
    echo "   Visit: https://docs.mongodb.com/manual/installation/"
else
    echo "✅ MongoDB detected"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create environment file
if [ ! -f .env ]; then
    echo ""
    echo "⚙️  Creating environment file..."
    cp .env.example .env

    # Generate random JWT secrets
    JWT_SECRET=$(openssl rand -base64 32 2>/dev/null || head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32)
    JWT_REFRESH_SECRET=$(openssl rand -base64 32 2>/dev/null || head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32)

    # Update .env file with generated secrets
    sed -i.bak "s/your-super-secret-jwt-key-here/$JWT_SECRET/" .env
    sed -i.bak "s/your-super-secret-refresh-key-here/$JWT_REFRESH_SECRET/" .env
    rm .env.bak 2>/dev/null || true

    echo "✅ Environment file created with random JWT secrets"
    echo "   Please edit .env file to configure your database and other settings"
else
    echo "✅ Environment file already exists"
fi

# Create logs directory
mkdir -p logs
echo "✅ Logs directory created"

# Create uploads directory
mkdir -p uploads
echo "✅ Uploads directory created"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file to configure your database connection"
echo "2. Ensure MongoDB is running"
echo "3. Start the development server:"
echo "   npm run dev"
echo ""
echo "🌐 The API will be available at: http://localhost:5000"
echo "📚 API Documentation: http://localhost:5000/api/docs"
echo "❤️  Health Check: http://localhost:5000/health"
echo ""
echo "🚀 Happy coding!"