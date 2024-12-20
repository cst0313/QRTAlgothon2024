from tools import *

path = './public_data/'

def run_strategy(file_name, password):
    df = read_data(path=path + file_name, password=password)

    portfolio_weights = []
    portfolio_returns = []
    portfolio_risks = []
    portfolio_sharpes = []

    def compute_portfolio_return(_df, _weights):
        return (1 + np.sum(_weights * _df.mean())) ** 252 - 1

    def compute_portfolio_risk(_df, _weights):  # portfolio variance formula
        return np.sqrt(_weights.T @ (_df.cov() * 252) @ _weights)

    def compute_random_portfolio(_df, _iterations) -> None:
        ranks = sortino_ratio(_df).sort_values(ascending=False).index[:24]
        ranks = [int(strat[6:]) for strat in ranks]
        no_of_stocks = _df.shape[1]

        rank_4 = ranks[:4]  # top 4 in sortino ratio
        for i in range(_iterations):
            weights = np.zeros(no_of_stocks)
            for n in range(no_of_stocks):
                if n in rank_4 or n not in ranks:
                    weights[n] = 0
                else:
                    x = np.random.random()
                    if x > 0.1:
                        x /= 2
                    weights[n] = x + 0.001

            weights = weights.round(4)
            weights /= abs(weights).sum()
            weights *= 0.6

            for n in rank_4:
                weights[n] = 0.1

            portfolio_weights.append(weights)

            expected_return = compute_portfolio_return(_df, weights)
            portfolio_returns.append(expected_return)

            risk = compute_portfolio_risk(_df, weights)
            portfolio_risks.append(risk)

            sharpe = expected_return / risk
            portfolio_sharpes.append(sharpe)

    data = df[-78:]

    # run the simulations
    compute_random_portfolio(data, 30000)

    # get the Max Sharpe Ratio, Max Return, Min Volatility
    max_sharpe = max(portfolio_sharpes)
    max_return = max(portfolio_returns)
    min_risk = min(portfolio_risks)

    # find the portfolio index for each
    sharpe_idx = portfolio_sharpes.index(max_sharpe)
    return_idx = portfolio_returns.index(max_return)
    min_risk_idx = portfolio_risks.index(min_risk)

    # find the portfolio weights for each
    sharpe_w = portfolio_weights[sharpe_idx]
    max_return_w = portfolio_weights[return_idx]
    min_risk_w = portfolio_weights[min_risk_idx]

    INITIAL_CASH = 1_000

    def compute_wealth(_df, _weights):
        initial_values = (1 + _df.iloc[0]) * _weights * INITIAL_CASH
        cumulative_ret = np.cumprod(1 + _df)
        cumulative_wealths = cumulative_ret * initial_values

        return cumulative_wealths.sum(axis=1)

    values = pd.DataFrame()
    values['Max Sharpe'] = compute_wealth(data, sharpe_w)
    values['Max Return'] = compute_wealth(data, max_return_w)
    values['Min Volatility'] = compute_wealth(data, min_risk_w)

    # find the portfolio weights
    results_weights = pd.DataFrame(index = data.columns)
    results_weights['max sharpe ratio'] = sharpe_w
    results_weights['max return'] = max_return_w
    results_weights['min risk'] = min_risk_w

    clipped_weights = results_weights['max sharpe ratio']

    pos_dict = clipped_weights.to_dict()
    submission_dict = get_submission_dict(pos_dict)
    
    return submission_dict, max_sharpe

def backtest(history, submission_dict, new_file, new_password):
    new_df = read_data(path = path + new_file, password = new_password)
    w_dict = {k: submission_dict[k] for k in submission_dict if k[:5] == 'strat'}
    w_dict = pd.DataFrame(data=w_dict.values(), index=w_dict.keys())

    pnls = pnl(new_df[-78:], w_dict)

    final_val = np.prod(1 + pnls) - 1
    history += [pl[0] for pl in pnls]

    print(final_val)
