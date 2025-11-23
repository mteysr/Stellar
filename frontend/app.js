// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api' 
    : '/api';

// DOM Elements
const loginScreen = document.getElementById('loginScreen');
const dashboardScreen = document.getElementById('dashboardScreen');
const connectBtn = document.getElementById('connectBtn');
const logoutBtn = document.getElementById('logoutBtn');
const loadingMsg = document.getElementById('loadingMsg');
const errorMsg = document.getElementById('errorMsg');
const publicKeyEl = document.getElementById('publicKey');
const shortAddressEl = document.getElementById('shortAddress');
const installNotice = document.getElementById('installNotice');

// State
let walletData = null;
let freighterAPI = null;

// Utility Functions
function showError(message) {
    errorMsg.textContent = message;
    errorMsg.classList.remove('hidden');
}

function hideError() {
    errorMsg.classList.add('hidden');
}

function showLoading() {
    loadingMsg.classList.remove('hidden');
    connectBtn.disabled = true;
}

function hideLoading() {
    loadingMsg.classList.add('hidden');
    connectBtn.disabled = false;
}

function shortenAddress(address) {
    if (!address) return '';
    return `${address.substring(0, 8)}...${address.substring(address.length - 8)}`;
}

function showDashboard(data) {
    publicKeyEl.textContent = data.publicKey;
    shortAddressEl.textContent = shortenAddress(data.publicKey);
    loginScreen.classList.add('hidden');
    dashboardScreen.classList.remove('hidden');
}

function showLogin() {
    dashboardScreen.classList.add('hidden');
    loginScreen.classList.remove('hidden');
}

// API Functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error || 'API request failed');
    }

    return result;
}

// Freighter Functions with Library Support
async function initializeFreighterAPI() {
    console.log('🔍 Initializing Freighter API...');
    
    // Method 1: Library API (freighterApi from CDN)
    if (typeof freighterApi !== 'undefined') {
        console.log('✅ Method 1: Freighter Library API found');
        freighterAPI = freighterApi;
        return true;
    }
    
    // Method 2: Extension injected API
    if (window.freighter) {
        console.log('✅ Method 2: window.freighter found');
        freighterAPI = window.freighter;
        return true;
    }
    
    // Method 3: window.stellar.freighter
    if (window.stellar?.freighter) {
        console.log('✅ Method 3: window.stellar.freighter found');
        freighterAPI = window.stellar.freighter;
        return true;
    }
    
    // Method 4: Wait for extension to load (5 seconds)
    console.log('⏳ Waiting for Freighter extension to inject...');
    return new Promise((resolve) => {
        let attempts = 0;
        const maxAttempts = 50;
        
        const checkInterval = setInterval(() => {
            attempts++;
            
            if (typeof freighterApi !== 'undefined') {
                console.log(`✅ Freighter Library loaded after ${attempts} attempts`);
                freighterAPI = freighterApi;
                clearInterval(checkInterval);
                resolve(true);
            } else if (window.freighter || window.stellar?.freighter) {
                console.log(`✅ Freighter Extension loaded after ${attempts} attempts`);
                freighterAPI = window.freighter || window.stellar.freighter;
                clearInterval(checkInterval);
                resolve(true);
            } else if (attempts >= maxAttempts) {
                console.error('❌ Freighter not found after 5 seconds');
                clearInterval(checkInterval);
                resolve(false);
            }
        }, 100);
    });
}

async function connectToFreighter() {
    if (!freighterAPI) {
        throw new Error('Freighter API not initialized');
    }

    try {
        console.log('🔌 Connecting to Freighter...');
        
        // Check if already connected
        const isAllowed = await freighterAPI.isAllowed();
        console.log('isAllowed:', isAllowed);
        
        if (!isAllowed) {
            console.log('🔐 Requesting access...');
            await freighterAPI.setAllowed();
        }

        // Get public key
        console.log('🔑 Getting public key...');
        const publicKey = await freighterAPI.getPublicKey();
        
        if (!publicKey) {
            throw new Error('Failed to retrieve public key from Freighter');
        }

        console.log('✅ Public key retrieved:', publicKey);
        return publicKey;
    } catch (error) {
        console.error('❌ Freighter connection error:', error);
        if (error.message && error.message.includes('denied')) {
            throw new Error('Access to Freighter was denied. Please approve the connection.');
        }
        throw error;
    }
}

