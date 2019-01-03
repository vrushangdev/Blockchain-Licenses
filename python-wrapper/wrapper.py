from web3 import Web3
from ethutils import DeployContract
from web3 import Web3, HTTPProvider
import ethutils
#Getting Latest Block Number


def test():
    #Public Key
    eth_public_key ='0x7064167411cF1af4f578A7A6F382b501c9f81369'
    eth_private_key ='12d4061a13e292f59a52a7cf6f2512ecca077773006fcb85d850b4aa6eb40e2d'
    file_path ='/Users/vrushangdesai/Desktop/blocks-frontend/backend/build/contracts/Election.json'
    contract_interface = ethutils.load_from_json(file_path)
    contract = DeployContract(contract_interface['abi'],contract_interface['bytecode'],eth_public_key,eth_private_key)
    contract=contract.deploy()
    print(contract.functions.getCandidateName().call())
    return contract.functions.getCandidateName().call()
