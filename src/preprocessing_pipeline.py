from src.custom_transformers import *
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import numpy as np

# Top Level - as a new class without any inheritance.
# Lists of columns for which the different pipelines are applied -> will later be given as self.attributes to the methods
class PreprocessingKingCountyData():
    def __init__(self):
        self.imputed_features = []

        ### Impute Values
        self.impute_pipeline = Pipeline([
            ('impute_nan', SimpleImputer(strategy='constant', fill_value=0))
        ])

        ### DataCleaning Pipeline - Applied to all columns - One Transformer after the other
        ### DF -> tranforer_1(DF) -> DF1 -> transformer_2(DF1) -> ... -> DF_n
        self.data_cleaning_pipeline = Pipeline([
            ('bedrooms_per_bath_outlier', Bath_Bed_Transformer()),
            ('calculate_sqft_basement', Sqft_Basement_Transformer()),
            ('define_last_change', Last_Change_Transformer()),
            ('price_per_sqft', Price_sqft_Transformer()),
            ('distance_to_wealth_centre', Distance_Wealth_Transformer()),
            ('distance_to_waterfront', Distance_Water_Transfomer())
        ])

        ### Would include several Pipelines, if there were several sets of features
        ### to be handled differently for imputation, scaling, transforming
        self.column_imputer = ColumnTransformer([
            ('just_imputing', self.impute_pipeline, self.imputed_features)
        ], remainder='passthrough')

        # Imputing ColumnTransformer which allows for choosing columns
        # and data_cleaning_Pipeline with sequential handling of the whole df applied into Pipelin
        self.full_pipeline = Pipeline([
            ('imputing', self.column_imputer()),
            ('data_cleaning', self.data_cleaning_pipeline())
        ])

    ### _fit_transform method -> to apply onto training data and potentially save values for test-data
    def preprocess_fit_transform(self, df, imputed_features):
        self.imputed_features = imputed_features
        return self.full_pipeline.fit_transform(df)
    
    ### transform to apply onto test data
    def preprocess_transform(self, df):
        return self.full_pipeline.transform(df)    
