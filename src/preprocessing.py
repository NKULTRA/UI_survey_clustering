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
    coerced to NaN later on. Since they're already strings distinct from
    true NaN, this function mainly documents/asserts that intent and
    gives you one place to extend the list. If you later use
    pd.isnull()-based logic anywhere, exclude these values explicitly.
    """
    global_values = special_na_map.get("*", [])
    for col in df.columns:
        col_values = special_na_map.get(col, [])
        values_to_protect = set(global_values) | set(col_values)
        if values_to_protect:
            mask = df[col].isin(values_to_protect)
            # no-op transformation placeholder: these values pass through
            # unchanged. This function exists to make the decision
            # explicit and inspectable, and as a hook if you later want
            # e.g. a dedicated "_uncertain" flag column instead:
            # df[f"{col}_uncertain"] = mask
            pass
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

        # Collect the set of distinct individual values across all rows
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
    rename -> drop -> mark special NA -> multiselect split ->
    text keyword extraction -> ordinal encode -> binary encode ->
    nominal one-hot encode.
    """
    df = rename_columns(df, config.COLUMN_RENAME_MAP)
    df = drop_columns(df, config.DROP_COLUMNS)
    df = mark_special_na_as_category(df, config.SPECIAL_NA_AS_CATEGORY)
    df = split_multiselect(df, config.MULTISELECT_COLUMNS)
    df = extract_text_keyword_features(df, config.TEXT_COLUMNS)
    df = encode_ordinal(df, config.ORDINAL_COLUMNS)
    df = encode_binary(df, config.BINARY_COLUMNS)
    df = encode_nominal(df, config.NOMINAL_COLUMNS)
    return df