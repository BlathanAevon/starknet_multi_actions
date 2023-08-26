from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from dmail_abi import DMAIL_TRANSACTION_ABI
from public_mint_abi import PUBLIC_MINT_ABI
from id_minter_abi import MINT_ID_ABI
from starknet_py.contract import Contract
from loguru import logger
from settings import (
    ACCEPTABLE_GWEI,
    MESSAGES_PER_ACCOUNT_FROM,
    MESSAGES_PER_ACCOUNT_TO,
    M_DELAY_FROM,
    M_DELAY_TO,
    DELAY_FROM,
    DELAY_TO,
    STARKNET_NODE,
    MODULES,
    RANDOMIZE_MODULES,
    MOD_DELAY_FROM,
    MOD_DELAY_TO,
)
import asyncio
import string
import random
import csv
import time
from web3 import Web3


def get_current_gas_price():
    try:
        # Connect to an Ethereum node using Web3
        w3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/eth"))

        # Get the current gas price in GWEI
        gas_price_wei = w3.eth.gas_price
        gas_price_gwei = w3.from_wei(gas_price_wei, "gwei")

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


async def mint_starknet_id(account):
    contract = Contract(
        address=0x05DBDEDC203E92749E2E746E2D40A768D966BD243DF04A6B712E222BC040A9AF,
        abi=MINT_ID_ABI,
        provider=account,
    )

    logger.info("Assembling Transaction...")
    invocation = await contract.functions["mint"].invoke(
        random.randint(400000, 20000000), auto_estimate=True
    )

    logger.info("Minting an ID...")
    await invocation.wait_for_acceptance()
    logger.success(f"Transaction done!")


async def mint_public_nft(account):
    contract = Contract(
        address=0x060582DF2CD4AD2C988B11FDEDE5C43F56A432E895DF255CCD1AF129160044B8,
        abi=PUBLIC_MINT_ABI,
        provider=account,
    )

    logger.info("Assembling Transaction...")
    invocation = await contract.functions["publicMint"].invoke(
        account.address, auto_estimate=True
    )

    logger.info("Minting an Public NFT...")
    await invocation.wait_for_acceptance()
    logger.success(f"Transaction done!")


async def main():
    accounts = []
    with open("wallets.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            if str(row[1].strip()).startswith("0x"):
                private_key = int(row[1].strip(), 16)
            else:
                private_key = int(row[1].strip())

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
            # await myswap_swap(acc, "USDT")
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

            logger.info(f"Working on wallet: {hex(acc.address)}\n")

            if RANDOMIZE_MODULES:
                random.shuffle(MODULES)
                logger.warning("Modules randomized!")

            for module in MODULES:
                if module == "mint_starknet_id":
                    await mint_starknet_id(acc)
                elif module == "dmail_send_email":
                    if MESSAGES_PER_ACCOUNT_FROM > 1:
                        for _ in range(
                            random.randint(
                                MESSAGES_PER_ACCOUNT_FROM, MESSAGES_PER_ACCOUNT_TO
                            )
                        ):
                            message_delay = random.randit(M_DELAY_FROM, M_DELAY_TO)
                            await dmail_send_email(acc)
                            logger.opt(colors=True).info(
                                f"<yellow>Waiting {message_delay} before next message</yellow>"
                            )
                            time.sleep(message_delay)
                    else:
                        await dmail_send_email(acc)
                elif module == "mint_public_nft":
                    await mint_public_nft(acc)
                else:
                    logger.error("MODULE NAME ERROR, CHECK THE CODE!")

                mod_tts = random.randint(MOD_DELAY_FROM, MOD_DELAY_TO)
                logger.warning(f"Sleeping {mod_tts} seconds between modules...\n")
                time.sleep(mod_tts)

            tts = random.randint(DELAY_FROM, DELAY_TO)
            logger.info(f"Sleeping {tts} seconds before next wallet...\n")
            time.sleep(tts)


asyncio.run(main())
