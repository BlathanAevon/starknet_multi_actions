from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from dmail_abi import DMAIL_TRANSACTION_ABI
from starknet_py.contract import Contract
from loguru import logger
from settings import ACCEPTABLE_GWEI, MESSAGES_PER_ACCOUNT_FROM, MESSAGES_PER_ACCOUNT_TO, M_DELAY_FROM, M_DELAY_TO, DELAY_FROM, DELAY_TO, STARKNET_NODE
import asyncio
import string
import random
import csv
import time
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


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


async def dmail_send_email(account):
    contract = Contract(
        address=0x0454F0BD015E730E5ADBB4F080B075FDBF55654FF41EE336203AA2E1AC4D4309,
        abi=DMAIL_TRANSACTION_ABI,
        provider=account,
    )

    logger.info("Generating random email and message...")
    random_email = f"{get_random_string(6)}".encode()
    random_message = get_random_string(3).encode()

    logger.info("Assembling Transaction...")
    invocation = await contract.functions["transaction"].invoke(
        random_email.hex(), random_message.hex(), auto_estimate=True
    )

    logger.info("Waiting for transaction confirmation on blockchain...")
    await invocation.wait_for_acceptance()
    logger.success(f"Transaction done!")


async def main():
    accounts = []
    with open("wallets.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            if str(row[1]).startswith("0x"):
                private_key = int(row[1], 16)
            else:
                private_key = int(row[1])

            address = row[0]
            starknet_account = Account(
                client=FullNodeClient(STARKNET_NODE),
                # Сюда адресс нашего кошелька
                address=address,
                key_pair=KeyPair.from_private_key(
                    # Сюда приватник
                    key=private_key
                ),
                chain=StarknetChainId.MAINNET,
            )

            accounts.append(starknet_account)

        random.shuffle(accounts)

        if len(accounts) < 1:
            logger.error("You forgot to add wallets in wallets.csv!")

        for acc in accounts:
            while True:
                gwei = get_current_gas_price()
                if gwei > ACCEPTABLE_GWEI:
                    logger.error(
                        f"Gwei is {gwei} - too high! Waiting for lower gas...\n"
                    )
                    time.sleep(random.randint(5, 10))
                else:
                    logger.success("Gas is acceptable for work")
                    break

            tts = random.randint(DELAY_FROM, DELAY_TO)

            logger.info(f"Working on wallet: {hex(acc.address)}\n")
            if MESSAGES_PER_ACCOUNT_FROM > 1:
                for _ in range(random.randint(MESSAGES_PER_ACCOUNT_FROM, MESSAGES_PER_ACCOUNT_TO)):
                    message_delay = random.randit(M_DELAY_FROM, M_DELAY_TO)
                    await dmail_send_email(acc)
                    logger.opt(colors=True).info(
                        f"<yellow>Waiting {message_delay} before next message</yellow>"
                    )
                    time.sleep(message_delay)
            else:
                await dmail_send_email(acc)

            logger.info(f"Sleeping {tts} seconds...\n")
            time.sleep(tts)


asyncio.run(main())
