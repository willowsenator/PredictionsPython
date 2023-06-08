import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

from datetime import datetime, timezone
from web3 import Web3
import pandas as pd
import json
import time

# Contract address and ABI
contract_address = "0x18B2A687610328590Bc8F2e5fEdDe3b582A49cdA"

with open("abi.json") as abi_file:
    data = abi_file.read()
abi = json.loads(data)

# Provider
rpc_mainnet = "https://bsc-dataseed.binance.org"
w3 = Web3(Web3.HTTPProvider(rpc_mainnet))

# Connect to contract
contract = w3.eth.contract(address=contract_address, abi=abi)
print(contract)
