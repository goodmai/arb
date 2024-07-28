// SPDX-License-Identifier: MIT
//ATTENTION This contract build in educational and tests purpose and never been used as product.
pragma solidity ^0.8.0;

import "@uniswap/v2-core/contracts/interfaces/IUniswapV2Pair.sol";
import "@uniswap/v2-core/contracts/interfaces/IUniswapV2Factory.sol";
import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Arbitrage {
    address public owner;
    IUniswapV2Router02 public uniswapRouter;
    IERC20 public weth;
    IERC20 public usdt;

    uint256 public constant SLIPPAGE = 1; // 1%
    uint256 public constant PROFIT_THRESHOLD = 0.5; // 0.5%

    constructor(
        address _uniswapRouter,
        address _weth,
        address _usdt
    ) {
        owner = msg.sender;
        uniswapRouter = IUniswapV2Router02(_uniswapRouter);
        weth = IERC20(_weth);
        usdt = IERC20(_usdt);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _;
    }

    function getReserves(address pairAddress) public view returns (uint256 reserveWETH, uint256 reserveUSDT) {
        IUniswapV2Pair pair = IUniswapV2Pair(pairAddress);
        (uint112 reserve0, uint112 reserve1, ) = pair.getReserves();
        address token0 = pair.token0();
        if (token0 == address(weth)) {
            reserveWETH = reserve0;
            reserveUSDT = reserve1;
        } else {
            reserveWETH = reserve1;
            reserveUSDT = reserve0;
        }
    }

    function calculatePriceImpact(uint256 amountIn, uint256 reserveIn, uint256 reserveOut) public pure returns (uint256) {
        uint256 amountInWithFee = amountIn * 997;
        uint256 numerator = amountInWithFee * reserveOut;
        uint256 denominator = (reserveIn * 1000) + amountInWithFee;
        return numerator / denominator;
    }

    function executeArbitrage(address pool1, address pool2, uint256 amountWETH) external onlyOwner {
        // Step 1: Fetch reserves for both pools
        (uint256 reserveWETH1, uint256 reserveUSDT1) = getReserves(pool1);
        (uint256 reserveWETH2, uint256 reserveUSDT2) = getReserves(pool2);

        // Step 2: Calculate prices
        uint256 price1 = (reserveUSDT1 * 1e18) / reserveWETH1;
        uint256 price2 = (reserveUSDT2 * 1e18) / reserveWETH2;

        // Step 3: Determine the direction of arbitrage
        bool isArbitragePossible;
        if (price1 > price2) {
            isArbitragePossible = true;
        } else {
            isArbitragePossible = false;
        }

        // Step 4: Check for profit after slippage and gas fees
        uint256 profit;
        if (isArbitragePossible) {
            // Buy on pool2, sell on pool1
            uint256 wethBought = calculatePriceImpact(amountWETH, reserveUSDT2, reserveWETH2);
            uint256 usdtReceived = calculatePriceImpact(wethBought, reserveWETH1, reserveUSDT1);
            profit = usdtReceived - (amountWETH * price2);
        } else {
            // Buy on pool1, sell on pool2
            uint256 wethBought = calculatePriceImpact(amountWETH, reserveUSDT1, reserveWETH1);
            uint256 usdtReceived = calculatePriceImpact(wethBought, reserveWETH2, reserveUSDT2);
            profit = usdtReceived - (amountWETH * price1);
        }

        // Calculate net profit after considering slippage and fees
        uint256 netProfit = profit * (100 - SLIPPAGE) / 100;

        // Step 5: Execute the trade if the profit is above the threshold
        if (netProfit >= PROFIT_THRESHOLD) {
            if (isArbitragePossible) {
                // Buy on pool2
                usdt.transferFrom(msg.sender, address(this), amountWETH * price2);
                usdt.approve(address(uniswapRouter), amountWETH * price2);
                uniswapRouter.swapExactTokensForTokens(
                    amountWETH * price2,
                    0,
                    getPathForUSDTToWETH(),
                    address(this),
                    block.timestamp
                );

                // Sell on pool1
                weth.approve(address(uniswapRouter), amountWETH);
                uniswapRouter.swapExactTokensForTokens(
                    amountWETH,
                    0,
                    getPathForWETHToUSDT(),
                    msg.sender,
                    block.timestamp
                );
            } else {
                // Buy on pool1
                usdt.transferFrom(msg.sender, address(this), amountWETH * price1);
                usdt.approve(address(uniswapRouter), amountWETH * price1);
                uniswapRouter.swapExactTokensForTokens(
                    amountWETH * price1,
                    0,
                    getPathForUSDTToWETH(),
                    address(this),
                    block.timestamp
                );

                // Sell on pool2
                weth.approve(address(uniswapRouter), amountWETH);
                uniswapRouter.swapExactTokensForTokens(
                    amountWETH,
                    0,
                    getPathForWETHToUSDT(),
                    msg.sender,
                    block.timestamp
                );
            }
        } else {
            revert("No arbitrage opportunity");
        }
    }

    function getPathForWETHToUSDT() private view returns (address[] memory) {
        address[] memory path = new address[](2);
        path[0] = address(weth);
        path[1] = address(usdt);
        return path;
    }

    function getPathForUSDTToWETH() private view returns (address[] memory) {
        address[] memory path = new address[](2);
        path[0] = address(usdt);
        path[1] = address(weth);
        return path;
    }

    function withdrawTokens(address token) external onlyOwner {
        IERC20(token).transfer(owner, IERC20(token).balanceOf(address(this)));
    }

    function withdrawETH() external onlyOwner {
        payable(owner).transfer(address(this).balance);
    }

    receive() external payable {}
}
