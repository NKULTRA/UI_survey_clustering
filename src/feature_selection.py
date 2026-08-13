"""
Feature selection diagnostics for the OSMI Mental Health in Tech survey.

Two of these functions expect a different pipeline stage than the other
two -- this matters, calling them on the wrong stage will error or give
meaningless results:

  - apply_chi_square, apply_mutual_information
      -> run on prepare_for_feature_selection()'s output. Column names
         referenced in FEATURE_FILTER_GROUPS (e.g. "mental_health_benefits")
         still exist at that stage, since one-hot encoding hasn't run yet.

  - apply_variance_threshold, apply_correlation_filter
      -> run on run_pipeline()'s output (df_processed). Both need purely
         numeric input (MinMaxScaler, .corr()), which only exists after
         one-hot encoding has fully run.
"""

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from sklearn.metrics import mutual_info_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import VarianceThreshold


def apply_chi_square(df, feature_filter_groups):
    """
    Chi-square test of independence for each configured feature pair.
    Expects prepare_for_feature_selection()'s output (pre-one-hot).
    pd.crosstab drops NaN rows automatically (pairwise per pair, not
    globally), so no explicit dropna() needed here.

    Returns: dict {(col_a, col_b): (chi2_stat, p_value, dof, expected)}
    Low p-value -> reject independence -> features are significantly
    associated (candidate for redundancy, unless the pair is one of the
    "expected real relationship" ones -- see FEATURE_FILTER_GROUPS notes).
    Always sanity-check the `expected` array before trusting a result:
    cells below ~5 mean the chi-square approximation is unreliable
    (small/sparse contingency table).
    """
    results = {}

    for col_a, col_b in feature_filter_groups:
        contingency_table = pd.crosstab(df[col_a], df[col_b])
        chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)
        results[(col_a, col_b)] = (chi2_stat, p_value, dof, expected)

    return results


def apply_mutual_information(df, feature_filter_groups):
    """
    Pairwise Mutual Information for each configured feature pair.
    Expects prepare_for_feature_selection()'s output (pre-one-hot).
    Explicit dropna() per pair, since mutual_info_score (unlike
    pd.crosstab) doesn't handle NaN safely on its own.

    Returns: dict {(col_a, col_b): mi_score}
    No fixed upper bound and no built-in significance test -- use for
    RANKING pairs relative to each other / cross-checking against
    chi-square results, not for picking an absolute "high MI" threshold.
    """
    results = {}

    for col_a, col_b in feature_filter_groups:
        paired = df[[col_a, col_b]].dropna()
        mi_score = mutual_info_score(paired[col_a], paired[col_b])
        results[(col_a, col_b)] = mi_score

    return results


def apply_variance_threshold(df, threshold=0.0099):
    """
    Variance thresholding across the FULL feature matrix.
    Expects run_pipeline()'s output (df_processed, fully numeric).

    Min-max scales every column to [0,1] first, so binary/ordinal/
    continuous features become comparable on the same scale before
    applying one threshold -- without this, raw variance would be
    scale-dependent (e.g. unscaled age would dwarf any binary column).

    Threshold default (0.0099) derived from: "a flag reported by fewer
    than ~1% of respondents is too rare to plausibly define a distinct
    cluster segment" -> p=0.01 -> variance = p*(1-p) ~= 0.0099 for a
    binary feature at that rate. Adjust this reasoning (not just the
    number) if a different practical threshold is wanted.

    age_group is dropped first -- it's a categorical profiling-only
    column (not meant for the model matrix), not something to encode.

    fillna(0) is a TEMPORARY placeholder for this diagnostic only --
    NOT the actual imputation strategy for the final model input.

    Returns: DataFrame [feature, variance, kept], sorted ascending.
    """
    df_model_input = df.drop(columns=["age_group"], errors="ignore")

    df_filled = df_model_input.fillna(0)

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
    """
    Full pairwise Spearman correlation matrix + extraction of pairs
    above |threshold|. Expects run_pipeline()'s output (df_processed,
    fully numeric).

    Spearman (rank-based), not Pearson, since it's valid for ordinal
    data (only assumes a genuine order, not equal-sized intervals) --
    unlike Pearson, which assumes roughly continuous/linear relationships.

    .corr() handles NaN via pairwise deletion automatically -- no
    fillna() needed here (unlike apply_variance_threshold).

    age_group dropped first, same reasoning as apply_variance_threshold.

    Returns: (full corr_matrix, high_corr_pairs DataFrame). Only the
    upper triangle (excluding the diagonal) is extracted into pairs,
    since the matrix is symmetric and the diagonal is always a
    meaningless 1.0 self-correlation.
    """
    df_model_input = df.drop(columns=["age_group"], errors="ignore")
    corr_matrix = df_model_input.corr(method='spearman')

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