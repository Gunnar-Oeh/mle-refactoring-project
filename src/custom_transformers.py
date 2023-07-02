from src.data_cleaning_functions import constant_degr_km, dist, outlier_ratio
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

###############################
### Define Transformer CLasses
###############################
class Restore_Names_Transformer(BaseEstimator, TransformerMixin):
    '''If A ColumnTransformer-Pipeline is applied beforehand with
    .set_output(transform = "pandas") a df will be returned, but column
    names will be preceeded with the name of the Pipeline__ or remainder__
    thus we remove those preceding additions, to make the column indexing
    used in the following Transformers work again'''
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        X_temp = X.copy()
        map_names = {}
        for nam in X_temp.columns:
            map_names[nam] = nam.split("__")[1]

        X_temp.rename(mapper = map_names, axis = 1, inplace = True)
        return X_temp

class Bath_Bed_Transformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    # If one were to determine the ratio, which defines outliers from the test data dynamically
    # this would need to be done within fit?
    
    def transform(self, X, y = None):
        X_temp = X.copy()
        X_temp["bedrooms_per_bath"] =  X_temp.bedrooms / X_temp.bathrooms
        ind = X_temp["bedrooms_per_bath"] <= outlier_ratio
        X_temp = X_temp.loc[ind]
        return X_temp
    
class Sqft_Basement_Transformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        X_temp = X.copy()
        X_temp.eval('sqft_basement = sqft_living - sqft_above', inplace=True)
        return X_temp
    
class Last_Change_Transformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        X_temp = X.copy()
    # We will create an empty list in which we will store values
        last_known_change_lst = []

    # For each row in our data frame, we look at what is in the column "yr_renovated".
        for idx, yr_re in X_temp.yr_renovated.items():
        # if "yr_renovated" is 0 or contains no value, we store the year of construction of the house in our empty listes ab
            if str(yr_re) == 'nan' or yr_re == 0.0:
                last_known_change_lst.append(X_temp.yr_built[idx])
        # if there is a value other than 0 in the column "yr_renovated", we transfer this value into our new list
            else:
                last_known_change_lst.append(int(yr_re))
        
        X_temp['last_known_change'] = last_known_change_lst
        # We delete the "yr_renovated" and "yr_built" columns
        X_temp.drop(["yr_renovated", "yr_built"], axis=1, inplace=True)
        return X_temp
    
class Price_sqft_Transformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        X_temp = X.copy()
        X_temp['sqft_price'] = (X_temp.price/(X_temp.sqft_living + X_temp.sqft_lot)).round(2)
        return X_temp
    
class Distance_Wealth_Transformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        # Find location of highest wealth from the Test-Data
        ind = X['price']==X['price'].max()
        self.coordinates_max_price = {"lat": X.lat[ind].item(), "long":X.long[ind].item()}
        return self
    
    def transform(self, X, y = None):
        X_temp = X.copy()

        # Absolute difference of latitude between centre and property
        X_temp['delta_lat'] = np.absolute(self.coordinates_max_price["lat"]- X_temp['lat'])
        # Absolute difference of longitude between centre and property
        X_temp['delta_long'] = np.absolute(self.coordinates_max_price["long"]-X_temp['long'])
        # Distance between centre and property
        X_temp['center_wealth_distance']= ((X_temp['delta_long'] * np.cos(np.radians(self.coordinates_max_price["lat"]))) ** 2 + 
                                           X_temp['delta_lat']**2) ** (1/2) * 2 * np.pi * constant_degr_km
    
        X_temp.drop(["delta_lat", "delta_long"], axis = 1, inplace = True)
        return X_temp

class Distance_Water_Transfomer(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        X_temp = X.copy()
        # All houses with "waterfront" are added to the list
        self.X_water = X_temp.query('waterfront == 1')
        return self
    
    def transform(self, X, y = None):
        X_temp = X.copy()
        water_distance = []
        # For each row in our data frame we now calculate the distance to all the houses at the seafront
        for idx in X_temp.index: # lat not necessary
            ref_list = []
        
            # Find the smallest distance among all distances for house idx
            for x,y in zip(list(self.X_water.long), list(self.X_water.lat)):
                dist_idx_water = dist(X_temp.long[idx], X_temp.lat[idx],x,y)  
                ref_list.append(dist_idx_water.min())
        
            water_distance.append(min(ref_list))
        X_temp["water_dist_km"] = water_distance
        return X_temp
