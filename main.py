import warnings
from datetime import datetime, timezone
from web3 import Web3
import pandas as pd
import json
import time

warnings.simplefilter(action="ignore", category=FutureWarning)

# Contract address and ABI
contract_address = "0x0E3A8078EDD2021dadcdE733C6b4a86E51EE8f07"

with open("abi.json") as abi_file:
    data = abi_file.read()
abi = json.loads(data)

# Provider
rpc_mainnet = "https://bsc-dataseed.binance.org"
w3 = Web3(Web3.HTTPProvider(rpc_mainnet))

# Connect to contract
contract = w3.eth.contract(address=contract_address, abi=abi)

# Current epoch
current_epoch = contract.functions.currentEpoch().call()

lookback = 70
starting_epoch = current_epoch - lookback
columns = ["epoch", "start_timestamp", "lock_timestamp", "close_timestamp", "lock_price", "close_price",
           "total_amount", "bull_amount", "bear_amount", "bull_ratio", "bear_ratio", "oracle_called"]
df = pd.DataFrame(columns=columns)

count = 0
for e in range(0, lookback):
    time.sleep(1)
    starting_epoch += 1
    count += 1
    print(starting_epoch, count)

    current_rounds_list = contract.functions.rounds(starting_epoch).call()

    # Name items
    epoch = current_rounds_list[0]
    start_timestamp = current_rounds_list[1]
    lock_timestamp = current_rounds_list[2]
    close_timestamp = current_rounds_list[3]
    lock_price = current_rounds_list[4]
    close_price = current_rounds_list[5]
    total_amount = current_rounds_list[8]
    bull_amount = current_rounds_list[9]
    bear_amount = current_rounds_list[10]
    oracle_called = current_rounds_list[13]

    # Calculate ratio
    total_amount_in_human = round(float(Web3.from_wei(total_amount, "ether")), 5)
    bear_amount_in_human = round(float(Web3.from_wei(bear_amount, "ether")), 5)
    bull_amount_in_human = round(float(Web3.from_wei(bull_amount, "ether")), 5)

    # Ratios
    if bear_amount_in_human != 0 and bull_amount_in_human != 0:
        bull_ratio = round(bull_amount_in_human / bear_amount_in_human, 2)
        bear_ratio = round(bear_amount_in_human / bull_amount_in_human, 2)
    else:
        bull_ratio = 0
        bear_ratio = 0

    row_dict = {
        "epoch": epoch,
        "start_timestamp": start_timestamp,
        "lock_timestamp": lock_timestamp,
        "close_timestamp": close_timestamp,
        "lock_price": lock_price,
        "close_price": close_price,
        "total_amount": total_amount_in_human,
        "bull_amount": bull_amount_in_human,
        "bear_amount": bear_amount_in_human,
        "bull_ratio": bull_ratio,
        "bear_ratio": bear_ratio,
        "oracle_called": oracle_called,
    }

    try:
        df.loc[len(df)] = row_dict
        df.to_csv("predictions.csv", index=False)
    except Exception as e:
        print("Error occurred:", str(e))

