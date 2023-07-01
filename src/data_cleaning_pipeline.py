### Into Transformers
class Bath_Bed_Transformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    # If one were to determine the ratio, which defines outliers from the test data dynamically
    # this would need to be done within fit?
    
    def transform(self, X, y = None):
        return bath_bed_ratio_outlier(X)
    
class Sqft_Basement_Transformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        return sqft_basement(X)
    
class Last_Change_Transformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        return last_known_change(X)
    
class Price_sqft_Transformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        X_temp = X.copy()
        X_temp['sqft_price'] = (X_temp.price/(X_temp.sqft_living + X_temp.sqft_lot)).round(2)
        return X_temp
    
class Distance_Wealth_Transformer(self, X, y = None):
    def fit(self, X, y = None):
        # Find location of highest wealth from the Test-Data
        ind = X['price']==X['price'].max()
        self.coordinates_max_price = {"lat": X.lat[ind], "long":X.long[ind]}
        return self
    
    def transform(self, X, y = None):
        return dist_wealth_centre(X)

class Distance_Water_Transfomer(self, X, y = None):
    def fit(self, X, y = None):
        X_temp = X.copy
        # All houses with "waterfront" are added to the list
        self.water_list= X_temp.query('waterfront == 1')
        return self
    
    def transform(self, X, y = None):
        X_temp = X.copy

        
        return X_temp