from django.shortcuts import render,HttpResponse


from web3 import Web3
import json
class DeployContract:
    def __init__(self, abi, bin, public_key, private_key,provider='HTTP://127.0.0.1:8545'):
        provider = 'HTTP://127.0.0.1:8545'
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
    eth_public_key ='0x1c534c5385828a5D9f394E5BAF53506F0b900a03'
    eth_private_key ='f46c2fca55b266769cb1dde8e4635d1df758cf828c338f93560fdab5cf19c955'
    file_path ='/Users/vrushangdesai/Desktop/blocks-frontend/backend/build/contracts/Admin.json'
    contract_interface = load_from_json(file_path)
    contract = DeployContract(contract_interface['abi'],contract_interface['bytecode'],eth_public_key,eth_private_key)
    contract=contract.deploy()
    data = dict()
    data['admin_address']=contract.functions.getAdminAddress().call()

    print(contract.functions.getAdminAddress().call())
    return data

#####################################################################################################################################
#PLS IGNORE ABOVE CODE IT IS JUST FOR TESTING PURPOSES
# Create your views here.
def userdashboard(request):
    test_data=test()
    return render(request, 'userdashboard/set_admin.html', {
        'Address': test_data['admin_address']})
