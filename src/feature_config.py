"""
Feature treatment configuration for the OSMI Mental Health in Tech survey.
"""

# ---------------------------------------------------------------------------
# 1) Rename map: original (long) survey question -> short snake_case name
# ---------------------------------------------------------------------------
COLUMN_RENAME_MAP = {
    'Are you self-employed?': 'self_employed',
    'How many employees does your company or organization have?': 'company_size',
    'Is your employer primarily a tech company/organization?': 'tech_company',
    'Is your primary role within your company related to tech/IT?': 'tech_role',
    'Does your employer provide mental health benefits as part of healthcare coverage?': 'mental_health_benefits',
    'Do you know the options for mental health care available under your employer-provided coverage?': 'awareness_mental_health_care',
    'Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?': 'formal_mental_health_discussion',
    'Does your employer offer resources to learn more about mental health concerns and options for seeking help?': 'mental_health_resources',
    'Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources provided by your employer?': 'anonymity_protected',
    'If a mental health issue prompted you to request a medical leave from work, asking for that leave would be:': 'medical_leave_request',
    'Do you think that discussing a mental health disorder with your employer would have negative consequences?': 'negative_consequences_discussion',
    'Do you think that discussing a physical health issue with your employer would have negative consequences?': 'negative_consequences_physical_health',
    'Would you feel comfortable discussing a mental health disorder with your coworkers?': 'comfortable_discussing_with_coworkers',
    'Would you feel comfortable discussing a mental health disorder with your direct supervisor(s)?': 'comfortable_discussing_with_supervisor',
    'Do you feel that your employer takes mental health as seriously as physical health?': 'employer_takes_mental_health_seriously',
    'Have you heard of or observed negative consequences for co-workers who have been open about mental health issues in your workplace?': 'negative_consequences_open_about_mental_health',
    'Do you have medical coverage (private insurance or state-provided) which includes treatment of mental health issues?': 'medical_coverage',
    'Do you know local or online resources to seek help for a mental health disorder?': 'awareness_resources',
    'If you have been diagnosed or treated for a mental health disorder, do you ever reveal this to clients or business contacts?': 'reveal_to_clients',
    'If you have revealed a mental health issue to a client or business contact, do you believe this has impacted you negatively?': 'negative_impact_reveal',
    'If you have been diagnosed or treated for a mental health disorder, do you ever reveal this to coworkers or employees?': 'reveal_to_coworkers',
    'If you have revealed a mental health issue to a coworker or employee, do you believe this has impacted you negatively?': 'negative_impact_reveal_coworker',
    'Do you believe your productivity is ever affected by a mental health issue?': 'productivity_affected',
    'If yes, what percentage of your work time (time performing primary or secondary job functions) is affected by a mental health issue?': 'percentage_affected',
    'Do you have previous employers?': 'previous_employers',
    'Have your previous employers provided mental health benefits?': 'previous_employers_mental_health_benefits',
    'Were you aware of the options for mental health care provided by your previous employers?': 'awareness_previous_employers',
    'Did your previous employers ever formally discuss mental health (as part of a wellness campaign or other official communication)?': 'previous_employers_mental_health_discussion',
    'Did your previous employers provide resources to learn more about mental health issues and how to seek help?': 'previous_employers_resources',
    'Was your anonymity protected if you chose to take advantage of mental health or substance abuse treatment resources with previous employers?': 'previous_employers_anonymity_protected',
    'Do you think that discussing a mental health disorder with previous employers would have negative consequences?': 'previous_employers_negative_consequences',
    'Do you think that discussing a physical health issue with previous employers would have negative consequences?': 'previous_employers_negative_consequences_physical',
    'Would you have been willing to discuss a mental health issue with your previous co-workers?': 'previous_employers_comfortable_discussing_coworkers',
    'Would you have been willing to discuss a mental health issue with your direct supervisor(s)?': 'previous_employers_comfortable_discussing_supervisor',
    'Did you feel that your previous employers took mental health as seriously as physical health?': 'previous_employers_mental_health_seriously',
    'Did you hear of or observe negative consequences for co-workers with mental health issues in your previous workplaces?': 'previous_employers_negative_consequences_coworkers',
    'Would you be willing to bring up a physical health issue with a potential employer in an interview?': 'potential_employer_physical_health',
    'Why or why not?': 'reason_not_willing_physical_health',
    'Would you bring up a mental health issue with a potential employer in an interview?': 'potential_employer_mental_health',
    'Why or why not?.1': 'reason_not_willing_mental_health',
    'Do you feel that being identified as a person with a mental health issue would hurt your career?': 'career_impact_mental_health',
    'Do you think that team members/co-workers would view you more negatively if they knew you suffered from a mental health issue?': 'team_view_mental_health',
    'How willing would you be to share with friends and family that you have a mental illness?': 'willingness_share_mental_illness',
    'Have you observed or experienced an unsupportive or badly handled response to a mental health issue in your current or previous workplace?': 'unsupportive_response_mental_health',
    'Have your observations of how another individual who discussed a mental health disorder made you less likely to reveal a mental health issue yourself in your current workplace?': 'less_likely_reveal_mental_health',
    'Do you have a family history of mental illness?': 'family_history_mental_illness',
    'Have you had a mental health disorder in the past?': 'past_mental_health_disorder',
    'Do you currently have a mental health disorder?': 'current_mental_health_disorder',
    'If yes, what condition(s) have you been diagnosed with?': 'diagnosed_conditions',
    'If maybe, what condition(s) do you believe you have?': 'believed_conditions',
    'Have you been diagnosed with a mental health condition by a medical professional?': 'diagnosed_by_professional',
    'If so, what condition(s) were you diagnosed with?': 'diagnosed_conditions_professional',
    'Have you ever sought treatment for a mental health issue from a mental health professional?': 'sought_treatment',
    'If you have a mental health issue, do you feel that it interferes with your work when being treated effectively?': 'interferes_with_work_treated',
    'If you have a mental health issue, do you feel that it interferes with your work when NOT being treated effectively?': 'interferes_with_work_not_treated',
    'What is your age?': 'age',
    'What is your gender?': 'gender',
    'What country do you live in?': 'country_live',
    'What US state or territory do you live in?': 'us_state_live',
    'What country do you work in?': 'country_work',
    'What US state or territory do you work in?': 'us_state_work',
    'Which of the following best describes your work position?': 'work_position',
    'Do you work remotely?': 'works_remotely',
}

