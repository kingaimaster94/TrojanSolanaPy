# import base58
# from solders.keypair import Keypair
from solathon import Client, Keypair, PublicKey, Transaction
from solathon.core.instructions import transfer
from solathon.utils import *
import csv


client = Client("https://api.devnet.solana.com")

def generateKeyPair():
    # account = Keypair()
    # privateKey = base58.b58encode(account.secret() + base58.b58decode(str(account.pubkey()))).decode('utf-8')
    # return account.pubkey(), account.secret(), privateKey
    new_account = Keypair()
    print(new_account.public_key)
    print(new_account.private_key)
    
    balance = client.get_balance("HGTGTnvisMt4pvcP3h3Z6LP732PewGqqgKY6UkLxB5qW")
    sol_balance = lamport_to_sol(balance)
    wallet_balance = str(sol_balance) + " SOL ($0.00)"
    
    return new_account.public_key, wallet_balance

def getWalletBalance(pubKey: PublicKey):
    balance = client.get_balance(pubKey)
    sol_balance = lamport_to_sol(balance)
    return sol_balance

def is_valid_token_address(pubKey: PublicKey):
    return True