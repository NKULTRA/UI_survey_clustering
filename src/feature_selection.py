import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency
from sklearn.metrics import mutual_info_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import (
    mutual_info_classif, VarianceThreshold, SelectKBest
)


# Chi-square test for feature selection
def apply_chi_square(df, FEATURE_FILTER_GROUPS):
    results = {}

    for col_a, col_b in FEATURE_FILTER_GROUPS:
        contingency_table = pd.crosstab(df[col_a], df[col_b])
        chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        results[(col_a, col_b)] = (chi2_stat, p_value, dof, expected)

    return results


# Mutual Information for feature selection
def apply_mutual_information(df, FEATURE_FILTER_GROUPS):
    results = {}

    for col_a, col_b in FEATURE_FILTER_GROUPS:
        paired = df[[col_a, col_b]].dropna()
        mi_score = mutual_info_score(paired[col_a], paired[col_b])
        results[(col_a, col_b)] = mi_score

    return results


# Variance Threshold for feature selection
def apply_variance_threshold(df, threshold=0.0099):
    df_model_input = df.drop(columns=["age_group"], errors="ignore")
    # errors="ignore" so this doesn't crash if age_group isn't present
    # (e.g. if called on a df that hasn't gone through bucket_age)

    df_filled = df_model_input.fillna(0)  # TEMPORARY placeholder

    X_minmax = MinMaxScaler().fit_transform(df_filled)

    selector = VarianceThreshold(threshold=threshold)
    selector.fit(X_minmax)

    results = pd.DataFrame({
        'feature': df_model_input.columns,
        'variance': selector.variances_,
        'kept': selector.get_support(),
    }).sort_values('variance')

    return results



def apply_correlation_filter():

    # for the report itself it probably also makes sense to include a correlation matrix heatmap of the features, 
    # so you can visually show which features are highly correlated and justify dropping one of them.

    pass