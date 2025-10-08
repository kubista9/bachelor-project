from fredapi import Fred
import pandas as pd

fred = Fred(api_key='9e03508d30b285d66848fd01e97544df')

# -----------------------------
# 🏦 1. MONEY, BANKING & CREDIT
# -----------------------------

df = fred.get_series('M1SL')        # M1 Money Stock
df.to_csv('M1_Money_Stock.csv')

df = fred.get_series('MZM')         # Money with Zero Maturity
df.to_csv('MZM_Money_Zero_Maturity.csv')

df = fred.get_series('CURRCIR')     # Currency in Circulation
df.to_csv('Currency_in_Circulation.csv')

df = fred.get_series('TOTRESNS')    # Total Reserves
df.to_csv('Total_Reserves.csv')

df = fred.get_series('REQRESNS')    # Required Reserves
df.to_csv('Required_Reserves.csv')

df = fred.get_series('EXCSRESNS')   # Excess Reserves
df.to_csv('Excess_Reserves.csv')

df = fred.get_series('TOTALSL')     # Consumer Credit Outstanding
df.to_csv('Consumer_Credit_Outstanding.csv')

df = fred.get_series('BUSLOANS')    # Commercial and Industrial Loans
df.to_csv('Commercial_Industrial_Loans.csv')

df = fred.get_series('REALLN')      # Real Estate Loans
df.to_csv('Real_Estate_Loans.csv')

df = fred.get_series('USNIM')       # Net Interest Margin of Banks
df.to_csv('Net_Interest_Margin_Banks.csv')

# -----------------------------
# 📊 2. PRICES, WAGES & COSTS
# -----------------------------

df = fred.get_series('PPIACO')      # PPI: All Commodities
df.to_csv('PPI_All_Commodities.csv')

df = fred.get_series('PCUOMFGOMFG') # PPI: Manufacturing
df.to_csv('PPI_Manufacturing.csv')

df = fred.get_series('IR')          # Import Price Index (all commodities)
df.to_csv('Import_Price_Index.csv')

df = fred.get_series('CES0500000003') # Avg Hourly Earnings: Total Private
df.to_csv('Average_Hourly_Earnings_Total_Private.csv')

df = fred.get_series('ECIWAG')        # Employment Cost Index: Wages and Salaries
df.to_csv('Employment_Cost_Index_Wages_Salaries.csv')

df = fred.get_series('ULCNFB')        # Unit Labor Costs
df.to_csv('Unit_Labor_Costs.csv')

# -----------------------------
# 🧍‍♂️ 3. EMPLOYMENT & DEMOGRAPHICS
# -----------------------------

df = fred.get_series('CIVPART')       # Labor Force Participation Rate
df.to_csv('Labor_Force_Participation_Rate.csv')

df = fred.get_series('EMRATIO')       # Employment-Population Ratio
df.to_csv('Employment_Population_Ratio.csv')

df = fred.get_series('LNS14000006')   # Unemployment Rate: Men 20+
df.to_csv('Unemployment_Rate_Men_20+.csv')

df = fred.get_series('JTSJOL')        # Job Openings (JOLTS)
df.to_csv('Job_Openings_JOLTS.csv')

df = fred.get_series('ICSA')          # Initial Jobless Claims
df.to_csv('Initial_Jobless_Claims.csv')

df = fred.get_series('LREM25TTUSM156S') # Youth Unemployment Rate
df.to_csv('Youth_Unemployment_Rate.csv')

# -----------------------------
# 🏠 4. HOUSING & REAL ESTATE
# -----------------------------

df = fred.get_series('CSUSHPINSA')  # Case-Shiller Home Price Index
df.to_csv('Case_Shiller_US_Home_Price_Index.csv')

df = fred.get_series('MSPUS')       # Median Sales Price of Houses
df.to_csv('Median_Sales_Price_Houses.csv')

df = fred.get_series('HOUST')       # Housing Starts
df.to_csv('Housing_Starts.csv')

df = fred.get_series('PERMIT')      # Building Permits
df.to_csv('Building_Permits.csv')

df = fred.get_series('MORTGAGE30US') # 30-Year Fixed Rate Mortgage Average
df.to_csv('Mortgage_30Y_Fixed.csv')

df = fred.get_series('CUSR0000SEHA') # Rent Inflation (CPI Rent of Primary Residence)
df.to_csv('Rent_Inflation_CPI.csv')

# -----------------------------
# 🏭 5. PRODUCTION & BUSINESS ACTIVITY
# -----------------------------

df = fred.get_series('INDPRO')         # Industrial Production Index
df.to_csv('Industrial_Production_Index.csv')

df = fred.get_series('CAPUTLB00004S')  # Capacity Utilization: Manufacturing
df.to_csv('Capacity_Utilization_Manufacturing.csv')

df = fred.get_series('BUSINV')         # Private Inventories
df.to_csv('Private_Inventories.csv')

df = fred.get_series('NAPM')           # ISM PMI
df.to_csv('ISM_PMI.csv')

df = fred.get_series('T10YFF')         # 10-Year Treasury Minus Fed Funds
df.to_csv('Yield_Curve_T10YFF.csv')

df = fred.get_series('CLIUSA')         # Composite Leading Indicator (OECD)
df.to_csv('Composite_Leading_Indicator.csv')

# -----------------------------
# 🌍 6. INTERNATIONAL & TRADE
# -----------------------------

df = fred.get_series('NETEXP')         # Net Exports
df.to_csv('Net_Exports.csv')

df = fred.get_series('BOPGSTB')        # Balance on Goods and Services
df.to_csv('Balance_Goods_Services.csv')

