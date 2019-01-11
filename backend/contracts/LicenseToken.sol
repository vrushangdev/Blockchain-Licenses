pragma solidity >=0.4.21 <0.6.0;
//admin permission contract
contract Admin {
  //admin address variable
  address admin ;
  //admin contract constructor to set admin as person who executes or deploys smart contract using msg.sender function
  constructor() public{
    admin = msg.sender;
  }
//setting acess modifier to restrict other addresses from acessing criticial functions .
  modifier onlyAdmin()
{
    require(
        msg.sender == admin,
        "Sender not authorized."
    );
    // Do not forget the "_;"! It will
    // be replaced by the actual function
    // body when the modifier is used.
    _;
}
//Change Admin Address Or Ownership
  function changeAdmin(address _newAdmin) onlyAdmin() public {
    admin = _newAdmin;

  }
  //function to get admin retrieve current admin address from blockchain
  function getAdminAddress() public view returns (address) {
    return admin;

  }

}
//License Token Contract Start's Here


contract LicenseToken is Admin {
//Using Enum To Defing Our Custom DataType's Like LicenseType ANd LicenseState
  enum LicenseType {WIN,MAC,LINUX}
  enum LicenseState {ACTIVE,INACTIVE,EXPIRED}

  struct LicenseAttributes {
    LicenseType licenseType;
    LicenseState state;
    uint registeredOn;
    uint expiresOn;
    string device_hardware_id;

  }
//declaring list of our license tokens with attributes
  LicenseAttributes[] license;
//setting dictionary to store license data
mapping (uint256 => address) public licenseNumberToClient;
mapping (address => uint256) ownershipLicenseCount;
mapping (uint256 => address) public licenseNumberToBeApproved;

//events

event LicenseGiven(address account,uint256 licenseNumber);
event Transfer(address _from,address _to,uint256 _licenseNumber);
event Approval(address admin,address approved,uint256 licenseNumber);
//contructor
constructor() public {




}
//started to implement basic function's
//this function will return us total number of licenses

  function totalLicenses() public view returns (uint256 total) {
    return license.length;
  }
  function balanceOf(address _account) public view returns (uint256 balance) {

      return  ownershipLicenseCount[_account];

  }
  function ownerOf(uint256 _license_number) public view returns (address owner) {

    owner = licenseNumberToClient[_license_number];
    //.i.e owner might not be burn address : 0x0000000000000000000000000000000000000000 else everyone will get free license's
    require(owner != address(0));
    return  owner;

  }

  function transferFrom(address _from,address _to,uint256 _license_number)onlyAdmin() public {
    //neither burn address
    require(_to!=address(0));
    //nor it should be admin address
    require(_to!=address(this));

    _transfer(_from,_to,_license_number);


  }

  function giveLicense(address _account,uint _type)onlyAdmin() public {
    uint256 licenseId = _mint(_account,_type);
    emit LicenseGiven(_account,licenseId);
  }


  //Internal Private Methods
  function _owns(address _claimant,uint _licenseId) internal view returns (address) {
    return licenseNumberToClient[_licenseId];

  }

  function _mint(address _account,uint _type) onlyAdmin() internal returns (uint256 tokenId){
    LicenseAttributes memory licenseToken = LicenseAttributes({
      licenseType : LicenseType(_type),
      state : LicenseState.INACTIVE,
      registeredOn :now,
      expiresOn : now ,
      device_hardware_id : "VRUSHANG"
      });
      
      uint id = license.push(licenseToken) -1;
      _transfer(0x0000000000000000000000000000000000000000,_account,id);
      return id;

  }
  function _transfer(address _from,address _to,uint _licNumber)internal {
    ownershipLicenseCount[_to]++;
    licenseNumberToClient[_licNumber]=_to;

    if(_from!= address(0)){
      ownershipLicenseCount[_from]--;

    }
    emit Transfer(_from, _to, _licNumber);
  }
}