# ---------------------------------------------------------------------------
# 2) Columns to drop entirely
# ---------------------------------------------------------------------------
DROP_COLUMNS = [
    'us_state_live',  # too many categories for one-hot, not central to the analysis
    'us_state_work',  # too many categories for one-hot, not central to the analysis
]

# ---------------------------------------------------------------------------
# 2b) Age cleaning + bucketing. Bounds chosen from inspecting the actual
#     min/max of the distribution -- min=3 and max=323 in the raw data
#     are clear data-entry errors / placeholder values (e.g. 99).
# ---------------------------------------------------------------------------
AGE_CLEANING = {
    "col": "age",
    "min_age": 18,
    "max_age": 75,
}

AGE_BUCKETING = {
    "col": "age",
    "new_col": "age_group",
}

# ---------------------------------------------------------------------------
# 2c) Gender cleaning. Keys must be lowercase/stripped. STILL EMPTY --
#     needs the full value_counts() to build synonym_map properly.
# ---------------------------------------------------------------------------
GENDER_CLEANING = {
    "col": "gender",
    "new_col": "gender_cleaned",
    "other_label": "Other/Non-binary",
    "synonym_map": {
        # TODO: fill in once full value_counts() reviewed
    },
}

# ---------------------------------------------------------------------------
# 3) Ordinal columns: category order matters. Map column -> list of
#    categories in order (lowest to highest). "I don't know"/"Maybe"/etc.
#    are intentionally left OUT of these lists and handled as their own
#    category (see SPECIAL_NA_AS_CATEGORY + note on that mechanism below).
# ---------------------------------------------------------------------------
ORDINAL_COLUMNS = {
    'awareness_resources': ["No, I don't know any", 'I know some', 'Yes, I know several'],
    'medical_leave_request': ['Very easy', 'Somewhat easy', 'Neither easy nor difficult', 'Somewhat difficult', 'Very difficult'],
    'reveal_to_coworkers': ["No, because it doesn't matter", 'No, because it would impact me negatively', 'Sometimes, if it comes up', 'Yes, always'],
    'awareness_previous_employers': ["No, I only became aware later", "I was aware of some", "Yes, I was aware of all of them"],
    'previous_employers_mental_health_discussion': ['None did', 'Some did', 'Yes, they all did'],
    'previous_employers_resources': ['None did', 'Some did', 'Yes, they all did'],
    'previous_employers_anonymity_protected': ['No', 'Sometimes', 'Yes, always'],
    'previous_employers_negative_consequences': ['None of them', 'Some of them', 'Yes, all of them'],
    'previous_employers_negative_consequences_physical': ['None of them', 'Some of them', 'Yes, all of them'],
    'previous_employers_comfortable_discussing_coworkers': ['No, at none of my previous employers', 'Some of my previous employers', 'Yes, at all of my previous employers'],
    'previous_employers_comfortable_discussing_supervisor': ['No, at none of my previous employers', 'Some of my previous employers', 'Yes, at all of my previous employers'],
    'previous_employers_mental_health_seriously': ['None did', 'Some did', 'Yes, they all did'],
    'previous_employers_negative_consequences_coworkers': ['None of them', 'Some of them', 'Yes, all of them'],
    'willingness_share_mental_illness': ['Not open at all', 'Somewhat not open', 'Neutral', 'Somewhat open', 'Very open'],
    'interferes_with_work_treated': ['Never', 'Rarely', 'Sometimes', 'Often'],
    'works_remotely': ['Never', 'Sometimes', 'Always'],
    'percentage_affected': ['1-25%', '26-50%', '51-75%', '76-100%'],  # FIXED: matches actual data categories (no 0-10%/11-25% split exists)

    # --- NOT YET ADDED, see error list ---
    # 'previous_employers_mental_health_benefits': ['No, none did', 'Some did', 'Yes, they all did'],
}

