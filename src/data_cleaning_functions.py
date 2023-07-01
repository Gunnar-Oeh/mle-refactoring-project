### Data Cleaning Functions
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# Constant for sloppy degree to km calculations
constant_degr_km = 6378/360

# Imputation for waterfront and view
# Can be done with .fillna(0, inplace=True)

### Drop Houses with an irregular Bedrooms/Bathroom ratio. Outliers > 8
def bath_bed_ratio_outlier(df, outlier_ratio = 8):
    df_temp = df.copy()
    df_temp["bedrooms_per_bath"] =  df_temp.bedrooms / df_temp.bathrooms
    ind = df_temp["bedrooms_per_bath"] <= outlier_ratio
    df_temp = df_temp.loc[ind]
    return df_temp

### Calculate SQFT Basement
def sqft_basement(df):
    df_temp = df.copy()
    df_temp.eval('sqft_basement = sqft_living - sqft_above', inplace=True)
    return df_temp

### Determine Last known change
def last_known_change(df):
    df_temp = df.copy()
    # We will create an empty list in which we will store values
    last_known_change_lst = []

    # For each row in our data frame, we look at what is in the column "yr_renovated".
    for idx, yr_re in df_temp.yr_renovated.items():
        # if "yr_renovated" is 0 or contains no value, we store the year of construction of the house in our empty listes ab
        if str(yr_re) == 'nan' or yr_re == 0.0:
            last_known_change_lst.append(df_temp.yr_built[idx])
        # if there is a value other than 0 in the column "yr_renovated", we transfer this value into our new list
        else:
            last_known_change_lst.append(int(yr_re))

    # We create a new column and take over the values of our previously created list
    df_temp['last_known_change'] = last_known_change_lst

    # We delete the "yr_renovated" and "yr_built" columns
    df_temp.drop(["yr_renovated", "yr_built"], axis=1, inplace=True)

    return df_temp

### Function for calculating Distance to wealth center
def dist_wealth_centre(df, coords, constant_degr_km = constant_degr_km):
    X_temp = df.copy()
    # Constant for sloppy transformation

    # Absolute difference of latitude between centre and property
    X_temp['delta_lat'] = np.absolute(coords["lat"]- X_temp['lat'])
    # Absolute difference of longitude between centre and property
    X_temp['delta_long'] = np.absolute(coords["long"]-X_temp['long'])
    # Distance between centre and property
    X_temp['center_wealth_distance']= ((X_temp['delta_long'] * np.cos(np.radians(coords["lat"]))) ** 2 + 
                                       X_temp['delta_lat']**2) ** (1/2) * 2 * np.pi * constant_degr_km
    
    X_temp.drop(["delta_lat", "delta_lon"], axis = 1, inplace = True)
    return X_temp

# Distance from One Point to Another
def dist(long, lat, ref_long, ref_lat, constant_degr_km = constant_degr_km):
    '''dist computes the distance in km to a reference location. Input: long and lat of 
    the location of interest and ref_long and ref_lat as the long and lat of the reference location'''
    delta_long = long - ref_long
    delta_lat = lat - ref_lat
    delta_long_corr = delta_long * np.cos(np.radians(ref_lat))
    return ((delta_long_corr)**2 +(delta_lat)**2) ** (1/2) * 2 * np.pi * constant_degr_km


# Distance to the Water of every entry in the dataframe
def dist_water(df):
    X_temp= df.copy()

    # All houses with "waterfront" as DF
    X_temp = X_temp.query('waterfront == 1')

    water_distance = []
    # For each row in our data frame we now calculate the distance to all the houses at the seafront
    for idx, lat in X_temp.lat.items():
        ref_list = []
        for x,y in zip(list(df_water.long), list(df_water.lat)):
            ref_list.append(dist(X_temp.long[idx], X_temp.lat[idx],x,y).min())
        
    water_distance.append(min(ref_list))
    X_temp["water_dist_km"] = water_distance
    return X_temp




