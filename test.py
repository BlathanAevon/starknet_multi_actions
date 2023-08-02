class StarkNetAccount:
    client = FullNodeClient(STARKNET_NODE)

    def __init__(self, address, private_key) -> None:
        self.account = Account(
            client=self.client,
            address=address,
            key_pair=KeyPair.from_private_key(key=private_key),
            chain=StarknetChainId.MAINNET,
        )

    async def get_account_gas_balance(self):
        eth_token_address = (
            0x049D36570D4E46F48E99674BD3FCC84644DDD6B96F7C741B1562B82F9E004DC7
        )

        # Create a call to function "balanceOf" at address `eth_token_address`
        call = Call(
            to_addr=eth_token_address,
            selector=get_selector_from_name("balanceOf"),
            calldata=[self.account.address],
        )
        # Pass the created call to Client.call_contract

        account_balance = await self.account.client.call_contract(call)
        return round(account_balance[0] / 10**18, 4)

    async def get_account_tokens_balance(self, address: any):
        call = Call(
            to_addr=address,
            selector=get_selector_from_name("balanceOf"),
            calldata=[self.account.address],
        )
        # Pass the created call to Client.call_contract

        account_balance = await self.account.client.call_contract(call)
        return round(account_balance[0] / 10**6, 5)
