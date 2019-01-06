var LicenseToken = artifacts.require("./LicenseToken.sol");

module.exports = function(deployer) {
  deployer.deploy(LicenseToken);
};
