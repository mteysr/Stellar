#![no_std]
use soroban_sdk::{contract, contractimpl, symbol_short, vec, Env, Symbol, Vec, Address};

#[contract]
pub struct HelloContract;

#[contractimpl]
impl HelloContract {
    /// Returns a greeting message
    pub fn hello(env: Env, to: Symbol) -> Vec<Symbol> {
        vec![&env, symbol_short!("Hello"), to]
    }
    
    /// Store a value associated with an address
    pub fn store(env: Env, user: Address, value: u32) {
        env.storage().instance().set(&user, &value);
    }
    
    /// Retrieve the stored value for an address
    pub fn get(env: Env, user: Address) -> Option<u32> {
        env.storage().instance().get(&user)
    }
}

mod test;
