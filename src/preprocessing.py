"""
Preprocessing functions for the OSMI Mental Health in Tech survey.

Each function handles one column-treatment type described in
feature_config.py. `run_pipeline` ties them together in a sensible order.
Keep these functions pure (df in, df out) so they're easy to test and
to call individually from the notebook while you're iterating.
"""

import pandas as pd
import numpy as np


def rename_columns(df: pd.DataFrame, rename_map: dict) -> pd.DataFrame:
    """Rename long survey-question columns to short snake_case identifiers."""
    return df.rename(columns=rename_map)


def drop_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Drop columns that are redundant, too granular, or unused."""
    existing = [c for c in columns if c in df.columns]
    return df.drop(columns=existing)


def mark_special_na_as_category(df: pd.DataFrame, special_na_map: dict) -> pd.DataFrame:
    """
    Ensure values like 'I don't know' / 'N/A (not currently aware)' are
    treated as their own explicit category and are NOT accidentally
    coerced to NaN later on. Documentation/assertion hook -- extend with
    a dedicated flag column per special value if needed later.
    """
    global_values = special_na_map.get("*", [])
    for col in df.columns:
        col_values = special_na_map.get(col, [])
        values_to_protect = set(global_values) | set(col_values)
        if values_to_protect:
            mask = df[col].isin(values_to_protect)
            # no-op placeholder -- these values pass through unchanged.
            pass
    return df


def clean_age(df: pd.DataFrame, col: str = "age", min_age: int = 18, max_age: int = 75) -> pd.DataFrame:
    """
    Set implausible age values (e.g. 3, 15, 17, 99, 323) to NaN.
    Bounds chosen based on inspecting min/max of the actual distribution --
    see DECISIONS.md for the justification.
    """
    df = df.copy()
    invalid = ~df[col].between(min_age, max_age)
    df.loc[invalid, col] = np.nan
    return df


def bucket_age(df: pd.DataFrame, col: str = "age", new_col: str = "age_group") -> pd.DataFrame:
    """
    Create a human-readable age_group column for cluster interpretation,
    while the cleaned numeric age column remains available for the
    actual clustering/distance calculations.
    """
    df = df.copy()
    bins = [0, 24, 34, 44, 54, 100]
    labels = ["<25", "25-34", "35-44", "45-54", "55+"]
    df[new_col] = pd.cut(df[col], bins=bins, labels=labels)
    return df


def clean_gender(df: pd.DataFrame, col: str = "gender", new_col: str = "gender_cleaned",
                  synonym_map: dict = None, other_label: str = "Other/Non-binary") -> pd.DataFrame:
    """
    Normalize free-text gender responses: lowercase/strip, map common
    synonyms to a small set of labels, and fold unmatched low-frequency
    responses into `other_label`. synonym_map keys must already be
    lowercase/stripped. Extend synonym_map to add explicit categories
    (e.g. 'Non-binary', 'Transgender') rather than routing everything
    to Other, as data volume allows -- see conversation/DECISIONS.md.
    """
    df = df.copy()
    normalized = df[col].astype(str).str.strip().str.lower()

    mapping = synonym_map or {}
    mapped = normalized.map(mapping)

    # Anything not explicitly mapped falls back to the residual category
    df[new_col] = mapped.fillna(other_label)
    return df


def split_direction_and_basis(df: pd.DataFrame, col: str, direction_map: dict, basis_map: dict) -> pd.DataFrame:
    """
    Splits a column with 'direction' (No/Maybe/Yes-ish) and optional
    'basis' (belief vs. experience, or observed vs. experienced)
    into two separate columns. basis_map values may be None for
    categories where the distinction doesn't apply (e.g. 'No', 'Maybe').
    """
    df = df.copy()
    df[f"{col}_direction"] = df[col].map(direction_map)
    df[f"{col}_basis"] = df[col].map(basis_map)
    return df


def apply_direction_basis_columns(df: pd.DataFrame, direction_basis_config: dict) -> pd.DataFrame:
    """
    Applies split_direction_and_basis to every column listed in the config
    (e.g. career_harm, coworker_view, unsupportive_response_observed),
    using each column's own direction_map/basis_map. Drops the original
    column afterward since it's now represented by the two split columns.
    """
    df = df.copy()
    for col, maps in direction_basis_config.items():
        if col not in df.columns:
            continue
        df = split_direction_and_basis(df, col, maps["direction_map"], maps["basis_map"])
        df = df.drop(columns=[col])
    return df


def encode_ordinal(df: pd.DataFrame, ordinal_map: dict) -> pd.DataFrame:
    """
    Encode ordinal columns as integers reflecting their defined order.
    Values not present in the provided order list become NaN -- inspect
    these afterwards (df[col].isnull().sum()) to catch typos or an
    incomplete category list before proceeding.
    """
    df = df.copy()
    for col, order in ordinal_map.items():
        if col not in df.columns:
            continue
        order_map = {category: i for i, category in enumerate(order)}
        df[col] = df[col].map(order_map)
    return df


def encode_nominal(df: pd.DataFrame, nominal_columns: list) -> pd.DataFrame:
    """One-hot encode low-cardinality nominal columns."""
    existing = [c for c in nominal_columns if c in df.columns]
    return pd.get_dummies(df, columns=existing, prefix=existing)


def encode_binary(df: pd.DataFrame, binary_map: dict) -> pd.DataFrame:
    """
    Encode simple binary columns. If a mapping dict is provided for a
    column, apply it; if None, assume the column is already 0/1.
    """
    df = df.copy()
    for col, mapping in binary_map.items():
        if col not in df.columns:
            continue
        if mapping is not None:
            df[col] = df[col].map(mapping)
    return df


def split_multiselect(df: pd.DataFrame, columns: list, delimiter: str = "|") -> pd.DataFrame:
    """
    Turn a pipe-separated multi-select column into one binary flag
    column per distinct value found across the whole column.
    e.g. "diagnosed_conditions" -> diagnosed_conditions__anxiety,
    diagnosed_conditions__mood_disorder, ...
    Drops the original column after expansion.
    """
    df = df.copy()
    for col in columns:
        if col not in df.columns:
            continue

        all_values = set()
        for cell in df[col].dropna():
            all_values.update(v.strip() for v in str(cell).split(delimiter))

        for value in sorted(all_values):
            flag_col = f"{col}__{_slugify(value)}"
            df[flag_col] = df[col].apply(
                lambda cell, v=value: int(
                    isinstance(cell, str) and v in [x.strip() for x in cell.split(delimiter)]
                )
            )

        df = df.drop(columns=[col])
    return df


def extract_text_keyword_features(df: pd.DataFrame, text_config: dict) -> pd.DataFrame:
    """
    Create binary theme-flag features from free-text columns based on
    keyword lists, instead of full TF-IDF -- more interpretable and
    more robust given small sample size / high response variability.
    Drops the original free-text column after extraction.
    """
    df = df.copy()
    for col, cfg in text_config.items():
        if col not in df.columns:
            continue

        text_series = df[col].fillna("").astype(str).str.lower()

        for theme, keywords in cfg.get("keywords", {}).items():
            flag_col = f"{col}__{theme}"
            pattern = "|".join(keywords)
            df[flag_col] = text_series.str.contains(pattern, regex=True).astype(int)

        df = df.drop(columns=[col])
    return df


def _slugify(value: str) -> str:
    """Turn a category label into a safe column-name suffix."""
    return (
        value.lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace(",", "")
        .replace("/", "_")
        .replace("-", "_")
    )


def run_pipeline(df: pd.DataFrame, config) -> pd.DataFrame:
    """
    Apply all preprocessing steps in a sensible order:
    rename -> drop -> mark special NA -> age cleaning/bucketing ->
    gender cleaning -> multiselect split -> text keyword extraction ->
    direction/basis splits -> ordinal encode -> binary encode ->
    nominal one-hot encode.
    """
    df = rename_columns(df, config.COLUMN_RENAME_MAP)
    df = drop_columns(df, config.DROP_COLUMNS)
    df = mark_special_na_as_category(df, config.SPECIAL_NA_AS_CATEGORY)

    df = clean_age(df, **config.AGE_CLEANING)
    df = bucket_age(df, **config.AGE_BUCKETING)

    df = clean_gender(df, **config.GENDER_CLEANING)

    df = split_multiselect(df, config.MULTISELECT_COLUMNS)
    df = extract_text_keyword_features(df, config.TEXT_COLUMNS)
    df = apply_direction_basis_columns(df, config.DIRECTION_BASIS_COLUMNS)

    df = encode_ordinal(df, config.ORDINAL_COLUMNS)
    df = encode_binary(df, config.BINARY_COLUMNS)
    df = encode_nominal(df, config.NOMINAL_COLUMNS)
    return df