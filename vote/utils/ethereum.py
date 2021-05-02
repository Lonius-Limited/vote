from web3 import Web3
import uuid
import json
import frappe
import time

# w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/32ed9238d7784cd2a1d35e5bda567a37'))

w3 = Web3(Web3.HTTPProvider('http://176.58.127.109:8545'))

abi = """[
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Increment",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string[]",
				"name": "value",
				"type": "string[]"
			}
		],
		"name": "Vote",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "vote",
				"type": "string"
			}
		],
		"name": "castVote",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getVotesCast",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]"""

# addr = '0x3A2DC3E0317FA95d1E01f222Cb18C22Fca13F24f'

addr = '0x0e605bB3b70717Df1A2bef3aA3089e91230842c2'
contract = w3.eth.contract(address=addr, abi=abi)


def create_wallet():

	acc = w3.eth.account.create(str(uuid.uuid4().hex))
	return {'private_key': acc.privateKey.hex(), 'public_key':acc.address}

def load_wallet(pubKey, amount):

	return True


def log_casted_vote(data, privKey, pubKey):
    _w3 = w3
    nonce = w3.eth.get_transaction_count(pubKey)
    _w3.eth.account.from_key(privKey)
    
    tx = contract.functions.castVote(data
            ).buildTransaction({
                'gas': contract.functions.castVote(data).estimateGas(),
                'gasPrice': w3.toWei('1', 'gwei'),
                'nonce': nonce,
    })

    signed_tx = _w3.eth.account.sign_transaction(tx, private_key=privKey)

    tx_id = _w3.toHex(w3.keccak(signed_tx.rawTransaction))
    # print("tx_id: ", tx_id)
    # print("previous_state: - votes cast: ", (contract.functions.getVotesCast().call()))
    # print("previous_state: - vote count: ", contract.functions.getCount().call())
    res = _w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    return tx_id
    
privKey = '0x88493446687bb3ec38cd62ea85f46ea4a36e77e61bd41d1caff3bb58c5d2e1af'
pubKey = '0x8f7B5cE33bef6ddf5cCF7ad9FcE4F7E1bfBb8E9e'
    
def run(data):

    privKey = '0x88493446687bb3ec38cd62ea85f46ea4a36e77e61bd41d1caff3bb58c5d2e1af'
    pubKey = '0x8f7B5cE33bef6ddf5cCF7ad9FcE4F7E1bfBb8E9e'

    data = json.dumps(data)

    print(log_casted_vote(data, privKey, pubKey))

# for i in range(0,10):

# run({"data":{"x":"x"}})


def send_ethers(to, amount, nonce):
	privKey = '0x88493446687bb3ec38cd62ea85f46ea4a36e77e61bd41d1caff3bb58c5d2e1af'
	pubKey = '0x8f7B5cE33bef6ddf5cCF7ad9FcE4F7E1bfBb8E9e'
	transaction = {
		'to': to,
		'value': amount,
		'gas': 100000,
		'gasPrice': w3.toWei('1', 'gwei'),
		# 'nonce': w3.eth.get_transaction_count(pubKey),
		'nonce':nonce,
		'chainId': 4284
	}
	
	signed = w3.eth.account.sign_transaction(transaction, privKey)
	res = w3.eth.send_raw_transaction(signed.rawTransaction)
	return w3.toHex(w3.keccak(signed.rawTransaction))

# print(send_ethers("0x30A3d349b62caeE1824C08c23DcD1F0b20eBb5Fc", 400))




def get_tx(tx_id):
	return w3.eth.get_transaction(tx_id)

def get_tx_receipt(tx_id):
	return w3.eth.get_transaction_receipt(tx_id)


def get_votes_cast():
	return contract.functions.getVotesCast().call()

get_votes_cast_bc = get_votes_cast

# print(get_votes_cast_bc())


def ensure_all_users_have_wallets():
    c = frappe.get_all('Institution Member', fields=['public_key', 'name'])
    for i in c:
        if not(i['public_key']):
            w = create_wallet()
            frappe.db.set_value('Institution Member', i['name'], {
                'public_key': w['public_key'],
                'private_key': w['private_key']
    		})
    print("done creating wallets!")
    

def send_ethers_to_all_users(nonce):
    c = frappe.get_all('Institution Member', fields=['public_key', 'name'])
    nonce = nonce
    for i in c:
        print(send_ethers(i['public_key'], 2, nonce=nonce))
        nonce = nonce + 1
        time.sleep(1)
    
    