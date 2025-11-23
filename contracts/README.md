# Stellar Soroban Smart Contract

This directory contains example Stellar Soroban smart contracts.

## Hello Contract

A simple smart contract that demonstrates:
- Greeting functionality
- Storage operations (store and retrieve values)
- Basic Soroban SDK usage

## Building the Contract

### Prerequisites
- Rust and Cargo
- Soroban CLI

### Install Soroban CLI
```bash
cargo install --locked soroban-cli
```

### Build the Contract
```bash
cd hello_contract
soroban contract build
```

### Optimize the Contract (Optional)
```bash
soroban contract optimize --wasm target/wasm32-unknown-unknown/release/hello_contract.wasm
```

### Deploy to Testnet
```bash
# Configure network
soroban network add testnet \
  --rpc-url https://soroban-testnet.stellar.org:443 \
  --network-passphrase "Test SDF Network ; September 2015"

# Create identity
soroban keys generate alice --network testnet

# Deploy contract
soroban contract deploy \
  --wasm target/wasm32-unknown-unknown/release/hello_contract.wasm \
  --source alice \
  --network testnet
```

### Invoke Contract Functions
```bash
# Call hello function
soroban contract invoke \
  --id CONTRACT_ID \
  --source alice \
  --network testnet \
  -- \
  hello \
  --to World

# Store a value
soroban contract invoke \
  --id CONTRACT_ID \
  --source alice \
  --network testnet \
  -- \
  store \
  --user GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  --value 42

# Get stored value
soroban contract invoke \
  --id CONTRACT_ID \
  --source alice \
  --network testnet \
  -- \
  get \
  --user GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## Contract Functions

### `hello(to: Symbol) -> Vec<Symbol>`
Returns a greeting message combining "Hello" with the provided symbol.

### `store(user: Address, value: u32)`
Stores a u32 value associated with a user's address.

### `get(user: Address) -> Option<u32>`
Retrieves the stored value for a given user address.

## Testing
```bash
cd hello_contract
cargo test
```
