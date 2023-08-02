from abi import I0K_SWAP_APPROVE, I0K_SPENDER
from starknet_py.contract import Contract

async def I0K_approve(contract_address, account, amount):

    contract = Contract(
        address=contract_address,
        abi=I0K_SWAP_APPROVE,
        provider=account,
    )

    invocation = await contract.functions["approve"].invoke(
        I0K_SPENDER, amount, auto_estimate=True
    )

    await invocation.wait_for_acceptance()