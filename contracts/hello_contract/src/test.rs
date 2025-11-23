#![cfg(test)]

use super::*;
use soroban_sdk::{symbol_short, vec, Env, Address};

#[test]
fn test_hello() {
    let env = Env::default();
    let contract_id = env.register_contract(None, HelloContract);
    let client = HelloContractClient::new(&env, &contract_id);

    let words = client.hello(&symbol_short!("World"));
    assert_eq!(
        words,
        vec![&env, symbol_short!("Hello"), symbol_short!("World")]
    );
}

#[test]
fn test_store_and_get() {
    let env = Env::default();
    let contract_id = env.register_contract(None, HelloContract);
    let client = HelloContractClient::new(&env, &contract_id);

    let user = Address::generate(&env);
    let value: u32 = 42;

    // Store value
    client.store(&user, &value);

    // Retrieve value
    let result = client.get(&user);
    assert_eq!(result, Some(value));
}
