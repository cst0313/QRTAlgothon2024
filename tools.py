import numpy as np
import pandas as pd
import cryptpandas as crp


def get_value(pct_change):
    return np.cumprod(1 + pct_change)


def get_cum_return(pct_change):
    return get_value(pct_change) - 1


def get_std(pct_change):
    return pct_change.std()


def annual_risk(pct_change):
    return get_std(pct_change) * np.sqrt(252)


def annual_return(pct_change):
    return np.power(pct_change.mean() + 1, 252) - 1


def sharpe_ratio(pct_change):
    return annual_return(pct_change) / annual_risk(pct_change)


def get_peak(pct_change):
    value = get_value(pct_change)

    peaks = value.apply(lambda x: [x.iloc[:i + 1].max() for i in range(x.shape[0])])

    return peaks


def get_drawdown(pct_change):
    return (get_value(pct_change) / get_peak(pct_change) - 1).fillna(0)


def max_drawdown(pct_change):
    drawdown = get_drawdown(pct_change)
    return -(drawdown.min())


def downside_risk(pct_change):
    temp = pct_change.apply(lambda x: [min(r_i, 0) for r_i in x])

    return temp.std() * np.sqrt(252)


def sortino_ratio(pct_change):
    down_vol = downside_risk(pct_change)
    annual_r_p = annual_return(pct_change)

    return annual_r_p / down_vol


def benchmark_mean(pct_change):
    return pct_change.mean()


def alpha(strat_ret, benchmark_ret):
    return annual_return(strat_ret) - annual_return(benchmark_ret)


def rolling_volatility(strat_ret, benchmark_ret):
    pass

def pnl(actual_rets, weights):
    return np.dot(actual_rets[weights.index], weights)

def read_data(path, password):
    _df = crp.read_encrypted(path=path, password=password)
    _df = _df.fillna(0)
    _df /= 100  # change to decimal

    _df = _df.apply(lambda x: np.where(x > 1, 0, x))
    _df = _df.apply(lambda x: np.where(x < -1, 0, x))

    _df['strat_4'] = 0
    _df['strat_5'] = 0

    return _df

def get_positions(pos_dict):
    pos = pd.Series(pos_dict)
    pos = pos.replace([np.inf, -np.inf], np.nan)
    pos = pos.dropna()
    pos = pos / pos.abs().sum()
    pos = pos.clip(-0.1,0.1)
    if pos.abs().max() / pos.abs().sum() > 0.1:
        raise ValueError(f"Portfolio too concentrated {pos.abs().max()=} / {pos.abs().sum()=}")
    return pos

def get_submission_dict(
        pos_dict,
        your_team_name: str = "T1089",
        your_team_passcode: str = "ilikeqrt",
):

    return {
        **get_positions(pos_dict).to_dict(),
        **{
            "team_name": your_team_name,
            "passcode": your_team_passcode,
        },
    }
