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

def save_seeds_to_file(seeds_with_balances):
    # Define the filename as 'seeds.txt'
    filename = "seeds.txt"
    
    # Open the file in write mode
    with open(filename, 'w') as file:
        for seed, address, balance in seeds_with_balances:
            # Write the seed, address, and balance to the file
            file.write(f"Seed: {seed.hex()}\n")
            file.write(f"Address: {address.decode()}\n")
            file.write(f"Balance: {balance} BTC\n")
            file.write("------------------------\n")

# Example usage:
# Assume seeds_with_balances is a list of tuples: (seed, address, balance)
# Example (seed, address, balance) data:
seeds_with_balances = [
    (b'\x12\x34\x56\x78\x90\xab\xcd\xef', b'1A1zP1eP5QWck1deuVsZgV6A5VHGzHqj79Y', 0.5),
    (b'\x87\x65\x43\x21\x00\x12\x34\x56', b'1Q2w3E4r5T6y7U8i9O0p9A8l7J7w1P2b3L', 0.8)
]

# Save the seeds and associated data to the file 'seeds.txt'
save_seeds_to_file(seeds_with_balances)
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
