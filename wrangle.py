import acquire
import pandas as pd

def clean_zillow(df):
    # drop nulls and extra column
    df = df.dropna()
    df = df.drop(columns='Unnamed: 0')

    # readability
    df = df.rename(columns={'calculatedfinishedsquarefeet': 'sqr_ft'})

    # convert yearbuilt/fips to ints
    cols = ['yearbuilt', 'fips']
    df[cols] = df[cols].astype('int64')

    # limit houses to include only >= 70 sqr ft 
    # (most prevelant minimum required sqr ft by state)
    df = df[df.sqr_ft >= 70]

    # exclude houses with bthroom/bedroomcnts of 0
    df = df[df.bedroomcnt != 0]
    df = df[df.bathroomcnt != 0.0]

    return df

def wrangle_zillow():
    # aquire zillow data from mysql or csv
    zillow = acquire.get_zillow_data()

    # clean zillow data
    zillow = clean_zillow(zillow)

    return zillow
