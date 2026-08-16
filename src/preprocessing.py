"""
Preprocessing functions for the OSMI Mental Health in Tech survey.

Each function handles one column-treatment type described in
feature_config.py. `run_pipeline` ties them together in a sensible order.
Keep these functions pure (df in, df out) so they're easy to test and
to call individually from the notebook while you're iterating.
"""

import pandas as pd
import numpy as np


def bucket_top_n_categories(df: pd.DataFrame, col: str, top_categories: list, other_label: str = "Other") -> pd.DataFrame:
    """
    Collapse a high-cardinality categorical column down to its top N
    categories (given explicitly as top_categories) plus a residual
    other_label for everything else. Useful for columns like country_live
    where the raw data has a long tail of near-single-count categories
    that would otherwise explode one-hot dimensionality.
    """
    df = df.copy()
    df[col] = df[col].where(df[col].isin(top_categories), other=other_label)
    return df


def normalize_raw_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize raw column headers before renaming: replace non-breaking
    spaces (\\xa0, common in scraped/exported survey data and invisible
    in most editors) with regular spaces, collapse repeated whitespace,
    and strip leading/trailing whitespace. Run this BEFORE rename_columns
    so COLUMN_RENAME_MAP's keys (plain ASCII strings) match reliably --
    otherwise a column with a hidden \\xa0 silently fails to rename and
    skips all downstream processing.
    """
    df = df.copy()
    new_columns = (
        df.columns
        .str.replace("\xa0", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    df.columns = new_columns
    return df


def rename_columns(df: pd.DataFrame, rename_map: dict) -> pd.DataFrame:
    """Rename long survey-question columns to short snake_case identifiers."""
    return df.rename(columns=rename_map)


def drop_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Drop columns that are redundant, too granular, or unused."""
    existing = [c for c in columns if c in df.columns]
    return df.drop(columns=existing)


def extract_special_na_flags(df: pd.DataFrame, special_na_map: dict) -> pd.DataFrame:
    """
    For any column containing a value from special_na_map, create a new
    '{col}_special' column holding that value as its own category
    (NaN elsewhere) -- so it's preserved as data rather than silently
    disappearing into NaN when encode_ordinal/encode_binary run on the
    original column afterward.
    """
    df = df.copy()
    global_values = set(special_na_map.get("*", []))

    for col in df.columns:
        col_values = set(special_na_map.get(col, []))
        values_to_protect = global_values | col_values
        if not values_to_protect:
            continue

        mask = df[col].isin(values_to_protect)
        if mask.any():
            df[f"{col}_special"] = df[col].where(mask, other=np.nan)

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
    actual clustering/distance calculations. age_group is PROFILING-ONLY --
    always excluded from the final model matrix (see fill_remaining_with_mean's
    exclude_cols usage, and drop it explicitly before scaling/clustering).
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
    lowercase/stripped. Drops the original raw column afterward, since
    it's superseded by new_col -- do NOT also add `col` to DROP_COLUMNS
    in the config, since DROP_COLUMNS runs earlier in the pipeline than
    this function and would remove the column before it can be read here.
    """
    df = df.copy()
    normalized = df[col].astype(str).str.strip().str.lower()

    mapping = synonym_map or {}
    mapped = normalized.map(mapping)

    df[new_col] = mapped.fillna(other_label)
    df = df.drop(columns=[col])
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
    Applies split_direction_and_basis to every column listed in the config,
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
    """
    One-hot encode low-cardinality nominal columns. Builds clean,
    slugified column names (reusing the same _slugify helper as
    split_multiselect / encode_special_flags) instead of relying on
    pd.get_dummies' default naming, which would otherwise embed the raw
    category text -- including spaces, slashes, parentheses, etc. --
    directly into the column name.
    """
    df = df.copy()
    existing = [c for c in nominal_columns if c in df.columns]

    for col in existing:
        distinct_values = df[col].dropna().unique()
        new_columns = {}
        for value in distinct_values:
            flag_col = f"{col}_{_slugify(str(value))}"
            new_columns[flag_col] = (df[col] == value).astype(int)

        df = df.drop(columns=[col])
        df = pd.concat([df, pd.DataFrame(new_columns, index=df.index)], axis=1)

    return df


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


def canonicalize_multiselect_values(df: pd.DataFrame, canonicalization_map: dict,
                                     delimiter: str = "|", other_label: str = "Other") -> pd.DataFrame:
    """
    For each configured column, splits each cell on delimiter and maps
    every individual item (case-insensitively) to its canonical label
    via canonicalization_map[col]. Items mapped to "" (explicitly routed
    to the residual bucket) or not found in the map at all fall back to
    other_label. Deduplicates canonical items within a cell and rejoins
    with delimiter, so split_multiselect can operate on clean, consolidated
    categories afterward instead of raw free-text/spelling variants.

    Must run BEFORE split_multiselect in the pipeline.
    """
    df = df.copy()
    for col, value_map in canonicalization_map.items():
        if col not in df.columns:
            continue

        def canonicalize_cell(cell):
            if not isinstance(cell, str):
                return cell
            items = [v.strip() for v in cell.split(delimiter)]
            canonical_items = []
            for item in items:
                canonical = value_map.get(item.lower())
                if not canonical:  # None (unmapped) or "" (explicitly routed to Other)
                    canonical = other_label
                if canonical not in canonical_items:
                    canonical_items.append(canonical)
            return delimiter.join(canonical_items) if canonical_items else np.nan

        df[col] = df[col].apply(canonicalize_cell)
    return df


def split_multiselect(df: pd.DataFrame, columns: list, delimiter: str = "|") -> pd.DataFrame:
    """
    Turn a pipe-separated multi-select column into one binary flag
    column per distinct value found across the whole column.
    Drops the original column after expansion.

    Builds all new flag columns in a dict first and attaches them via a
    single pd.concat, rather than inserting one column at a time in a
    loop -- avoids pandas' "highly fragmented DataFrame" performance
    warning, which shows up here since some of these columns (e.g.
    work_position, diagnosed_conditions) produce many distinct flags.
    """
    df = df.copy()
    for col in columns:
        if col not in df.columns:
            continue

        all_values = set()
        for cell in df[col].dropna():
            all_values.update(v.strip() for v in str(cell).split(delimiter))

        new_columns = {}
        for value in sorted(all_values):
            flag_col = f"{col}__{_slugify(value)}"
            new_columns[flag_col] = df[col].apply(
                lambda cell, v=value: int(
                    isinstance(cell, str) and v in [x.strip() for x in cell.split(delimiter)]
                )
            )

        df = df.drop(columns=[col])
        df = pd.concat([df, pd.DataFrame(new_columns, index=df.index)], axis=1)
    return df


def extract_text_keyword_features(df: pd.DataFrame, text_config: dict) -> pd.DataFrame:
    """
    Create binary theme-flag features from free-text columns based on
    keyword lists, instead of full TF-IDF.
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
        .replace("'", "")
        .replace("’", "")  # curly apostrophe variant, just in case
    )