# ---------------------------------------------------------------------------
# 4) Nominal columns: no natural order -> one-hot encode
# ---------------------------------------------------------------------------
NOMINAL_COLUMNS = [
    "company_size",
]

# ---------------------------------------------------------------------------
# 5) Simple binary columns (already 0/1, or a clean two-value Yes/No).
#    !! SEE ERROR LIST -- many columns below actually have 3+ categories
#    in the real data and should NOT be here. Left as-is from your version
#    so you can compare against the fixes discussed. !!
# ---------------------------------------------------------------------------
BINARY_COLUMNS = {
    "self_employed": None,  # already 0/1
    "tech_company": None,  # already 0/1
    "tech_role": None,  # already 0/1
    "formal_mental_health_discussion": {"Yes": 1, "No": 0},
    "awareness_mental_health_care": {"Yes": 1, "No": 0},
    "mental_health_benefits": {"Yes": 1, "No": 0},
    "mental_health_resources": {"Yes": 1, "No": 0},
    "anonymity_protected": {"Yes": 1, "No": 0},
    "negative_consequences_discussion": {"Yes": 1, "No": 0},
    "negative_consequences_physical_health": {"Yes": 1, "No": 0},
    "comfortable_discussing_with_coworkers": {"Yes": 1, "No": 0},
    "comfortable_discussing_with_supervisor": {"Yes": 1, "No": 0},
    "employer_takes_mental_health_seriously": {"Yes": 1, "No": 0},
    "medical_coverage": None,  # already 0/1
    "negative_consequences_open_about_mental_health": {"Yes": 1, "No": 0},  # OK -- truly 2 values
    "potential_employer_physical_health": {"Yes": 1, "No": 0},
    "potential_employer_mental_health": {"Yes": 1, "No": 0},
    "less_likely_reveal_mental_health": {"Yes": 1, "No": 0},
    "family_history_mental_illness": {"Yes": 1, "No": 0},
    "past_mental_health_disorder": {"Yes": 1, "No": 0},
    "current_mental_health_disorder": {"Yes": 1, "No": 0},
    "diagnosed_by_professional": {"Yes": 1, "No": 0},  # OK -- truly 2 values
    "sought_treatment": None,  # already 0/1

    # --- NOT YET ADDED, see error list ---
    # "previous_employers": None,  # already 0/1
}

