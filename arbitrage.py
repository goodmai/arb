from web3 import Web3

# Подключение к Ethereum через RPC-сервис . Использован chainlist , для решения в проде рекомендуется заменить на infura
w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
# Адреса токенов и пулов
weth_address = Web3.to_checksum_address('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')  # WETH
usdt_address = Web3.to_checksum_address('0xdAC17F958D2ee523a2206206994597C13D831ec7')  # USDT
pools = [
    Web3.to_checksum_address('0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852'),  # Uniswap V2 WETH/USDT https://etherscan.io/address/0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852#code
    Web3.to_checksum_address('0x06da0fd433c1a5d7a4faa01111c044910a184553')  # SushiSwap WETH/USDT https://etherscan.io/address/0x06da0fd433c1a5d7a4faa01111c044910a184553#code
]

# ABI контракта Uniswap V2 Pair
abi = '''[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'''


# Функция для получения decimals из контракта токена
def get_token_decimals(token_address):
    erc20_abi = '''[{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"}]'''
    token_contract = w3.eth.contract(address=token_address, abi=erc20_abi)
    return token_contract.functions.decimals().call()


# Получение decimals для WETH и USDT
weth_decimals = get_token_decimals(weth_address)
usdt_decimals = get_token_decimals(usdt_address)

# Функция для получения цены из пула
def get_price(pool_contract):
    reserves = pool_contract.functions.getReserves().call()
    token0_address = pool_contract.functions.token0().call()
    (reserve0, reserve1, _) = reserves

    # Проверяем, какой токен является первым в паре (token0)
    if token0_address.lower() == weth_address.lower():
        # Если WETH первый, то цена ETH = reserve1 / reserve0
        price = reserve1 / reserve0 / 10 ** (usdt_decimals - weth_decimals)
    else:
        # Если USDT первый, то цена ETH = reserve0 / reserve1
        price = reserve0 / reserve1 / 10 ** (weth_decimals - usdt_decimals)

    return price

# Получение цен из пулов
prices = [get_price(w3.eth.contract(address=pool, abi=abi)) for pool in pools]

for i, pool in enumerate(pools):
    print(f"Pool {i+1} ({pool}): {prices[i]:.6f} USDT/WETH")

# Функция для получения резервов и адресов токенов из пула
def get_pool_data(pool_address):
    pool_contract = w3.eth.contract(address=pool_address, abi=abi)
    reserves = pool_contract.functions.getReserves().call()
    token0_address = pool_contract.functions.token0().call()
    token1_address = pool_contract.functions.token1().call()
    return reserves, token0_address, token1_address
#Основная функция для внешних модулей
def calculate_arbitrage(prices, gas_price, slippage, swap_gas_estimate):
    average_price = sum(prices) / len(prices)
    swap_cost_eth = swap_gas_estimate * gas_price * 2 / (10 ** 18)  # in ETH
    swap_cost_usdt = swap_cost_eth * average_price

    differences = []
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            price_diff = abs(prices[i] - prices[j])
            percent_diff = price_diff / ((prices[i] + prices[j]) / 2) * 100
            if percent_diff > 0.5:
                arbitrage_profit = price_diff - (slippage * 2 * min(prices[i], prices[j])) - swap_cost_usdt
                if arbitrage_profit > 0:
                    differences.append({
                        'pool_1': i + 1,
                        'pool_2': j + 1,
                        'percent_diff': percent_diff,
                        'profit_usdt': arbitrage_profit
                    })
    return differences

# Проверка данных для каждого пула
for pool in pools:
    reserves, token0_address, token1_address = get_pool_data(pool)
    print(f"Пул: {pool}")
    print(f"Резервы: {reserves}")
    print(f"Token0: {token0_address}")
    print(f"Token1: {token1_address}")
    print()

# Учитываем проскальзывание в 1%
slippage = 0.01

# Получение текущей цены газа в Wei (примерный расчет, для точности используйте более надежные методы)
gas_price = w3.eth.gas_price
average_price = (prices[0]+prices[1])/2
# Оценка стоимости свапов
swap_gas_estimate = 150000  # приблизительная оценка газа для одного свапа
swap_cost_eth = swap_gas_estimate * gas_price * 2  # два свапа
swap_cost_usdt = swap_cost_eth * average_price / (10 ** weth_decimals)  # перевод стоимости в USDT

# Поиск арбитражных возможностей
differences = []
for i in range(len(prices)):
    for j in range(i + 1, len(prices)):
        diff = abs(prices[i] - prices[j]) / ((prices[i] + prices[j]) / 2) * 100
        if diff > 0.5:  # Проверяем разницу больше 0.5%
            price_diff = abs(prices[i] - prices[j])
            arbitrage_profit = price_diff - (slippage * 2 * prices[i]) - swap_cost_usdt  # Учитываем проскальзывание и стоимость свапов
            if arbitrage_profit > 0:
                print(f"Возможна арбитражная возможность между пулами {i+1} и {j+1}: {diff:.2f}% с возможной прибылью {arbitrage_profit:.6f} USDT")
                differences.append(diff)

if not differences:
    print("Арбитражных возможностей не найдено.")

# Средняя цена ETH
average_price = sum(prices) / len(prices)
print(f"\nСредняя цена ETH: {average_price:.6f} USDT")