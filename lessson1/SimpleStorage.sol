// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 favoriteNumber;
    bool favoriteBool;
    
    int[] numbers;
    // string favoriteString = "String";
    // int256 favoriteInt = -5;
    // address favoriteAddress = 0xC8D95Aed98256d23b16539c385524c8879B4A416;
    // bytes32 favoriteBytes = "cat";
    
    struct People {
        uint256 favoriteNumber;
        string name;
    }
    
    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;
    
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
    
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }
    
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
    
    function nothing() private {
         numbers.push(1);
         numbers.push(2);
         
         // pointer to numbers
        //  int[] storage myArray = numbers;
         // copy the value of number
        //  int[] memory myArray2 = numbers;
    }
}
