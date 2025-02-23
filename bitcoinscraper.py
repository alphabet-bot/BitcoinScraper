import ecdsa
import hashlib
import base58
import requests

def generate_seed():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    seed = private_key.to_string()
    return seed

def bitcoin_address_from_seed(seed):
    private_key = ecdsa.SigningKey.from_string(seed, curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key().to_string()
    public_key_hash = hashlib.sha256(public_key).digest()
    ripemd160_hash = hashlib.new('ripemd160', public_key_hash).digest()
    bitcoin_address = base58.b58encode_check(b'\x00' + ripemd160_hash)
    return bitcoin_address

def check_balance(address):
    url = f"https://blockchain.info/q/addressbalance/{address}"
    response = requests.get(url)
    if response.status_code == 200:
        balance = int(response.text)
        return balance / 1e8  # Convert satoshis to BTC
    else:
        return None

def save_seeds_to_file(seeds_with_balances, filename):
    with open(filename, 'w') as file:
        for seed, address, balance in seeds_with_balances:
            file.write(f"Seed: {seed.hex()}\n")
            file.write(f"Address: {address.decode()}\n")
            file.write(f"Balance: {balance} BTC\n")
            file.write("------------------------\n")

def main():
    num_seeds = int(input("Enter the number of seeds to generate: "))
    seeds_with_balances = []
    for i in range(num_seeds):
        seed = generate_seed()
        address = bitcoin_address_from_seed(seed)
        balance = check_balance(address.decode())
        if balance is not None and balance > 0:
            print(f"Seed {i+1}: {seed.hex()}")
            print(f"Address: {address.decode()}")
            print(f"Balance: {balance} BTC")
            print("------------------------")
            seeds_with_balances.append((seed, address, balance))
        else:
            print(f"No balance found for seed {i+1}")
    
    if seeds_with_balances:
        filename = input("Enter a filename to save the seeds with balances (default: 'seeds_with_balances.txt'): ")
        if not filename:
            filename = 'seeds_with_balances.txt'
        save_seeds_to_file(seeds_with_balances, filename)
        print(f"Seeds with balances saved to '{filename}'")

if __name__ == "__main__":
    main()
