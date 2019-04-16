import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

periods = 252


def generate_tearsheet(stats):
    equity = pd.Series(stats).sort_index()
    returns = equity.pct_change().fillna(0.0)

    rolling = returns.rolling(window=periods)
    rolling_sharpe = np.sqrt(252) * (rolling.mean() / rolling.std())

    cum_returns = np.exp(np.log(1 + returns).cumsum())
    drawdown = cum_returns.div(cum_returns.cummax()) - 1

    fig, axs = plt.subplots(2, 1)

    cum_returns.plot(ax=axs[0], lw=2, color="green", alpha=0.6)
    axs[0].axhline(1.0, linestyle="--", color="black", lw=1)
    drawdown.plot.area(ax=axs[1], color="red", alpha=0.3)
    plt.show()
