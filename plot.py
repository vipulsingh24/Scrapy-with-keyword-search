import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def plot_yearwise(df, name):
    assert isinstance(df, pd.DataFrame), "Not a DataFrame"
    assert isinstance(name, str), "Second argument should be name of newspaper to be plot, str."

    df1 = df.resample('AS').count() # AS-Year Start
    fig, ax = plt.subplots(figsize=(16, 8))
    plt.yticks(np.arange(df1['Title'].min(), df1['Title'].max() + 20, 20))
    plt.xticks(df1.index)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # plt.grid(True)
    ax.grid(color='black', zorder=0)
    ax.bar(df1.index, df1['Title'], width=100, zorder=3)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of articles', fontsize=12)
    plt.title("Number of articles published by "+name+" year-wise")
    # plt.show()
    plt.savefig('Plots/Yearly/'+name+'.png')

def plot_monthwise(df, name):
    assert isinstance(df, pd.DataFrame), "Not a DataFrame"
    assert isinstance(name, str), "Second argument should be name of newspaper to be plot, str."
    df_m = df.resample('M').count()
    df_semi = df.resample('2Q').count() # Resample data to Semi-Annual
    fig, ax = plt.subplots(figsize=(16, 10))
    plt.yticks(np.arange(df_m['Title'].min(), df_m['Title'].max() + 1, 2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    ax.bar(df_m.index, df_m['Title'], width=20, zorder=10)
    plt.xticks(df_semi.index, rotation=70)
    plt.xlabel('Date (Month)', fontsize=12)
    plt.ylabel('Number of articles', fontsize=12)
    plt.title("Number of articles published by " + name + " month-wise")
    # plt.show()
    plt.savefig('Plots/Monthly/'+name+'.png')


# Functions to clean dates
def TOI(df):
    '''
    Clean dates of Times of India Newspaper and bring it in proper date format(YYYY-mm-dd)
    :param df: Dataframe on which cleaning is to be done
    :return: Dataframe with Date as Index and proper format
    '''
    assert isinstance(df, pd.DataFrame), "Not a DataFrame"
    # Drop null values
    df.dropna(how='any', axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Cleaning Dates
    df['Date'] = df['Date'].apply(lambda x: re.findall(r'[a-zA-Z]{3}\s[0-9]{1,2},\s[0-9]{4}', x))
    df['Date'] = df.Date.apply(', '.join)
    df['Date'] = df['Date'].str.replace(',', '').astype('str')
    df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%b %d %Y'))
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.reset_index(drop=True).set_index('Date')
    return df

def IE(df):
    '''
    Clean dates of Indian Express Newspaper and bring it in proper date format(YYYY-mm-dd)
    :param df: Dataframe on which cleaning is to be done
    :return: Dataframe with Date as Index and proper format
    '''
    assert isinstance(df, pd.DataFrame), "Not a DataFrame"
    # Drop null values
    df.dropna(how='any', axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Cleaning Dates
    df['Date'] = df['Date'].apply(lambda x: re.findall(r'[a-zA-Z]{3}\s[0-9]{1,2}(?:,)*(?:\s)*[0-9]{4}', x))
    df['Date'] = df.Date.apply(''.join)
    df['Date'] = df['Date'].str.replace(',', '').astype('str')
    df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%b %d %Y'))
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.reset_index(drop=True).set_index('Date')
    return df

def TheHindu(df):
    '''
    Clean dates of The Hindu Newspaper and bring it in proper date format(YYYY-mm-dd)
    :param df: Dataframe on which cleaning is to be done
    :return: Dataframe with Date as Index and proper format
    '''
    assert isinstance(df, pd.DataFrame), "Not a DataFrame"
    # Drop null values
    df.dropna(how='any', axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Cleaning Dates
    df['Date'] = df['Date'].apply(lambda x: re.findall(r'[a-zA-Z]{3,9}\s[0-9]{1,2}(?:,)*(?:\s)*[0-9]{4}', x))
    df['Date'] = df.Date.apply(''.join)
    df['Date'] = df['Date'].str.replace(',', '').astype('str')
    df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%B %d %Y') if len(x) > 11 else datetime.strptime(x, '%b %d %Y'))
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.reset_index(drop=True).set_index('Date')
    return df


if __name__ == "__main__":
    # df = pd.read_csv('data/HIV_TOI.csv')
    # df = TOI(df)
    # df = pd.read_csv('data/HIV_IE.csv')
    # df = IE(df)
    df = pd.read_csv('data/HIV_TH.csv')
    df = TheHindu(df)
    # plot_yearwise(df, 'TOI')
    # plot_monthwise(df, 'TOI')
    # plot_yearwise(df, 'Indian_Express')
    # plot_monthwise(df, 'Indian_Express')
    plot_yearwise(df, 'The Hindu')
    plot_monthwise(df, 'The Hindu')
    print(df.head())