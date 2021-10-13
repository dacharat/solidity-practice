from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

# import solcx
# solcx.install_solc('0.8.9')
load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

# Compile Our Solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.8.9"
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
# chain_id = 1337 // for local blockchain
# my_address = "0xD3E3e0007aA1557b71DdDc7b7e6f46cFF9ba1A71"

w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
my_address = "0xC8D95Aed98256d23b16539c385524c8879B4A416"
chain_id = 4  # for rinkeby
private_key = os.getenv("PRIVATE_KEY")
# print(private_key)

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)
# 1. Build a traansaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
# print(transaction)

# 2, Sign a transaction
signed_txn = w3.eth.account.sign_transaction(
    transaction, private_key=private_key)
print("Deploying Contract!")

# 3. Send a transaciton
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")
# https://rinkeby.etherscan.io/address/0x79737fe5723cac74cf91052768300946cd25f59d

#  ====================================
# Working with deployed Contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)
tx_greeting_hash = w3.eth.send_raw_transaction(
    signed_greeting_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())
