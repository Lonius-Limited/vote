from web3 import Web3
import uuid
w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/32ed9238d7784cd2a1d35e5bda567a37'))

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

addr = '0x3A2DC3E0317FA95d1E01f222Cb18C22Fca13F24f'

contract = w3.eth.contract(address=addr, abi=abi)


def create_wallet():

	acc = w3.eth.account.create(str(uuid.uuid4().hex))
	return dict(private_key=acc.privateKey.hex(), public_key=acc.address)
	# return {'private_key': acc.privateKey.hex(), 'public_key':acc.address}
	# sorry guy

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
    print("tx_id: ", tx_id)
    print("previous_state: - votes cast: ", (contract.functions.getVotesCast().call()))
    print("previous_state: - vote count: ", contract.functions.getCount().call())
    res = _w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    return tx_id

privKey = '0x88493446687bb3ec38cd62ea85f46ea4a36e77e61bd41d1caff3bb58c5d2e1af'
pubKey = '0x8f7B5cE33bef6ddf5cCF7ad9FcE4F7E1bfBb8E9e'

def get_votes_cast_bc():
	return contract.functions.getVotesCast().call()

def run():

    privKey = '0x88493446687bb3ec38cd62ea85f46ea4a36e77e61bd41d1caff3bb58c5d2e1af'
    pubKey = '0x8f7B5cE33bef6ddf5cCF7ad9FcE4F7E1bfBb8E9e'

    data = "{'data': [...some long transaction data], 'more': 'yes, more data'}"
    print(log_casted_vote(data, privKey, pubKey))

# run()