# ---------------------------------------------------------------------------
# 6) Multi-select columns: pipe-separated values -> one binary flag per
#    distinct value. Currently empty -- see error list re: diagnosed/
#    believed conditions columns (recommend moving them here instead of
#    TEXT_COLUMNS to preserve full category granularity).
# ---------------------------------------------------------------------------
MULTISELECT_COLUMNS = [
    # "diagnosed_conditions",
    # "believed_conditions",
    # "diagnosed_conditions_professional",
]

# ---------------------------------------------------------------------------
# Direction/basis splits for columns with an orthogonal belief-vs-experience
# (or observed-vs-experienced) dimension that a single ordinal scale would
# misrepresent.
# ---------------------------------------------------------------------------
DIRECTION_BASIS_COLUMNS = {
    "career_impact_mental_health": {
        "direction_map": {
            "No, it has not": "No", "No, I don't think it would": "No",
            "Maybe": "Maybe",
            "Yes, I think it would": "Yes", "Yes, it has": "Yes",
        },
        "basis_map": {
            "No, it has not": "experienced", "Yes, it has": "experienced",
            "No, I don't think it would": "belief", "Yes, I think it would": "belief",
            "Maybe": None,
        },
    },
    "team_view_mental_health": {
        "direction_map": {
            "No, they do not": "No", "No, I don't think they would": "No",
            "Maybe": "Maybe",
            "Yes, I think they would": "Yes", "Yes, they do": "Yes",
        },
        "basis_map": {
            "No, they do not": "experienced", "Yes, they do": "experienced",
            "No, I don't think they would": "belief", "Yes, I think they would": "belief",
            "Maybe": None,
        },
    },
    "unsupportive_response_mental_health": {
        "direction_map": {
            "No": "No",
            "Maybe/Not sure": "Maybe",
            "Yes, I observed": "Yes",
            "Yes, I experienced": "Yes",
        },
        "basis_map": {
            "No": None,
            "Maybe/Not sure": None,
            "Yes, I observed": "observed",
            "Yes, I experienced": "experienced",
        },
    },
}

# ---------------------------------------------------------------------------
# 7) Free-text columns needing NLP-ish treatment (Unit 4.3 territory).
# ---------------------------------------------------------------------------
TEXT_COLUMNS = {
    "reason_not_willing_physical_health": {
        "keywords": {
            "fear": ["afraid", "fear"],
        }
    },
    "reason_not_willing_mental_health": {
        "keywords": {
            "stigma": ["stigma"],  # FIXED: was "Stigma" (capitalized) -- never matched lowercased text
        }
    },

    # --- RECOMMEND MOVING THESE THREE TO MULTISELECT_COLUMNS INSTEAD ---
    # "diagnosed_conditions": {...},
    # "believed_conditions": {...},
    # "diagnosed_conditions_professional": {...},
}

# ---------------------------------------------------------------------------
# 8) Values that look like missingness but are actually a meaningful,
#    actively-selected answer -- keep these as their OWN category rather
#    than collapsing into NaN or into another category.
#    !! NOTE: mark_special_na_as_category() is currently a no-op in
#    preprocessing.py -- listing values here does not yet protect them
#    from becoming NaN in encode_ordinal/encode_binary. See error list. !!
# ---------------------------------------------------------------------------
SPECIAL_NA_AS_CATEGORY = {
    "*": [
        "I don't know",
        "I am not sure",
        "Not sure",
        "Maybe",
        "N/A (not currently aware)",
        "Not eligible for coverage / N/A",
        "Not applicable to me",
        "Not applicable to me (I do not have a mental illness)",
    ],
}