import acquire
import pandas as pd
import prepare

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

    # remove all rows where any column has z score gtr than 3
    non_quants = ['yearbuilt', 'fips', 'parcelid']
    quants = df.drop(columns=non_quants).columns
    #print(quants)
    df = prepare.remove_outliers(3.5, quants, df)

    # see if sqr feet makes sense
    df = clean_sqr_feet(df)

    return df

def minimum_sqr_ft(df):
    # min square footage for type of room
    bathroom_min = 10
    bedroom_min = 70
    
    # total MIN sqr feet
    total = df.bathroomcnt * bathroom_min + df.bedroomcnt * bedroom_min

    # return MIN sqr feet
    return total

def clean_sqr_feet(df):
    # get MIN sqr ft
    min_sqr_ft = minimum_sqr_ft(df)

    # return df with sqr_ft >= min_sqr_ft
    # change 'sqr_ft' to whichever name you have for sqr_ft in df
    return df[df.sqr_ft >= min_sqr_ft]

def wrangle_zillow():
    # aquire zillow data from mysql or csv
    zillow = acquire.get_zillow_data()

    # clean zillow data
    zillow = clean_zillow(zillow)

    return zillow