df = fred.get_series('EXPGS')          # Exports of Goods and Services
df.to_csv('Exports_Goods_Services.csv')

df = fred.get_series('IMPGS')          # Imports of Goods and Services
df.to_csv('Imports_Goods_Services.csv')

df = fred.get_series('DEXUSEU')        # USD/EUR Exchange Rate
df.to_csv('USD_EUR_Exchange_Rate.csv')

df = fred.get_series('TWEXBPA')        # Trade Weighted USD Index
df.to_csv('Trade_Weighted_USD_Index.csv')

df = fred.get_series('IR3TIB01USM156N') # 3-Month Interbank Rate
df.to_csv('3M_Interbank_Rate.csv')

df = fred.get_series('FPCPITOTLZGJPN') # Japan CPI (Inflation)
df.to_csv('Japan_CPI.csv')

# -----------------------------
# 💹 7. FINANCIAL MARKETS
# -----------------------------

df = fred.get_series('SP500')      # S&P 500 Index
df.to_csv('SP500.csv')

df = fred.get_series('DJIA')       # Dow Jones Industrial Average
df.to_csv('DJIA.csv')

df = fred.get_series('VIXCLS')     # CBOE Volatility Index (VIX)
df.to_csv('VIX.csv')

df = fred.get_series('BAA10Y')     # Moody’s Baa - 10Y Treasury Spread
df.to_csv('BAA10Y_Spread.csv')

df = fred.get_series('TEDRATE')    # TED Spread
df.to_csv('TED_Spread.csv')

df = fred.get_series('WALCL')      # Fed Total Assets
df.to_csv('Fed_Total_Assets.csv')

df = fred.get_series('WRESBAL')    # Reserve Balances with Fed
df.to_csv('Reserve_Balances_Fed.csv')

# -----------------------------
# 🧾 8. FISCAL & GOVERNMENT
# -----------------------------

df = fred.get_series('FYFSD')          # Federal Surplus or Deficit
df.to_csv('Federal_Surplus_Deficit.csv')

df = fred.get_series('GFDEGDQ188S')    # Federal Debt: Total Public Debt % GDP
df.to_csv('Federal_Debt_Percent_GDP.csv')

df = fred.get_series('GCEC1')          # Government Consumption Expenditures
df.to_csv('Gov_Consumption_Expenditures.csv')

df = fred.get_series('FGEXPND')        # Federal Gov Current Expenditures
df.to_csv('Federal_Gov_Expenditures.csv')

df = fred.get_series('FYGFGDQ188S')    # Federal Debt Held by the Public
df.to_csv('Federal_Debt_Public.csv')

# -----------------------------
# 🧑‍🎓 9. EDUCATION & POPULATION
# -----------------------------

df = fred.get_series('POPTHM')          # Total Population: Men
df.to_csv('Total_Population_Men.csv')

df = fred.get_series('SPPOPGROWUSA')    # Population Growth Rate
df.to_csv('Population_Growth_Rate.csv')

df = fred.get_series('SEADFUSA')        # Educational Attainment (Bachelor’s+)
df.to_csv('Education_Bachelor_or_Higher.csv')

df = fred.get_series('LFWA64TTUSM647S') # Working Age Population
df.to_csv('Working_Age_Population.csv')

# -----------------------------
# 💰 10. CONSUMER & SENTIMENT
# -----------------------------

df = fred.get_series('UMCSENT')            # University of Michigan Sentiment
df.to_csv('Consumer_Sentiment_Michigan.csv')

df = fred.get_series('CONSUMERCONFIDENCE') # Conference Board Confidence
df.to_csv('Consumer_Confidence_Index.csv')

df = fred.get_series('TOTALSL')            # Consumer Loans (TOTALSL reused)
df.to_csv('Consumer_Loans.csv')

df = fred.get_series('RRSFS')              # Real Retail & Food Services Sales
df.to_csv('Retail_Food_Services_Sales.csv')

df = fred.get_series('PCE')                # Personal Consumption Expenditures
df.to_csv('Personal_Consumption_Expenditures.csv')

# -----------------------------
# ⚙️ 11. ENERGY & COMMODITIES
# -----------------------------

df = fred.get_series('DCOILWTICO')  # Crude Oil WTI
df.to_csv('Crude_Oil_WTI.csv')

df = fred.get_series('GASREGW')     # Retail Gasoline Prices
df.to_csv('Retail_Gasoline_Prices.csv')

df = fred.get_series('PCOPPUSDM')   # Copper Prices
df.to_csv('Copper_Prices.csv')

df = fred.get_series('IR14270')     # Gold Fixing Price (London PM)
df.to_csv('Gold_Price_London_PM.csv')

df = fred.get_series('COALPRCUSA')  # Coal Prices
df.to_csv('Coal_Prices.csv')

df = fred.get_series('PNGASUS')     # Natural Gas Spot Price
df.to_csv('Natural_Gas_Price.csv')

# -----------------------------
# 🧮 12. DERIVED / COMPOSITE INDICATORS
# -----------------------------

df = fred.get_series('NFCI')          # Chicago Fed Financial Conditions Index
df.to_csv('Financial_Conditions_Index.csv')

df = fred.get_series('ADSINDEX')      # ADS Business Conditions Index
df.to_csv('ADS_Business_Conditions_Index.csv')

df = fred.get_series('USSLIND')       # Leading Index for the US
df.to_csv('Leading_Index_USA.csv')

df = fred.get_series('RECPROUSM156N') # Probability of Recession Next 12 Months
df.to_csv('Recession_Probability_12M.csv')
