pragma solidity >=0.4.21 <0.6.0;

contract Election {
  //Constructor
  //store
  //read
  string public candidate;
  constructor() public {
    candidate="Candidate1";

  }
  function getCandidateName() public view returns (string memory) {
    return candidate;
  }

}
