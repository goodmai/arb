import pytest
from unittest.mock import MagicMock
from web3 import Web3
from arbitrage import get_price, calculate_arbitrage, weth_address, usdt_address

@pytest.fixture
def mock_web3():
    mock = MagicMock(spec=Web3)
    mock.eth = MagicMock()
    mock.eth.contract = MagicMock()
    return mock

@pytest.mark.parametrize("price_mock_1_reserve, price_mock_2_reserve, expected_profit", [
    ((1000 * 10 ** 18, 2000 * 10 ** 6, 12345678), (950 * 10 ** 18, 2000 * 10 ** 6, 12345678), 0.003684),
    ((1000 * 10 ** 18, 2000 * 10 ** 6, 12345678), (900 * 10 ** 18, 2000 * 10 ** 6, 12345678), 0.011764),
    ((1000 * 10 ** 18, 2000 * 10 ** 6, 12345678), (800 * 10 ** 18, 2000 * 10 ** 6, 12345678), 0.035714),
    ((1000 * 10 ** 18, 2000 * 10 ** 6, 12345678), (500 * 10 ** 18, 2000 * 10 ** 6, 12345678), 0.142857)
])
def test_arbitrage(mock_web3, price_mock_1_reserve, price_mock_2_reserve, expected_profit):
    pools = [
        Web3.to_checksum_address('0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852'),  # Uniswap V2 WETH/USDT
        Web3.to_checksum_address('0x06da0fd433c1a5d7a4faa01111c044910a184553')  # SushiSwap WETH/USDT
    ]

    price_mock_1 = MagicMock()
    price_mock_1.call.return_value = price_mock_1_reserve

    price_mock_2 = MagicMock()
    price_mock_2.call.return_value = price_mock_2_reserve

    mock_web3.eth.contract.return_value.functions.getReserves.side_effect = [price_mock_1, price_mock_2]
    mock_web3.eth.contract.return_value.functions.token0.return_value.call.return_value = weth_address
    mock_web3.eth.contract.return_value.functions.token1.return_value.call.return_value = usdt_address

    prices = [get_price(mock_web3.eth.contract(address=pool, abi='')) for pool in pools]

    gas_price = 100 * 10 ** 9  # 100 gwei
    swap_gas_estimate = 150000
    slippage = 0.01

    differences = calculate_arbitrage(prices, gas_price, slippage, swap_gas_estimate)

    assert differences, "No arbitrage opportunities found."
    assert abs(differences[0]['profit_usdt'] - expected_profit) > 0, f"Expected profit close to {expected_profit}, got {differences[0]['profit_usdt']}"
