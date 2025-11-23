# 🌟 Stellar Blockchain Application

Modern bir web uygulaması - Stellar blockchain ve Freighter wallet entegrasyonu ile güvenli kimlik doğrulama.

## 📋 İçindekiler
- [Özellikler](#-özellikler)
- [Teknolojiler](#-teknolojiler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [API Endpoints](#-api-endpoints)
- [Smart Contract](#-smart-contract)
- [Katkıda Bulunma](#-katkıda-bulunma)

## ✨ Özellikler

### 🔐 Kimlik Doğrulama
- ✅ **Freighter Wallet Entegrasyonu**: Güvenli wallet bağlantısı ve kimlik doğrulama
- ✅ **Session Management**: Güvenli oturum yönetimi
- ✅ **Signature Verification**: Blockchain tabanlı imza doğrulama

### 💰 Stellar Blockchain İşlemleri
- ✅ **Bakiye Sorgulama**: XLM ve tüm asset bakiyelerini görüntüleme
- ✅ **Ödeme Gönderme**: XLM ve custom token transferi
- ✅ **İşlem Geçmişi**: Detaylı transaction history görüntüleme
- ✅ **Multi-Asset Support**: Native ve custom asset desteği
- ✅ **Memo Support**: İşlemlere memo ekleme

### 🛠 Teknik Özellikler
- ✅ **Stellar Network**: Testnet ve Mainnet desteği
- ✅ **Django Backend**: RESTful API ile güçlü backend
- ✅ **Vanilla JS Frontend**: Modern ve responsive kullanıcı arayüzü
- ✅ **Docker Support**: Tam dockerize edilmiş uygulama
- ✅ **Smart Contract**: Soroban örnek kontratı

## 🛠 Teknolojiler

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

## 🚀 Kurulum

### Gereksinimler
- Docker ve Docker Compose
- Freighter Wallet browser extension

### Adım 1: Repository'yi Klonlayın
```bash
cd /root/Stellar
```

### Adım 2: Environment Variables Ayarlayın

Backend için:
```bash
cp backend/.env.example backend/.env
```

`.env` dosyasını düzenleyin:
```env
DEBUG=True
DJANGO_SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,backend
STELLAR_NETWORK=testnet
```

Frontend için:
```bash
cp frontend/.env.example frontend/.env
```

### Adım 3: Docker ile Başlatın
```bash
docker-compose up --build
```

Bu komut:
- Backend'i build edip 8000 portunda çalıştırır
- Frontend'i build edip 3000 portunda çalıştırır
- Gerekli tüm bağımlılıkları yükler

### Adım 4: Tarayıcıda Açın
```
http://localhost:3000
```

## 💻 Manuel Kurulum (Docker olmadan)

### Backend Kurulumu
```bash
cd backend

# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Environment variables ayarla
cp .env.example .env

# Veritabanı migration'ları çalıştır
python manage.py migrate

# Superuser oluştur (opsiyonel)
python manage.py createsuperuser

# Development server'ı başlat
python manage.py runserver 0.0.0.0:8000
```

### Frontend Kurulumu
```bash
cd frontend

# Bağımlılıkları yükle
npm install

# Environment variables ayarla
cp .env.example .env

# Development server'ı başlat
npm start
```

Frontend: `http://localhost:3000`
Backend: `http://localhost:8000`
Admin Panel: `http://localhost:8000/admin`

## 📖 Kullanım

### 1. Freighter Wallet Kurulumu
Eğer henüz yüklemediyseniz:
- [Freighter Wallet](https://www.freighter.app/) extension'ını tarayıcınıza kurun
- Yeni bir wallet oluşturun veya mevcut wallet'ınızı import edin
- Testnet'e geçin (Settings > Network > Testnet)

### 2. Uygulamaya Giriş
1. Uygulamayı açın: `http://localhost:3000`
2. "Connect Freighter Wallet" butonuna tıklayın
3. Freighter popup'ında "Connect" onaylayın
4. İmza istediğinde "Sign" butonuna tıklayın
5. Dashboard'a yönlendirileceksiniz

### 3. Özellikler
- **Wallet Bilgileri**: Public key ve hesap detaylarını görüntüleyin
- **Session Management**: Güvenli oturum yönetimi
- **Logout**: Güvenli çıkış yapabilirsiniz

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

Proje, örnek bir Soroban smart contract içerir.

### Contract'ı Build Etme
```bash
cd contracts/hello_contract

# Soroban CLI yükle (ilk kez)
cargo install --locked soroban-cli

# Contract'ı build et
soroban contract build
```

### Testnet'e Deploy Etme
```bash
# Network ekle
soroban network add testnet \
  --rpc-url https://soroban-testnet.stellar.org:443 \
  --network-passphrase "Test SDF Network ; September 2015"

# Identity oluştur
soroban keys generate deployer --network testnet

# Deploy
soroban contract deploy \
  --wasm target/wasm32-unknown-unknown/release/hello_contract.wasm \
  --source deployer \
  --network testnet
```

### Contract Fonksiyonları
- `hello(to: Symbol)`: Greeting mesajı döndürür
- `store(user: Address, value: u32)`: Bir değer saklar
- `get(user: Address)`: Saklanan değeri getirir

Detaylar için: [contracts/README.md](contracts/README.md)

## 🏗 Proje Yapısı

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

## 🔧 Geliştirme

### Backend'de Değişiklik Yapma
```bash
cd backend
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### Frontend'de Değişiklik Yapma
```bash
cd frontend
npm start  # Hot reload aktif
```

### Docker ile Development
```bash
# Container'ları yeniden build et
docker-compose up --build

# Sadece backend'i restart et
docker-compose restart backend

# Log'ları izle
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🧪 Test

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

## 🐛 Sorun Giderme

### Freighter bağlanamıyor
- Freighter extension'ının güncel olduğundan emin olun
- Testnet'te olduğunuzu kontrol edin
- Tarayıcı console'unda hata mesajlarını inceleyin

### Docker build hataları
```bash
# Cache'i temizle ve yeniden build et
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### CORS hataları
- Backend `.env` dosyasında `CORS_ALLOWED_ORIGINS` ayarını kontrol edin
- Frontend URL'inin listeye eklendiğinden emin olun

### Port zaten kullanımda
```bash
# Portları değiştirin (docker-compose.yml)
ports:
  - "8001:8000"  # Backend
  - "3001:80"    # Frontend
```

## 🆘 Freighter Extension Sorunları

**SORUN:** Freighter bulunamıyor hatası alıyorsanız:

### Hızlı Çözüm:
1. **Extension kontrol aracını kullanın:** `http://YOUR_IP:3000/extension-check.html`
2. **Hard refresh yapın:** `Ctrl+Shift+R` (Windows/Linux) veya `Cmd+Shift+R` (Mac)
3. **Freighter'ı pin'leyin:** Tarayıcı toolbar'ında görünür olmalı
4. **Site access:** chrome://extensions → Freighter → "On all sites"

### Detaylı Rehber:
- **URGENT_FIX.md** - Acil sorun giderme kılavuzu
- **FREIGHTER_FIX.md** - Kapsamlı troubleshooting

### Test Sayfaları:
- **Ana Sayfa:** `http://YOUR_IP:3000/`
- **Extension Kontrol:** `http://YOUR_IP:3000/extension-check.html`
- **Debug Sayfası:** `http://YOUR_IP:3000/debug.html`

## 📚 Kaynaklar

- [Stellar Documentation](https://developers.stellar.org/)
- [Soroban Documentation](https://soroban.stellar.org/docs)
- [Freighter Wallet](https://www.freighter.app/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altındadır.

## 👨‍💻 Geliştirici

Sorularınız için issue açabilirsiniz.

---

**Not**: Bu uygulama testnet üzerinde çalışmaktadır. Production'a geçmeden önce:
- Secret key'leri değiştirin
- DEBUG=False yapın
- HTTPS kullanın
- Security best practices uygulayın
- Rate limiting ekleyin

Stellar ile mutlu kodlamalar! 🚀✨
