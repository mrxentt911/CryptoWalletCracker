import time
from web3 import Web3
from eth_account import Account
from mnemonic import Mnemonic

# Enable HD wallet support
Account.enable_unaudited_hdwallet_features()

# Infura setup (replace with your own project ID)
INFURA_PROJECT_ID = "d78462515c7d426f9630608bf6a41946"
INFURA_URL = f"https://mainnet.infura.io/v3/d78462515c7d426f9630608bf6a41946"

# Connect to Infura
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not w3.is_connected():
    raise Exception("Web3 connection failed. Check Infura URL or Internet.")

# Output file
OUTPUT_FILE = "wallets.txt"

def generate_wallet_and_check_balance():
    # Generate random mnemonic
    mnemo = Mnemonic("english")
    phrase = mnemo.generate(strength=128)  # 12 words

    # Derive wallet
    acct = Account.from_mnemonic(phrase, account_path="m/44'/60'/0'/0/0")
    address = acct.address

    # Check balance
    try:
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, "ether")
    except Exception as e:
        balance_eth = "Error"

    # Print to terminal
    print("="*30)
    print(f"Address:   {address}")
    print(f"Mnemonic:  {phrase}")
    print(f"Balance:   {balance_eth} ETH")

    # Save to file
    with open(OUTPUT_FILE, "a") as f:
        f.write("="*30 + "\n")
        f.write(f"Address:   {address}\n")
        f.write(f"Mnemonic:  {phrase}\n")
        f.write(f"Balance:   {balance_eth} ETH\n")

    return balance_eth

# Infinite loop
try:
    while True:
        generate_wallet_and_check_balance()
        time.sleep(1)  # Pause briefly between checks
except KeyboardInterrupt:
    print("\nScript stopped by user.")