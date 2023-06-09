import json

from web3 import Web3

# Contract address and ABI
contract_address = "0x0E3A8078EDD2021dadcdE733C6b4a86E51EE8f07"

with open("abi.json") as abi_file:
    data = abi_file.read()
abi = json.loads(data)

# Provider
account_mainnet = ""
pk_account = ""
rpc_mainnet = "https://bsc-dataseed.binance.org"
w3 = Web3(Web3.HTTPProvider(rpc_mainnet))

# Connect to contract
contract = w3.eth.contract(address=contract_address, abi=abi)

# Current epoch
current_epoch = contract.functions.currentEpoch().call()


# Send tx
def send_tx(side):
    chain_id = 56
    gas = 300000
    gas_price = Web3.to_wei("5.5", "gwei")
    send_bnb = 0.001
    amount = Web3.to_wei(send_bnb, "ether")

    # Nonce
    nonce = w3.eth.get_transaction_count(account_mainnet)

    # Build Tx BULL
    if side == "bull":
        tx_build = contract.functions.betBull(current_epoch, amount).buildTransaction({
            "chainId": chain_id,
            "gas": gas,
            "value": amount,
            "gasPrice": gas_price,
            "nonce": nonce
        })

    # Build Tx BEAR
    else:
        tx_build = contract.functions.betBear(current_epoch, amount).buildTransaction({
            "chainId": chain_id,
            "gas": gas,
            "value": amount,
            "gasPrice": gas_price,
            "nonce": nonce
        })

    # Sign Tx
    tx_signed = w3.eth.account.sign_transaction(tx_build, pk_account)

    # Send Tx
    sent_tx = w3.eth.send_raw_transaction(tx_signed.rawTransaction)