async function signWithFreighter(message) {
    if (!freighterAPI) {
        throw new Error('Freighter API not initialized');
    }

    try {
        console.log('✍️ Signing message...');
        const signedMessage = await freighterAPI.signMessage(message);
        
        if (!signedMessage) {
            throw new Error('Failed to sign message');
        }

        console.log('✅ Message signed');
        return signedMessage;
    } catch (error) {
        console.error('❌ Signing error:', error);
        if (error.message && error.message.includes('denied')) {
            throw new Error('Message signing was denied. Please approve in Freighter.');
        }
        throw error;
    }
}

// Main Authentication Flow
async function handleConnect() {
    hideError();
    showLoading();

    try {
        // Step 1: Ensure Freighter API is initialized
        if (!freighterAPI) {
            console.log('Freighter API not initialized, trying now...');
            const initialized = await initializeFreighterAPI();
            if (!initialized) {
                throw new Error('Freighter wallet not found. Please install it from freighter.app');
            }
        }

        // Step 2: Connect to Freighter and get public key
        console.log('Step 2: Connecting to Freighter...');
        const publicKey = await connectToFreighter();
        console.log('Connected! Public key:', publicKey);

        // Step 3: Get challenge from backend
        console.log('Step 3: Getting challenge from backend...');
        const authResponse = await apiCall('/auth/connect/', 'POST', { public_key: publicKey });
        console.log('Challenge received');

        // Step 4: Sign the challenge
        console.log('Step 4: Signing challenge...');
        const signature = await signWithFreighter(authResponse.challenge);
        console.log('Challenge signed');

        // Step 5: Verify signature with backend
        console.log('Step 5: Verifying signature...');
        const verifyResponse = await apiCall('/auth/verify/', 'POST', {
            public_key: publicKey,
            signature: signature,
            challenge: authResponse.challenge
        });
        console.log('Authentication successful!');

        // Step 6: Save to localStorage and show dashboard
        walletData = {
            publicKey: publicKey,
            wallet: verifyResponse.wallet,
            sessionKey: verifyResponse.session_key
        };
        localStorage.setItem('walletData', JSON.stringify(walletData));
        
        showDashboard(walletData);

    } catch (error) {
        console.error('Authentication error:', error);
        showError(error.message || 'Failed to connect to Freighter wallet');
    } finally {
        hideLoading();
    }
}

async function handleLogout() {
    try {
        await apiCall('/auth/logout/', 'POST');
    } catch (error) {
        console.error('Logout error:', error);
    }
    
    walletData = null;
    localStorage.removeItem('walletData');
    showLogin();
}

// Initialize App
async function init() {
    console.log('🚀 App initializing...');
    
    // Initialize Freighter API
    const freighterAvailable = await initializeFreighterAPI();
    
    if (!freighterAvailable) {
        console.error('❌ Freighter not available');
        showError('Freighter wallet not found. Please install it from freighter.app');
        installNotice.style.display = 'block';
        return;
    } else {
        console.log('✅ Freighter API ready!');
        installNotice.style.display = 'none';
        hideError();
    }
    
    // Check if user is already authenticated
    const storedData = localStorage.getItem('walletData');
    if (storedData) {
        try {
            walletData = JSON.parse(storedData);
            
            // Verify session is still valid
            const walletInfo = await apiCall('/auth/wallet/');
            showDashboard(walletData);
        } catch (error) {
            console.log('Session expired');
            localStorage.removeItem('walletData');
            showLogin();
        }
    } else {
        showLogin();
    }

    // Event Listeners
    connectBtn.addEventListener('click', handleConnect);
    logoutBtn.addEventListener('click', handleLogout);
}

// Start app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('DOM loaded, waiting 1 second for extensions...');
        setTimeout(init, 1000);
    });
} else {
    console.log('DOM already loaded, waiting 1 second for extensions...');
    setTimeout(init, 1000);
}
