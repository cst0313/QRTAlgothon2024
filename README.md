Problem statement: given data input every 19 minutes, allocate weights to different strategies such that return is maximized. 
Strategy:
Choose 4 strategies with highest Sortino Ratio and allocate 0.1 weight to the top 4. 
After that we generate random portfolios for the top 20 strategies (excluding the top 4), and select the best random portfolio according to Sharpe. 
