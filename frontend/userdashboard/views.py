from django.shortcuts import render,HttpResponse


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


from web3 import Web3
from web3 import Web3, HTTPProvider
#Getting Latest Block Number


def test():
    #Public Key
    eth_public_key ='0x7064167411cF1af4f578A7A6F382b501c9f81369'
    eth_private_key ='12d4061a13e292f59a52a7cf6f2512ecca077773006fcb85d850b4aa6eb40e2d'
    file_path ='/Users/vrushangdesai/Desktop/blocks-frontend/backend/build/contracts/Election.json'
    contract_interface = load_from_json(file_path)
    contract = DeployContract(contract_interface['abi'],contract_interface['bytecode'],eth_public_key,eth_private_key)
    contract=contract.deploy()
    print(contract.functions.getCandidateName().call())
    return contract.functions.getCandidateName().call()
#####################################################################################################################################
#PLS IGNORE ABOVE CODE IT IS JUST FOR TESTING PURPOSES
# Create your views here.
def userdashboard(request):
    test_data=test()
    return HttpResponse('<strong>{}</strong>'.format(test_data))
