from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
import asyncio
from tokens import *
from abi import *
from starknet_py.contract import Contract
import string
import random
from loguru import logger
import csv
import time


STARKNET_NODE = "https://starknet-mainnet.public.blastapi.io"

# How many messages to send on every acccount
MESSAGES_PER_ACCOUNT = 1


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


async def dmail_send_email(account):
    contract = Contract(
        address=0x0454F0BD015E730E5ADBB4F080B075FDBF55654FF41EE336203AA2E1AC4D4309,
        abi=DMAIL_TRANSACTION,
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

        for acc in accounts:
            tts = random.randint(40, 350)

            logger.info(f"Working on wallet: {hex(acc.address)}\n")
            if MESSAGES_PER_ACCOUNT > 1:
                for _ in range(MESSAGES_PER_ACCOUNT):
                    message_delay = random.randit(10, 60)
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
