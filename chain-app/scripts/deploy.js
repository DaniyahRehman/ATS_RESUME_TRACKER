const hre = require("hardhat");

async function main() {
    // Get the contract factory
    const Tracking = await hre.ethers.getContractFactory("Tracking");
    
    // Deploy the contract
    const chainApp = await Tracking.deploy();  // Note: variable name changed from chainApp to tracking
    
    // Wait for deployment
    await chainApp.deployTransaction.wait();  // Changed from tracking.deployed()
    console.log(`Tracking deployed to ${chainApp.address}`);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});