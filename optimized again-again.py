# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 07:47:30 2023

@author: elzaf
"""
#Import libraries
import pandas as pd
import datetime as dt

#Load Bloomberg data that was manually cleaned in Excel
excel_data = pd.read_excel("bloomberg_cleaned.xlsx", sheet_name=None)
excel_data = {key: df.set_index('Date').assign(Date=pd.to_datetime(df['Date'])) for key, df in excel_data.items()}

# %% Define the function to calculate F-SCORE

def calculate_fscore(excel_data, year, month, price_month, data_dict, fscore_dict, data_name):

    target_date = dt.datetime(year, month, day=1)
    last_year = target_date - pd.DateOffset(years=1)
        
    # Classify companies by BM Ratio
    tickers = excel_data['BM RATIO'].loc[(excel_data['BM RATIO'].index.month == target_date.month) & (excel_data['BM RATIO'].index.year == target_date.year)].transpose()
    tickers = tickers.rename(columns={tickers.columns[0]: 'BM RATIO'}).assign(**{'BM RATIO':pd.to_numeric(tickers.iloc[:, 0], errors='coerce')}).dropna()
    tickers["Quantile"] = pd.qcut(tickers["BM RATIO"], q=5, labels=False) + 1
    tickers = tickers[tickers['Quantile'] >= 5]
    
    # Classify companies by Market Cap
    sizing = excel_data['MARKET_CAP'].loc[(excel_data['MARKET_CAP'].index.month == target_date.month) & (excel_data['MARKET_CAP'].index.year == target_date.year)].transpose()
    sizing = sizing.rename(columns={sizing.columns[0]: 'Marketcap'})
    sizing['Marketcap'] = pd.to_numeric(sizing.iloc[:, 0], errors='coerce')
    sizing = sizing.dropna().sort_values('Marketcap')
    sizing = sizing.drop(sizing[sizing['Marketcap'] == 0].index)
    sizing = pd.merge(sizing, pd.qcut(sizing["Marketcap"], q=3, labels=['Low', 'Medium', 'High']), left_index=True, right_index=True)
    sizing.rename(columns={"Marketcap_y": "Size", "Marketcap_x": "Marketcap"}, inplace=True)
    
    # Merge BM Ratio and Market Cap data
    year_data = pd.concat([tickers, sizing], axis=1).dropna()
    
    # Extract financial data for analysis    
    roa = excel_data['ROA'][(excel_data['ROA'].index.month == target_date.month) & (excel_data['ROA'].index.year == target_date.year)].transpose()
    roa = roa.rename(columns={roa.columns[0]: 'ROA'}).assign(**{'ROA':pd.to_numeric(roa.iloc[:, 0], errors='coerce')}).dropna()

    roa_ly = excel_data['ROA'].loc[(excel_data['ROA'].index.month == target_date.month) & (excel_data['ROA'].index.year == last_year.year)].transpose()
    roa_ly = roa_ly.rename(columns={roa_ly.columns[0]: 'ROA LY'}).assign(**{'ROA LY':pd.to_numeric(roa_ly.iloc[:, 0], errors='coerce')}).dropna()
 
    cfo = excel_data['CFO'].loc[(excel_data['CFO'].index.month == target_date.month) & (excel_data['CFO'].index.year == target_date.year)].transpose()
    cfo = cfo.rename(columns={cfo.columns[0]: 'CFO'}).assign(**{'CFO':pd.to_numeric(cfo.iloc[:, 0], errors='coerce')}).dropna()

    leverage = excel_data['LEVERAGE'].loc[(excel_data['LEVERAGE'].index.month == target_date.month) & (excel_data['LEVERAGE'].index.year == target_date.year)].transpose()
    leverage = leverage.rename(columns={leverage.columns[0]: 'LEVERAGE'}).assign(**{'LEVERAGE':pd.to_numeric(leverage.iloc[:, 0], errors='coerce')}).dropna()

    leverage_ly = excel_data['LEVERAGE'].loc[(excel_data['LEVERAGE'].index.month == target_date.month) & (excel_data['LEVERAGE'].index.year == last_year.year)].transpose()
    leverage_ly = leverage_ly.rename(columns={leverage_ly.columns[0]: 'LEVERAGE LY'}).assign(**{'LEVERAGE LY':pd.to_numeric(leverage_ly.iloc[:, 0], errors='coerce')}).dropna()

    current_ratio = excel_data['CURRENT RATIO'].loc[(excel_data['CURRENT RATIO'].index.month == target_date.month) & (excel_data['CURRENT RATIO'].index.year == target_date.year)].transpose()
    current_ratio = current_ratio.rename(columns={current_ratio.columns[0]: 'CURRENT RATIO'}).assign(**{'CURRENT RATIO':pd.to_numeric(current_ratio.iloc[:, 0], errors='coerce')}).dropna()

    current_ratio_ly = excel_data['CURRENT RATIO'].loc[(excel_data['CURRENT RATIO'].index.month == target_date.month) & (excel_data['CURRENT RATIO'].index.year == last_year.year)].transpose()
    current_ratio_ly = current_ratio_ly.rename(columns={current_ratio_ly.columns[0]: 'CURRENT RATIO LY'}).assign(**{'CURRENT RATIO LY':pd.to_numeric(current_ratio_ly.iloc[:, 0], errors='coerce')}).dropna()

    shares = excel_data['SHARES OUTSTANDING'].loc[(excel_data['SHARES OUTSTANDING'].index.month == target_date.month) & (excel_data['SHARES OUTSTANDING'].index.year == target_date.year)].transpose()
    shares = shares.rename(columns={shares.columns[0]: 'SHARES OUTSTANDING'}).assign(**{'SHARES OUTSTANDING':pd.to_numeric(shares.iloc[:, 0], errors='coerce')}).dropna()

    shares_ly = excel_data['SHARES OUTSTANDING'].loc[(excel_data['SHARES OUTSTANDING'].index.month == target_date.month) & (excel_data['SHARES OUTSTANDING'].index.year == target_date.year)].transpose()
    shares_ly = shares_ly.rename(columns={shares_ly.columns[0]: 'SHARES OUTSTANDING LY'}).assign(**{'SHARES OUTSTANDING LY':pd.to_numeric(shares_ly.iloc[:, 0], errors='coerce')}).dropna()

    gross_margin = excel_data['GROSS MARGIN'].loc[(excel_data['GROSS MARGIN'].index.month == target_date.month) & (excel_data['GROSS MARGIN'].index.year == target_date.year)].transpose()
    gross_margin = gross_margin.rename(columns={gross_margin.columns[0]: 'GROSS MARGIN'}).assign(**{'GROSS MARGIN':pd.to_numeric(gross_margin.iloc[:, 0], errors='coerce')}).dropna()

    gross_margin_ly = excel_data['GROSS MARGIN'].loc[(excel_data['GROSS MARGIN'].index.month == target_date.month) & (excel_data['GROSS MARGIN'].index.year == last_year.year)].transpose()
    gross_margin_ly = gross_margin_ly.rename(columns={gross_margin_ly.columns[0]: 'GROSS MARGIN LY'}).assign(**{'GROSS MARGIN LY':pd.to_numeric(gross_margin_ly.iloc[:, 0], errors='coerce')}).dropna()

    asset_turnover = excel_data['ASSET TURNOVER'].loc[(excel_data['ASSET TURNOVER'].index.month == target_date.month) & (excel_data['ASSET TURNOVER'].index.year == target_date.year)].transpose()
    asset_turnover = asset_turnover.rename(columns={asset_turnover.columns[0]: 'ASSET TURNOVER'}).assign(**{'ASSET TURNOVER':pd.to_numeric(asset_turnover.iloc[:, 0], errors='coerce')}).dropna()

    asset_turnover_ly = excel_data['ASSET TURNOVER'].loc[(excel_data['ASSET TURNOVER'].index.month == target_date.month) & (excel_data['ASSET TURNOVER'].index.year == last_year.year)].transpose()
    asset_turnover_ly = asset_turnover_ly.rename(columns={asset_turnover_ly.columns[0]: 'ASSET TURNOVER LY'}).assign(**{'ASSET TURNOVER LY':pd.to_numeric(asset_turnover_ly.iloc[:, 0], errors='coerce')}).dropna()

    px_last = excel_data['PX_LAST MONTHLY'].loc[(excel_data['PX_LAST MONTHLY'].index.month == price_month) & (excel_data['PX_LAST MONTHLY'].index.year == target_date.year)].transpose()
    px_last = px_last.rename(columns={px_last.columns[0]: 'PX_LAST'}).assign(**{'PX_LAST':pd.to_numeric(px_last.iloc[:, 0], errors='coerce')}).dropna()


  #  px_last_ny1 = excel_data['PX_LAST MONTHLY'].loc[(excel_data['PX_LAST MONTHLY'].index.month == price_month) & (excel_data['PX_LAST MONTHLY'].index.year == next_year1.year)].transpose()
  #  px_last_ny2 = excel_data['PX_LAST MONTHLY'].loc[(excel_data['PX_LAST MONTHLY'].index.month == price_month) & (excel_data['PX_LAST MONTHLY'].index.year == next_year2.year)].transpose()
 #   px_last_ny3 = excel_data['PX_LAST MONTHLY'].loc[(excel_data['PX_LAST MONTHLY'].index.month == price_month) & (excel_data['PX_LAST MONTHLY'].index.year == next_year3.year)].transpose()
 #  px_last_ny4 = excel_data['PX_LAST MONTHLY'].loc[(excel_data['PX_LAST MONTHLY'].index.month == price_month) & (excel_data['PX_LAST MONTHLY'].index.year == next_year4.year)].transpose()
 #   px_last_ny5 = excel_data['PX_LAST MONTHLY'].loc[(excel_data['PX_LAST MONTHLY'].index.month == price_month) & (excel_data['PX_LAST MONTHLY'].index.year == next_year5.year)].transpose()
    
    # Merge financial data with the tickers
    year_data = pd.concat([
        year_data, roa, roa_ly, cfo, leverage, leverage_ly, current_ratio, current_ratio_ly,
        shares, shares_ly, gross_margin, gross_margin_ly, asset_turnover, asset_turnover_ly, px_last,
    ], axis=1).dropna()
    
    # Calculate the F-SCORE
    fscore = pd.concat([
        (year_data['ROA'] > 0).astype(int),
        (year_data['CFO'] > 0).astype(int),
        (year_data['ROA'] - year_data['ROA LY'] > 0).astype(int),
        (year_data['CFO'] > year_data['ROA']).astype(int),
        (year_data['LEVERAGE'] < year_data['LEVERAGE LY']).astype(int),
        (year_data['CURRENT RATIO'] - year_data['CURRENT RATIO LY'] > 0).astype(int),
        (year_data['SHARES OUTSTANDING'] - year_data['SHARES OUTSTANDING LY'] <= 0).astype(int),
        (year_data['GROSS MARGIN'] - year_data['GROSS MARGIN LY'] > 0).astype(int),
        (year_data['ASSET TURNOVER'] - year_data['ASSET TURNOVER LY'] > 0).astype(int),
       # year_data['PX_LAST'].astype(float),
     #   year_data['PX_LAST +1'].astype(float),
     #   year_data['PX_LAST +2'].astype(float),
    #    year_data['PX_LAST +3'].astype(float),
    #    year_data['PX_LAST +4'].astype(float),
    #    year_data['PX_LAST +5'].astype(float)

    ], axis=1, keys=['ROA', 'CFO', 'Delta ROA', 'ACCRUALS', 'Delta LEVERAGE', 'Delta CURRENT RATIO',
                    'Delta SHARES', 'Delta GROSS MARGIN', 'Delta ASSET TURNOVER', 'PX_LAST'])
    
   # fscore['F-SCORE'] = fscore.iloc[:, :-1].sum(axis=1)
    fscore['F-SCORE'] = fscore.sum(axis=1)
    fscore = fscore.sort_values(by='F-SCORE', ascending=False)
    
    # Store the dataframes in the dictionaries with the specified data_name
    data_dict[data_name + '_Data'] = year_data
    fscore_dict[data_name + '_FSCORE'] = fscore
    
    return data_dict, fscore_dict

#%% Generate FSCORE using Piotroski's parameters
def calculate_fscore_range(excel_data, start_year, end_year, chosen_price_month, freq='all'):
    DATA = {}
    FSCORE = {}

    quarter_mappings = {'q1': 3, 'q2': 6, 'q3': 9, 'q4': 12}

    for year in range(start_year, end_year + 1):
        if freq == 'all':
            chosen_quarters = [3, 6, 9, 12]
        elif freq in quarter_mappings:
            chosen_quarters = [quarter_mappings[freq]]
        else:
            print("Invalid value for freq. Please choose 'all', 'q1', 'q2', 'q3', or 'q4'.")
            return DATA, FSCORE

        for chosen_quarter in chosen_quarters:
            quarter_label = f'{year}_Q{chosen_quarter // 3}'  # Use integer division (//) to get the desired label
            DATA, FSCORE = calculate_fscore(excel_data, int(year), int(chosen_quarter), chosen_price_month, DATA, FSCORE, quarter_label)

    return DATA, FSCORE

DATA, FSCORE = calculate_fscore_range(excel_data, 2013, 2020, 4, freq='all')



#%% Merge the generated F-SCORE into one DataFrame

def merge_fscore_dataframes(FSCORE):
    merged_df = None  # Initialize the merged dataframe as None

    for key, df in FSCORE.items():
        extracted_df = df[['F-SCORE', 'PX_LAST']]
        extracted_df.rename(columns={'F-SCORE': f'F-SCORE_{key}', 'PX_LAST': f'PX_LAST_{key}'}, inplace=True)

        if merged_df is None:
            merged_df = extracted_df
        else:
            merged_df = pd.concat([merged_df, extracted_df], axis=1)
    return merged_df

merged_df = merge_fscore_dataframes(FSCORE)

#%% Extract Prices for every ticker that we analyse at the buy/sell date

def extract_may_data(merged_df, excel_data, month):
    stock_tickers = merged_df.index
    px_last_monthly = excel_data['PX_LAST MONTHLY']
    px_last_monthly.index = pd.to_datetime(px_last_monthly.index)
    extracted_data = px_last_monthly.loc[px_last_monthly.index.month == month, stock_tickers].transpose()
    return extracted_data

extracted_data = extract_may_data(merged_df, excel_data, 5)

#%%

filtered_dfs = []

filtered_columns = []

# Loop through each dataframe in the FSCORE dictionary
for key, df in FSCORE.items():
    # Filter rows with FSCORE values of 8 and 9
    filtered_df = df[df['F-SCORE'].isin([8, 9])]
    # Extract the F-SCORE column and assign the key as the column name
    filtered_column = filtered_df['F-SCORE'].rename(key)
    # Append the filtered F-SCORE column to the list
    filtered_columns.append(filtered_column)

# Concatenate the filtered F-SCORE columns into a single dataframe

# Concatenate the filtered F-SCORE columns into a single dataframe
xxx = pd.concat(filtered_columns, axis=1)