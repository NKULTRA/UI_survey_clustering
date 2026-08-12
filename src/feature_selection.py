import pandas as pd
import numpy as np
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


def apply_correlation_filter(df, threshold=0.9):
    df_model_input = df.drop(columns=["age_group"], errors="ignore")
    corr_matrix = df_model_input.corr(method='spearman')

    # Only the upper triangle, excluding the diagonal, so each pair
    # appears once (the matrix is symmetric, and the diagonal is
    # always 1.0 self-correlation, not a real relationship)
    upper_triangle = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )

    high_corr_pairs = (
        upper_triangle.stack()
        .reset_index()
        .rename(columns={"level_0": "feature_a", "level_1": "feature_b", 0: "correlation"})
    )
    high_corr_pairs = high_corr_pairs[high_corr_pairs["correlation"].abs() > threshold]
    high_corr_pairs = high_corr_pairs.sort_values("correlation", key=abs, ascending=False)

    return corr_matrix, high_corr_pairs