STARKNET_NODE = "https://starknet-mainnet.public.blastapi.io"

# How many messages to send on every acccount
MESSAGES_PER_ACCOUNT_FROM = 1
MESSAGES_PER_ACCOUNT_TO = 1

# Delay between accounts
DELAY_FROM = 40
DELAY_TO = 300

# Delay between messages
M_DELAY_FROM = 10
M_DELAY_TO = 60

# Delay between modules
MOD_DELAY_FROM = 20
MOD_DELAY_TO = 80

# Gas value at which script is acceptable to work
ACCEPTABLE_GWEI = 17

# True if you want to randomize moudules execution
RANDOMIZE_MODULES = True

# Available modules: dmail_send_email, mint_starknet_id
MODULES = ["dmail_send_email", "mint_starknet_id"]
