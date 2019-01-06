from web3 import Web3
import json
class DeployContract:
    def __init__(self, abi, bin, public_key, private_key,provider='HTTP://127.0.0.1:7545'):
        provider = 'HTTP://127.0.0.1:7545'
        self.w3 = Web3(Web3.HTTPProvider(provider))
        self.abi = abi # Your contract ABI code
        self.bin = bin # Your contract ByteCode
        self.priv = private_key
        self.pub = public_key

    def deploy(self):
        instance = self.w3.eth.contract(abi=self.abi, bytecode=self.bin)
        tx_data = instance.constructor().__dict__.get('data_in_transaction')
        transaction = {
            'from': self.pub, # Only 'from' address, don't insert 'to' address
            'value': 0, # Add how many ethers you'll transfer during the deploy
            'gas': 2000000, #
            'gasPrice': self.w3.eth.gasPrice, # Get Gas Price
            'nonce': self.w3.eth.getTransactionCount(self.pub), # Get Nonce
            'data': tx_data # This is the data sent through the network
        }
        # Sign the transaction using private key
        signed = self.w3.eth.account.signTransaction(transaction, self.priv)
        #print(signed.rawTransaction)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        #Waiting For Transaction To Get Mined And Then Updating Contract Instance/Object With Contract Address

        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash.hex())
        print('Trasaction Hash :    ',tx_hash.hex())
        instance = self.w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=self.abi,
        bytecode=self.bin
        )


        return instance


def load_from_json(json_file_name: str):
    handle = open(json_file_name,'r')
    return json.loads(handle.read())
