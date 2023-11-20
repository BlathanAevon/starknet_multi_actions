# starknet_multi_actions

**A simple script, to send emails through Dmail.ai, mint Starknet ID, Mint random NFT**

![Static Badge](https://img.shields.io/badge/Starknet-8A2BE2) ![Static Badge](https://img.shields.io/badge/Language-python-blue)

## Installation:

1. Clone the repository
```python
git clone https://github.com/BlathanAevon/starknet_multi_actions
```

3. Go to directory
```bash
cd starknet_multi_actions
```
4. Virtual Environment creation
```bash
python (or python3) -m venv venv
```
5. Activate the virtual environment
    - Windows
      ```bash
      venv/Scripts/activate
      ```
    - Linux and MacOS
      ```bash
      source venv\bin\activate
      ```
6. Install dependencies (modules)
```bash
pip install -r requirements.txt
```

## Settings:

Put wallets in `wallets.csv` file in format *ADDRESS*, *PRIVATE KEY*
In `settings.py` set timings

## Run the program
```bash
python main.py
```
