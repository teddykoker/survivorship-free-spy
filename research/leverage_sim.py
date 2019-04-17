import pandas_datareader.data as web
import pandas as pd
import datetime


def sim_leverage(df, leverage=1, expense_ratio=0.0, initial_value=1.0):
    pct_change = df["Adj Close"].pct_change(1)
    sim = pd.DataFrame().reindex_like(df)
    pct_change = (pct_change - expense_ratio / 252) * leverage
    sim["Adj Close"] = (1 + pct_change).cumprod() * initial_value
    sim["Close"] = (1 + pct_change).cumprod() * initial_value

    sim.loc[sim.index[0], "Adj Close"] = initial_value
    sim = sim.drop(columns=["Volume"])

    sim["Open"] = sim["Adj Close"]
    sim["High"] = sim["Adj Close"]
    sim["Low"] = sim["Adj Close"]
    sim["Close"] = sim["Adj Close"]

    return sim


def main():
    start = datetime.datetime(1989, 1, 1)
    end = datetime.datetime(2019, 1, 1)
    vfinx = web.DataReader("VFINX", "yahoo", start, end)
    vusxt = web.DataReader("VUSTX", "yahoo", start, end)
    upro_sim = sim_leverage(vfinx, leverage=3.0, expense_ratio=0.0092)
    tmf_sim = sim_leverage(vusxt, leverage=3.0, expense_ratio=0.0111)
    spxu_sim = sim_leverage(
        vfinx, leverage=-3.0, expense_ratio=0.0091, initial_value=100000
    )

    spxu_sim.to_csv("../data/SPXU_SIM.csv")
    upro_sim.to_csv("../data/UPRO_SIM.csv")
    tmf_sim.to_csv("../data/TMF_SIM.csv")


if __name__ == "__main__":
    main()
