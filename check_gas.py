from web3 import Web3

def get_current_gas_price():
    try:
        # Connect to an Ethereum node using Web3
        w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))

        # Get the current gas price in GWEI
        gas_price_wei = w3.eth.gas_price
        gas_price_gwei = w3.from_wei(gas_price_wei, 'gwei')

        return round(gas_price_gwei, 0)
    except Exception as e:
        print("Error fetching gas price:", e)
        return None
