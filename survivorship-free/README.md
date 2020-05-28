# Survivorship Bias-Free S&P 500 Data

See more information at my [blog post](https://teddykoker.com/2019/05/creating-a-survivorship-bias-free-sp-500-dataset-with-python/).

Generated Data in `data` or `data.zip`. Tickers in `data/tickers.csv`.

### Generate Data

Download Quandl's [WIKI Prices](https://www.quandl.com/databases/WIKIP/usage/export) dataset and save as `WIKI_PRICES.csv`.

Then run `./generate.py`.

**EDIT 2020: iShares no longer publishes historical holdings to their website
(perhaps because of this abuse). Constituents until mid-2019 are available in
[constituents.csv](constituents.csv)**