def encode_special_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
    One-hot encode any auto-generated '_special' columns created by
    extract_special_na_flags (e.g. medical_leave_request_special holding
    "I don't know"). Builds clean, slugified column names (reusing the
    same _slugify helper as split_multiselect) instead of relying on
    pd.get_dummies' default naming, which would otherwise embed the raw
    category text -- including special characters like apostrophes,
    slashes, and parentheses -- directly into the column name.
    """
    df = df.copy()
    special_cols = [c for c in df.columns if c.endswith("_special")]
    if not special_cols:
        return df

    for col in special_cols:
        distinct_values = df[col].dropna().unique()
        new_columns = {}
        for value in distinct_values:
            flag_col = f"{col}_{_slugify(str(value))}"
            new_columns[flag_col] = (df[col] == value).astype(int)

        df = df.drop(columns=[col])
        df = pd.concat([df, pd.DataFrame(new_columns, index=df.index)], axis=1)

    return df


def impute_structural_missingness(df: pd.DataFrame, structural_config: list, verbose: bool = True) -> pd.DataFrame:
    """
    For each {gate_col, gate_value, gated_columns} entry in structural_config,
    handles columns whose missingness is explained by survey skip-logic
    (e.g. previous_employers_* questions only asked if previous_employers==1).

    For each gated_col:
      1. If cfg.get("create_flag", True) is True, creates a
         '{gated_col}_not_applicable' flag (1 = was actually NaN) --
         preserves the TRUE reason for missingness. Set create_flag=False
         for a group when its flags would be a near-perfect duplicate of
         gate_col itself (mathematically guaranteed when the gate is clean
         -- e.g. every self_employed-gated column's flag is just
         self_employed reproduced under a new name; verified via
         apply_correlation_filter showing r=+-1.0). In that case gate_col
         already carries the information -- no separate flag is needed.
      2. Fills the original column with its own mean (of valid, non-NaN
         values) -- a NEUTRAL value chosen specifically because the
         downstream model is K-means (distance-based): a fabricated
         out-of-range value (e.g. max+1) would distort Euclidean distance
         calculations by implying "more than Yes", whereas the mean places
         a "not applicable" respondent at the center of the existing
         distribution, adding no false directional signal.

    verbose=True prints, per gated_col, how many rows contradict the gate
    assumption (i.e. answered the gated question despite gate_col ==
    gate_value) -- real survey data is rarely perfectly clean skip-logic;
    a SMALL mismatch count is expected and not a sign the gate is wrong.
    A large mismatch count (e.g. close to the whole non-gated group size)
    usually means gate_value is backwards, not just noisy data -- see
    DECISIONS.md for a case where this caught an inverted gate_value.

    structural_config entries must specify their gate_value in whatever
    ENCODED form the column has at the pipeline stage this function is
    called at (e.g. ordinal-encoded int, not the original string) --
    this is meant to run on run_pipeline()'s output (df_processed),
    after ordinal/binary encoding.
    """
    df = df.copy()
    for cfg in structural_config:
        gate_col = cfg["gate_col"]
        gate_value = cfg["gate_value"]
        create_flag = cfg.get("create_flag", True)
        for gated_col in cfg["gated_columns"]:
            if gated_col not in df.columns:
                continue

            expected_na = df[gate_col] == gate_value
            actual_na = df[gated_col].isna()

            mismatch = expected_na & ~actual_na
            if verbose and mismatch.sum() > 0:
                print(f"{gated_col}: {mismatch.sum()} rows answered despite "
                      f"{gate_col}=={gate_value}")

            if create_flag:
                df[f"{gated_col}_not_applicable"] = actual_na.astype(int)

            fill_value = df[gated_col].dropna().mean()
            df[gated_col] = df[gated_col].fillna(fill_value)

    return df


def fill_remaining_with_mean(df: pd.DataFrame, exclude_cols: list = None) -> pd.DataFrame:
    """
    Plain mean-imputation for any column with remaining NaN after
    impute_structural_missingness has already run. Covers two kinds of
    leftover missingness:
      - Values already captured elsewhere as their own category (e.g.
        family_history_mental_illness's "I don't know" responses, already
        preserved via extract_special_na_flags/encode_special_flags) --
        the NaN remaining in the ORIGINAL column here is just a neutral
        placeholder, since the real signal already lives in the _special
        flag column.
      - Genuine residual non-response with no confirmed structural
        explanation (e.g. reveal_to_coworkers_direction, productivity_
        affected -- a compound "diagnosed or treated" gate was tested and
        only explained ~42-46% of the missingness, not enough to justify
        a _not_applicable flag; treated as plain residual instead -- see
        DECISIONS.md).

    exclude_cols: columns to skip entirely, e.g. ["age_group"] -- a
    profiling-only categorical column, never part of the model matrix,
    so it doesn't need (and can't take, being Categorical dtype) a
    numeric mean fill.
    """
    df = df.copy()
    exclude_cols = exclude_cols or []
    for col in df.columns:
        if col in exclude_cols:
            continue
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mean())
    return df


def prepare_for_feature_selection(df: pd.DataFrame, config) -> pd.DataFrame:
    """
    Runs every preprocessing step EXCEPT one-hot encoding (encode_nominal,
    encode_special_flags). Ordinal and binary encoding are safe to include
    here -- they convert values to numbers but keep the same column names.
    encode_nominal/encode_special_flags are excluded because they REPLACE
    a single column with several new ones, which would break any downstream
    step (like chi-square testing) that expects to find a column by its
    original name.

    Use this to get a DataFrame suitable for feature-selection diagnostics
    (apply_chi_square, apply_mutual_information from feature_selection.py)
    that reference column names directly, before those names disappear
    into one-hot columns. This is NOT the final model-ready feature
    matrix -- call run_pipeline for that. (apply_variance_threshold and
    apply_correlation_filter, by contrast, need run_pipeline's fully
    numeric output -- see feature_selection.py's module docstring.)
    """
    df = normalize_raw_column_names(df)
    df = rename_columns(df, config.COLUMN_RENAME_MAP)
    df = drop_columns(df, config.DROP_COLUMNS)

    # Must run BEFORE ordinal/binary encoding, so special values (e.g.
    # "I don't know", "Not applicable to me") are captured into their own
    # flag columns before the original column's non-mapped values become NaN.
    df = extract_special_na_flags(df, config.SPECIAL_NA_AS_CATEGORY)

    df = clean_age(df, **config.AGE_CLEANING)
    df = bucket_age(df, **config.AGE_BUCKETING)

    df = clean_gender(df, **config.GENDER_CLEANING)

    df = bucket_top_n_categories(df, **config.COUNTRY_BUCKETING)

    df = canonicalize_multiselect_values(df, config.MULTISELECT_CANONICALIZATION)
    df = split_multiselect(df, config.MULTISELECT_COLUMNS)
    df = extract_text_keyword_features(df, config.TEXT_COLUMNS)
    df = apply_direction_basis_columns(df, config.DIRECTION_BASIS_COLUMNS)

    df = encode_ordinal(df, config.ORDINAL_COLUMNS)
    df = encode_binary(df, config.BINARY_COLUMNS)
    return df


def run_pipeline(df: pd.DataFrame, config) -> pd.DataFrame:
    """
    Full pipeline, producing the final model-ready feature matrix:
    everything from prepare_for_feature_selection, plus one-hot encoding
    (nominal columns and special-NA flag columns).

    Feature selection diagnostics (chi-square, ANOVA, MI, variance
    thresholding) and imputation (impute_structural_missingness,
    fill_remaining_with_mean) are NOT run here -- call them separately in
    the notebook on the output of this function, so you can inspect
    results and make explicit decisions at each step rather than having
    them silently baked into one big pipeline call. Typical order after
    calling this:
        df_processed = run_pipeline(df, feature_config)
        # feature-selection diagnostics + decisions ...
        df_imputed = impute_structural_missingness(df_processed, STRUCTURAL_MISSINGNESS)
        df_imputed = fill_remaining_with_mean(df_imputed, exclude_cols=["age_group"])
        # then: drop age_group, scale, cluster
    """
    df = prepare_for_feature_selection(df, config)
    df = encode_nominal(df, config.NOMINAL_COLUMNS)
    df = encode_special_flags(df)
    return df