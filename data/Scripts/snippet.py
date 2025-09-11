# pip install yfinance pandas --upgrade
import pandas as pd
import yfinance as yf

TICKER = "AAPL"  # change to any symbol
t = yf.Ticker(TICKER)

def show_df(title, df, n=5):
    if df is None or (hasattr(df, "empty") and df.empty):
        print(f"\n{title}: <empty>")
        return
    print(f"\n{title}: shape={getattr(df, 'shape', None)}")
    try:
        print(df.head(n))
    except Exception:
        print(df)

def show_dict(title, d, max_keys=25):
    if not d:
        print(f"\n{title}: <empty>")
        return
    keys = sorted(d.keys())
    print(f"\n{title}: {len(keys)} keys")
    for k in keys[:max_keys]:
        print(f"  - {k}: {d.get(k)}")
    if len(keys) > max_keys:
        print(f"  ... (+{len(keys)-max_keys} more keys)")

print(f"=== yfinance snapshot for {TICKER} ===")

# 1) Quote / fast info
try:
    show_dict("fast_info", t.fast_info.__dict__ if hasattr(t.fast_info, "__dict__") else dict(t.fast_info))
except Exception:
    print("\nfast_info: <unavailable>")

try:
    show_dict("info (selected keys)", {k: t.info.get(k) for k in [
        "currentPrice","previousClose","open","dayHigh","dayLow","fiftyTwoWeekHigh","fiftyTwoWeekLow",
        "marketCap","currency","exchange","sharesOutstanding","trailingPE","forwardPE","dividendYield"
    ] if k in getattr(t, "info", {})})
except Exception:
    print("\ninfo: <unavailable>")

# 2) Historical prices & corporate actions
show_df("history(period='2y', interval='1d')", t.history(period="2y", interval="1d"))
show_df("dividends", t.dividends)
show_df("splits", t.splits)
show_df("actions", t.actions)

# 3) Options
try:
    expiries = t.options
    print(f"\noptions expiries: {expiries[:10]}{' ...' if len(expiries)>10 else ''}")
    if expiries:
        oc = t.option_chain(expiries[0])
        show_df(f"option_chain({expiries[0]}).calls", oc.calls)
        show_df(f"option_chain({expiries[0]}).puts", oc.puts)
except Exception as e:
    print(f"\noptions: <unavailable> ({e})")

# 4) Fundamentals
show_df("income_stmt (annual)", t.income_stmt)
show_df("quarterly_income_stmt", t.quarterly_income_stmt)
show_df("balance_sheet (annual)", t.balance_sheet)
show_df("cashflow (annual)", t.cashflow)

# 5) Earnings & calendar
try:
    show_df("earnings (annual history)", t.earnings)
except Exception:
    pass
try:
    show_df("earnings_dates (recent)", t.earnings_dates(limit=12))
except Exception:
    pass
try:
    show_df("calendar (upcoming events)", t.calendar)
except Exception:
    pass

# 6) Analysts & estimates
show_df("recommendations", t.recommendations)
show_df("recommendations_summary", t.recommendations_summary)
show_df("analyst_price_targets", t.analyst_price_targets)
show_df("earnings_estimate", t.earnings_estimate)
show_df("revenue_estimate", t.revenue_estimate)
show_df("eps_trend", t.eps_trend)
show_df("eps_revisions", t.eps_revisions)
show_df("growth_estimates", t.growth_estimates)

# 7) Holders & insiders
show_df("major_holders", t.major_holders)
show_df("institutional_holders", t.institutional_holders)
show_df("mutualfund_holders", t.mutualfund_holders)
show_df("insider_roster_holders", t.insider_roster_holders)
show_df("insider_transactions", t.insider_transactions)
show_df("insider_purchases", t.insider_purchases)

# 8) ESG / sustainability
show_df("sustainability (ESG)", t.sustainability)

# 9) Identifiers & shares
try:
    print("\nISIN:", getattr(t, "isin", None) or t.get_isin())
except Exception:
    print("\nISIN: <unavailable>")
try:
    show_df("shares (full history)", t.get_shares_full(start="1990-01-01"))
except Exception:
    print("\nshares (full history): <unavailable>")

# 10) News (first 5)
try:
    news = t.news or []
    print(f"\nnews items: {len(news)}")
    for n in news[:5]:
        print(f" - [{pd.to_datetime(n.get('providerPublishTime',0), unit='s', errors='coerce')}] {n.get('publisher')}: {n.get('title')}")
except Exception:
    print("\nnews: <unavailable>")
