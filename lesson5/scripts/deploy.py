from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    account = get_account()
    print(account)
    simple_storage = SimpleStorage.deploy({"from": account})
    # Transaction
    # Call
    print(simple_storage)
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    print(transaction)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


# def deploy_simple_storage_testnet():
#     account = accounts.add(config["wallets"]["from_key"])
#     simple_storage = SimpleStorage.deploy({"from": account})
#     stored_value = simple_storage.retrieve()
#     print(stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
