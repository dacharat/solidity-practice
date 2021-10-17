from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrage
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act
    starting_value = simple_storage.retrieve()
    expected = 0
    # Assert
    assert starting_value == expected


def test_updating_storage():
    # Arrage
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act
    expected = 15
    simple_storage.store(15, {"from": account})
    updated_value = simple_storage.retrieve()
    # Assert
    assert updated_value == expected
