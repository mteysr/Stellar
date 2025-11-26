# 🌟 Stellar Blockchain Application

A modern web application - Secure authentication with Stellar blockchain and Freighter wallet integration.

## 📋 Table of Contents
- [Features](#-features)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Smart Contract](#-smart-contract)
- [Contributing](#-contributing)

## ✨ Features

### 🔐 Authentication
- ✅ **Freighter Wallet Integration**: Secure wallet connection and authentication
- ✅ **Session Management**: Secure session management
- ✅ **Signature Verification**: Blockchain-based signature verification

### 💰 Stellar Blockchain Operations
- ✅ **Balance Query**: View XLM and all asset balances
- ✅ **Send Payment**: XLM and custom token transfers
- ✅ **Transaction History**: View detailed transaction history
- ✅ **Multi-Asset Support**: Native and custom asset support
- ✅ **Memo Support**: Add memos to transactions

### 🛠 Technical Features
- ✅ **Stellar Network**: Testnet and Mainnet support
- ✅ **Django Backend**: Powerful backend with RESTful API
- ✅ **Vanilla JS Frontend**: Modern and responsive user interface
- ✅ **Docker Support**: Fully dockerized application
- ✅ **Smart Contract**: Soroban example contract

## 🛠 Technologies

### Backend
- Python 3.11
- Django 4.2
- Django REST Framework
- Stellar SDK
- Gunicorn

### Frontend
- Vanilla JavaScript (ES6+)
- Freighter API
- Modern CSS
- Nginx Alpine

### Blockchain
- Stellar Network
- Soroban Smart Contracts
- Freighter Wallet

### DevOps
- Docker
- Docker Compose
- Nginx

## 🚀 Installation

### Requirements
- Docker and Docker Compose
- Freighter Wallet browser extension

### Step 1: Clone the Repository
```bash
cd /root/Stellar
```

### Step 2: Set Up Environment Variables

For backend:
```bash
cp backend/.env.example backend/.env
```

Edit the `.env` file:
```env
DEBUG=True
DJANGO_SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,backend
STELLAR_NETWORK=testnet
```

For frontend:
```bash
cp frontend/.env.example frontend/.env
```

### Step 3: Start with Docker
```bash
docker-compose up --build
```

This command will:
- Build and run backend on port 8000
- Build and run frontend on port 3000
- Install all required dependencies

### Step 4: Open in Browser
```
http://localhost:3000
```

## 💻 Manual Installation (Without Docker)

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Start development server
npm start
```

Frontend: `http://localhost:3000`
Backend: `http://localhost:8000`
Admin Panel: `http://localhost:8000/admin`

## 📖 Usage

### 1. Freighter Wallet Setup
If you haven't installed it yet:
- Install [Freighter Wallet](https://www.freighter.app/) extension in your browser
- Create a new wallet or import your existing wallet
- Switch to Testnet (Settings > Network > Testnet)

### 2. Login to Application
1. Open the application: `http://localhost:3000`
2. Click "Connect Freighter Wallet" button
3. Confirm "Connect" in Freighter popup
4. Click "Sign" button when signature is requested
5. You will be redirected to the Dashboard

### 3. Features
- **Wallet Information**: View public key and account details
- **Session Management**: Secure session management
- **Logout**: Securely log out

## 🔌 API Endpoints

### Authentication

#### Connect Wallet
```http
POST /api/auth/connect/
Content-Type: application/json

{
  "public_key": "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

Response:
```json
{
  "challenge": "Sign this message to authenticate...",
  "session_key": "session_key_here",
  "public_key": "GXXXXXXX...",
  "expires_at": "2024-01-01T12:00:00Z"
}
```

#### Verify Signature
```http
POST /api/auth/verify/
Content-Type: application/json

{
  "public_key": "GXXXXXXX...",
  "signature": "signature_here",
  "challenge": "challenge_message"
}
```

#### Get Wallet Info
```http
GET /api/auth/wallet/
```

#### Logout
```http
POST /api/auth/logout/
```

### Stellar Blockchain Operations

#### Get Balance
Get account balance with all assets:
```http
GET /api/auth/balance/
# or
GET /api/auth/balance/{public_key}/
```

Response:
```json
{
  "public_key": "GXXXXXXX...",
  "balances": [
    {
      "asset_type": "native",
      "asset_code": "XLM",
      "balance": "10000.0000000",
      "asset_issuer": null
    },
    {
      "asset_type": "credit_alphanum4",
      "asset_code": "USDC",
      "balance": "500.0000000",
      "asset_issuer": "GXXXXXXX..."
    }
  ],
  "total_assets": 2
}
```

#### Send Payment
Send XLM or custom assets:
```http
POST /api/auth/payment/
Content-Type: application/json

{
  "destination": "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "amount": "10.50",
  "asset_code": "XLM",
  "memo": "Payment for services",
  "secret_key": "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

For custom assets:
```json
{
  "destination": "GXXXXXXX...",
  "amount": "100",
  "asset_code": "USDC",
  "asset_issuer": "GXXXXXXX...",
  "memo": "Custom token payment",
  "secret_key": "SXXXXXXX..."
}
```

Response:
```json
{
  "success": true,
  "transaction_hash": "abc123...",
  "source_account": "GXXXXXXX...",
  "destination": "GXXXXXXX...",
  "amount": "10.50",
  "asset_code": "XLM",
  "ledger": 12345,
  "memo": "Payment for services"
}
```

#### Get Transaction History
Get transaction history for an account:
```http
GET /api/auth/transactions/?limit=20
# or
GET /api/auth/transactions/{public_key}/?limit=20
```

Response:
```json
{
  "public_key": "GXXXXXXX...",
  "transactions": [
    {
      "id": "123456789",
      "type": "payment",
      "created_at": "2024-01-01T12:00:00Z",
      "transaction_hash": "abc123...",
      "source_account": "GXXXXXXX...",
      "from_address": "GXXXXXXX...",
      "to_address": "GXXXXXXX...",
      "amount": "100.0000000",
      "asset_code": "XLM",
      "asset_type": "native"
    }
  ],
  "total_transactions": 15,
  "limit": 20
}
```

## 📜 Smart Contract

The project includes an example Soroban smart contract.

### Building the Contract
```bash
cd contracts/hello_contract

# Install Soroban CLI (first time)
cargo install --locked soroban-cli

# Build the contract
soroban contract build
```

### Deploying to Testnet
```bash
# Add network
soroban network add testnet \
  --rpc-url https://soroban-testnet.stellar.org:443 \
  --network-passphrase "Test SDF Network ; September 2015"

# Create identity
soroban keys generate deployer --network testnet

# Deploy
soroban contract deploy \
  --wasm target/wasm32-unknown-unknown/release/hello_contract.wasm \
  --source deployer \
  --network testnet
```

### Contract Functions
- `hello(to: Symbol)`: Returns a greeting message
- `store(user: Address, value: u32)`: Stores a value
- `get(user: Address)`: Retrieves the stored value

For details: [contracts/README.md](contracts/README.md)

## 🏗 Project Structure

```
Stellar/
├── backend/                    # Django backend
│   ├── authentication/         # Auth app
│   │   ├── models.py          # Wallet & Session models
│   │   ├── views.py           # API endpoints
│   │   ├── serializers.py     # DRF serializers
│   │   └── urls.py            # URL routing
│   ├── stellar_project/       # Django project
│   │   ├── settings.py        # Django settings
│   │   └── urls.py            # Main URLs
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend Docker image
│   └── manage.py             # Django management
├── frontend/                  # React frontend
│   ├── public/               # Static files
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── FreighterLogin.js
│   │   │   └── Dashboard.js
│   │   ├── utils/           # Utilities
│   │   │   ├── freighter.js # Freighter integration
│   │   │   └── api.js       # API calls
│   │   ├── App.js           # Main app
│   │   └── index.js         # Entry point
│   ├── package.json         # Node dependencies
│   ├── Dockerfile          # Frontend Docker image
│   └── nginx.conf          # Nginx configuration
├── contracts/               # Stellar smart contracts
│   ├── hello_contract/     # Example Soroban contract
│   │   ├── src/lib.rs     # Contract code
│   │   └── Cargo.toml     # Rust dependencies
│   └── README.md          # Contract documentation
├── docker-compose.yml      # Docker orchestration
└── README.md              # This file
```

## 🔧 Development

### Making Changes to Backend
```bash
cd backend
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### Making Changes to Frontend
```bash
cd frontend
npm start  # Hot reload active
```

### Development with Docker
```bash
# Rebuild containers
docker-compose up --build

# Restart only backend
docker-compose restart backend

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Contract Tests
```bash
cd contracts/hello_contract
cargo test
```

## 🐛 Troubleshooting

### Freighter cannot connect
- Make sure Freighter extension is up to date
- Check that you are on Testnet
- Review error messages in browser console

### Docker build errors
```bash
# Clear cache and rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### CORS errors
- Check `CORS_ALLOWED_ORIGINS` setting in backend `.env` file
- Make sure frontend URL is added to the list

### Port already in use
```bash
# Change ports (docker-compose.yml)
ports:
  - "8001:8000"  # Backend
  - "3001:80"    # Frontend
```

## 🆘 Freighter Extension Issues

**PROBLEM:** If you're getting "Freighter not found" error:

### Quick Fix:
1. **Use extension check tool:** `http://YOUR_IP:3000/extension-check.html`
2. **Do a hard refresh:** `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
3. **Pin Freighter:** Should be visible in browser toolbar
4. **Site access:** chrome://extensions → Freighter → "On all sites"

### Detailed Guide:
- **URGENT_FIX.md** - Emergency troubleshooting guide
- **FREIGHTER_FIX.md** - Comprehensive troubleshooting

### Test Pages:
- **Main Page:** `http://YOUR_IP:3000/`
- **Extension Check:** `http://YOUR_IP:3000/extension-check.html`
- **Debug Page:** `http://YOUR_IP:3000/debug.html`

## 📚 Resources

- [Stellar Documentation](https://developers.stellar.org/)
- [Soroban Documentation](https://soroban.stellar.org/docs)
- [Freighter Wallet](https://www.freighter.app/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Developer

Feel free to open an issue for questions.

---

**Note**: This application runs on testnet. Before moving to production:
- Change secret keys
- Set DEBUG=False
- Use HTTPS
- Implement security best practices
- Add rate limiting

Happy coding with Stellar! 🚀✨
