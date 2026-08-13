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
    'country_work',   # ~98% identical to country_live -- redundant, dropped to avoid double-weighting
]

# ---------------------------------------------------------------------------
# 2b) Age cleaning + bucketing.
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
# 2c) Gender cleaning.
# ---------------------------------------------------------------------------
GENDER_CLEANING = {
    "col": "gender",
    "new_col": "gender_cleaned",
    "other_label": "Other/Non-binary",
    "synonym_map": {
        "male": "Male", "m": "Male", "cis man": "Male", "male (cis)": "Male", "man": "Male",
        "cis male": "Male", "sex is male": "Male", "cis dude": "Male", "cisdude": "Male",
        "cis-male": "Male", "cis man ": "Male", "malr": "Male",
        "mail": "Male",
        "dude": "Male",

        "female": "Female", "f": "Female", "woman": "Female", "i identify as female.": "Female",
        "female assigned at birth": "Female", "fm": "Female", "cis female": "Female", "female/woman": "Female",
        "cisgender female": "Female", "cis-woman": "Female", "fem": "Female",
        "female (props for making this a freeform field, though)": "Female",

        "non-binary": "Other/Non-binary", "agender": "Other/Non-binary", "nonbinary": "Other/Non-binary",
        "genderqueer": "Other/Non-binary", "genderfluid": "Other/Non-binary", "bigender": "Other/Non-binary",
        "androgynous": "Other/Non-binary", "enby": "Other/Non-binary", "transitioned, m2f": "Other/Non-binary",
        "genderfluid (born female)": "Other/Non-binary", "other/transfeminine": "Other/Non-binary",
        "female or multi-gender femme": "Other/Non-binary",
        "other": "Other/Non-binary",
        "nb masculine": "Other/Non-binary",
        "genderqueer woman": "Other/Non-binary",
        "mtf": "Other/Non-binary",
        "queer": "Other/Non-binary",
        "fluid": "Other/Non-binary",
        "male/genderqueer": "Other/Non-binary",
        "male (trans, ftm)": "Other/Non-binary",
        "genderflux demi-girl": "Other/Non-binary",
        "female-bodied; no feelings about gender": "Other/Non-binary",
        "afab": "Other/Non-binary",
        "transgender woman": "Other/Non-binary",
    },
}

COUNTRY_BUCKETING = {
    "col": "country_live",
    "top_categories": [
        "United States of America", "United Kingdom", "Canada", "Germany",
        "Netherlands", "Australia",
    ],
    "other_label": "Other",
}

"""
Template for canonicalizing diagnosed_conditions / believed_conditions /
diagnosed_conditions_professional before multi-select splitting.

Fill in the "" on the right of each raw value with your chosen canonical
category label (e.g. "Autism Spectrum", "ADHD", "Anxiety Disorder").
Leave it as "" for any value you want routed to the residual "Other"
bucket instead (e.g. one-off free-text write-ins, sarcastic asides).

Use the SAME canonical label spelling across all three dicts for values
that represent the same underlying condition, so they end up in the
same final flag column regardless of which source column they came from.
"""

DIAGNOSED_CONDITIONS_MAP = {
    "add (w/o hyperactivity)": "Attention Deficit Hyperactivity Disorder",
    "addictive disorder": "Addictive Disorder",
    "anxiety disorder (generalized, social, phobia, etc)": "Anxiety Disorder",
    "asperges": "Autism",
    "attention deficit hyperactivity disorder": "Attention Deficit Hyperactivity Disorder",
    "autism": "Autism",
    "autism (asperger's)": "Autism",
    "autism spectrum disorder": "Autism",
    "burn out": "Burn out",
    'combination of physical impairment (strongly near-sighted) with a possibly mental one (mcd / "adhd", though its actually a stimulus filtering impairment)': "Attention Deficit Hyperactivity Disorder",
    "depression": "Mood Disorder",
    "dissociative disorder": "Dissociative Disorder",
    "eating disorder (anorexia, bulimia, etc)": "Eating Disorder",
    "gender dysphoria": "Gender Dysphoria",
    "i haven't been formally diagnosed, so i felt uncomfortable answering, but social anxiety and depression.": "Mood Disorder",
    "intimate disorder": "Anxiety Disorder",
    "mood disorder (depression, bipolar disorder, etc)": "Mood Disorder",
    "obsessive-compulsive disorder": "Obsessive-Compulsive Disorder",
    "pdd-nos": "Autism",
    "ptsd (undiagnosed)": "Post-traumatic Stress Disorder",  # even undiagnosed, the person suffers from a condition, might be depression
    "personality disorder (borderline, antisocial, paranoid, etc)": "Personality Disorder",
    "pervasive developmental disorder (not otherwise specified)": "Autism",
    "post-traumatic stress disorder": "Post-traumatic Stress Disorder",
    "psychotic disorder (schizophrenia, schizoaffective, etc)": "Psychotic Disorder",
    "schizotypal personality disorder": "Personality Disorder",
    "seasonal affective disorder": "Mood Disorder",
    "sexual addiction": "Addictive Disorder",
    "sleeping disorder": "Sleeping Disorder",
    "stress response syndromes": "Adjustment Disorder",
    "substance use disorder": "Addictive Disorder",
    "transgender": "Gender Dysphoria",
    "traumatic brain injury": "",
}

BELIEVED_CONDITIONS_MAP = {
    "addictive disorder": "Addictive Disorder",
    "anxiety disorder (generalized, social, phobia, etc)": "Anxiety Disorder",
    "asperger syndrome": "Autism",
    "asperger's": "Autism",
    "attention deficit hyperactivity disorder": "Attention Deficit Hyperactivity Disorder",
    "autism": "Autism",
    "burnout": "Burn out",
    "depersonalisation": "Depersonalization Disorder",
    "dissociative disorder": "Dissociative Disorder",
    "eating disorder (anorexia, bulimia, etc)": "Eating Disorder",
    "gender identity disorder": "Gender Dysphoria",
    "mood disorder (depression, bipolar disorder, etc)": "Mood Disorder",
    "obsessive-compulsive disorder": "Obsessive-Compulsive Disorder",
    "personality disorder (borderline, antisocial, paranoid, etc)": "Personality Disorder",
    "post-traumatic stress disorder": "Post-traumatic Stress Disorder",
    "psychotic disorder (schizophrenia, schizoaffective, etc)": "Psychotic Disorder",
    "stress response syndromes": "Adjustment Disorder",
    "substance use disorder": "Addictive Disorder",
    "suicidal ideation": "Mood Disorder",
    "tinnitus": "",
    "we're all hurt, right?!": "",
    "depersonalization disorder": "Depersonalization Disorder",
    "post-partum / anxiety": "Anxiety Disorder",
}

DIAGNOSED_CONDITIONS_PROFESSIONAL_MAP = {
    "add (w/o hyperactivity)": "Attention Deficit Hyperactivity Disorder",
    "addictive disorder": "Addictive Disorder",
    "anxiety disorder (generalized, social, phobia, etc)": "Anxiety Disorder",
    "asperger syndrome": "Autism",
    "aspergers": "Autism",
    "attention deficit disorder": "Attention Deficit Hyperactivity Disorder",
    "attention deficit hyperactivity disorder": "Attention Deficit Hyperactivity Disorder",
    "autism": "Autism",
    "autism (asperger's)": "Autism",
    'autism - while not a "mental illness", still greatly affects how i handle anxiety': "Autism",
    "autism spectrum disorder": "Autism",
    "burn out": "Burn out",
    "depression": "Mood Disorder",
    "dissociative disorder": "Dissociative Disorder",
    "eating disorder (anorexia, bulimia, etc)": "Eating Disorder",
    "gender dysphoria": "Gender Dysphoria",
    "gender identity disorder": "Gender Dysphoria",
    "intimate disorder": "Anxiety Disorder",
    'mcd (when it was diagnosed, the ultra-mega "disorder" adhd didn\'t exist yet)': "Attention Deficit Hyperactivity Disorder",
    "mood disorder (depression, bipolar disorder, etc)": "Mood Disorder",
    "obsessive-compulsive disorder": "Obsessive-Compulsive Disorder",
    "pdd-nos": "Autism",
    "pdd-nos (see above)": "Autism",
    "personality disorder (borderline, antisocial, paranoid, etc)": "Personality Disorder",
    "post-traumatic stress disorder": "Post-traumatic Stress Disorder",
    "psychotic disorder (schizophrenia, schizoaffective, etc)": "Psychotic Disorder",
    "schizotypal personality disorder": "Personality Disorder",
    "seasonal affective disorder": "Mood Disorder",
    "stress response syndromes": "Adjustment Disorder",
    "substance use disorder": "Addictive Disorder",
    "suicidal ideation": "Mood Disorder",
    "attention deficit disorder (but not the hyperactive version)": "Attention Deficit Hyperactivity Disorder",
    "autism spectrum disorder ": "Autism",  
    "posttraumatic stress disourder": "Post-traumatic Stress Disorder", 
}

MULTISELECT_CANONICALIZATION = {
    "diagnosed_conditions": DIAGNOSED_CONDITIONS_MAP,
    "believed_conditions": BELIEVED_CONDITIONS_MAP,
    "diagnosed_conditions_professional": DIAGNOSED_CONDITIONS_PROFESSIONAL_MAP,
    # work_position intentionally excluded -- it was already clean, no
    # canonicalization needed; split_multiselect handles it directly.
}

# ---------------------------------------------------------------------------
# 3) Ordinal columns: category order matters. Map column -> list of
#    categories in order (lowest to highest), where LOWEST = FAVORABLE
#    (less stigma / more support / more openness), for consistency when
#    interpreting cluster centroids later.
#
#    Exceptions to the favorable=low convention, left in their natural
#    order instead (see DECISIONS.md):
#    - works_remotely: frequency-of-remote-work, not an attitude/outcome
#      measure -- no inherent "favorable" direction to align to.
#    - past_mental_health_disorder / current_mental_health_disorder:
#      self-reported health status (absent/uncertain/confirmed), not a
#      stigma/comfort measure -- No/Maybe/Yes reflects degree of
#      presence/certainty, not favorability.
# ---------------------------------------------------------------------------
ORDINAL_COLUMNS = {
    'awareness_resources': ['Yes, I know several', 'I know some', "No, I don't know any"],
    'medical_leave_request': ['Very easy', 'Somewhat easy', 'Neither easy nor difficult', 'Somewhat difficult', 'Very difficult'],
    'awareness_previous_employers': ["Yes, I was aware of all of them", "I was aware of some", "No, I only became aware later"],
    'previous_employers_mental_health_discussion': ['Yes, they all did', 'Some did', 'None did'],
    'previous_employers_resources': ['Yes, they all did', 'Some did', 'None did'],
    'previous_employers_anonymity_protected': ['Yes, always', 'Sometimes', 'No'],
    'previous_employers_negative_consequences': ['None of them', 'Some of them', 'Yes, all of them'],
    'previous_employers_negative_consequences_physical': ['None of them', 'Some of them', 'Yes, all of them'],
    'previous_employers_comfortable_discussing_coworkers': ['Yes, at all of my previous employers', 'Some of my previous employers', 'No, at none of my previous employers'],
    'previous_employers_comfortable_discussing_supervisor': ['Yes, at all of my previous employers', 'Some of my previous employers', 'No, at none of my previous employers'],
    'previous_employers_mental_health_seriously': ['Yes, they all did', 'Some did', 'None did'],  
    'previous_employers_negative_consequences_coworkers': ['None of them', 'Some of them', 'Yes, all of them'],
    'willingness_share_mental_illness': ['Very open', 'Somewhat open', 'Neutral', 'Somewhat not open', 'Not open at all'],
    'interferes_with_work_treated': ['Never', 'Rarely', 'Sometimes', 'Often'],
    'interferes_with_work_not_treated': ['Never', 'Rarely', 'Sometimes', 'Often'],
    'works_remotely': ['Never', 'Sometimes', 'Always'],  
    'percentage_affected': ['1-25%', '26-50%', '51-75%', '76-100%'],
    'negative_consequences_discussion': ['No', 'Maybe', 'Yes'],
    'negative_consequences_physical_health': ['No', 'Maybe', 'Yes'],
    'comfortable_discussing_with_coworkers': ['Yes', 'Maybe', 'No'],
    'comfortable_discussing_with_supervisor': ['Yes', 'Maybe', 'No'],
    'potential_employer_physical_health': ['Yes', 'Maybe', 'No'],
    'potential_employer_mental_health': ['Yes', 'Maybe', 'No'],
    'less_likely_reveal_mental_health': ['No', 'Maybe', 'Yes'],
    'past_mental_health_disorder': ['No', 'Maybe', 'Yes'], 
    'current_mental_health_disorder': ['No', 'Maybe', 'Yes'], 
    'previous_employers_mental_health_benefits': ['Yes, they all did', 'Some did', 'No, none did'],
    'awareness_mental_health_care': ['Yes', 'I am not sure', 'No'],
    'negative_impact_reveal': ['No', "I'm not sure", 'Yes'],
    'negative_impact_reveal_coworker': ['No', "I'm not sure", 'Yes'],
    'productivity_affected': ['No', 'Unsure', 'Yes'],
    'career_impact_mental_health_direction': ['No', 'Maybe', 'Yes'],
    'team_view_mental_health_direction': ['No', 'Maybe', 'Yes'],
    'unsupportive_response_mental_health_direction': ['No', 'Maybe', 'Yes'],

    # Produced by DIRECTION_BASIS_COLUMNS split -- frequency dimension, ordinal
    'reveal_to_coworkers_direction': ['Always', 'Sometimes', 'Never'], 
    'reveal_to_clients_direction': ['Always', 'Sometimes', 'Never'],
}

# ---------------------------------------------------------------------------
# 4) Nominal columns: no natural order -> one-hot encode
# ---------------------------------------------------------------------------
NOMINAL_COLUMNS = [
    "company_size",
    "mental_health_benefits",
    "gender_cleaned",
    "country_live", 
    "reveal_to_coworkers_basis",
    "reveal_to_clients_basis",
    "career_impact_mental_health_basis",
    "team_view_mental_health_basis",
    "unsupportive_response_mental_health_basis",
]

# ---------------------------------------------------------------------------
# 5) Simple binary columns.
# ---------------------------------------------------------------------------
BINARY_COLUMNS = {
    "self_employed": None,
    "tech_company": None,
    "tech_role": None,
    "formal_mental_health_discussion": {"Yes": 1, "No": 0},
    "mental_health_resources": {"Yes": 1, "No": 0},
    "anonymity_protected": {"Yes": 1, "No": 0},
    "employer_takes_mental_health_seriously": {"Yes": 1, "No": 0},
    "medical_coverage": None,
    "negative_consequences_open_about_mental_health": {"Yes": 1, "No": 0},
    "family_history_mental_illness": {"Yes": 1, "No": 0},
    "diagnosed_by_professional": {"Yes": 1, "No": 0},
    "sought_treatment": None,
    "previous_employers": None,
}

# ---------------------------------------------------------------------------
# 6) Multi-select columns.
# ---------------------------------------------------------------------------
MULTISELECT_COLUMNS = [
    "diagnosed_conditions",
    "believed_conditions",
    "diagnosed_conditions_professional",
    "work_position",
]

# ---------------------------------------------------------------------------
# Direction/basis splits.
# ---------------------------------------------------------------------------
DIRECTION_BASIS_COLUMNS = {
    "reveal_to_coworkers": {
        "direction_map": {
            "No, because it doesn't matter": "Never",
            "No, because it would impact me negatively": "Never",
            "Sometimes, if it comes up": "Sometimes",
            "Yes, always": "Always",
        },
        "basis_map": {
            "No, because it doesn't matter": "indifferent",
            "No, because it would impact me negatively": "fear",
            "Sometimes, if it comes up": None,
            "Yes, always": None,
        },
    },
    "reveal_to_clients": {
        "direction_map": {
            "No, because it doesn't matter": "Never",
            "No, because it would impact me negatively": "Never",
            "Sometimes, if it comes up": "Sometimes",
            "Yes, always": "Always",
        },
        "basis_map": {
            "No, because it doesn't matter": "indifferent",
            "No, because it would impact me negatively": "fear",
            "Sometimes, if it comes up": None,
            "Yes, always": None,
        },
    },
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
# 7) Free-text columns.
# ---------------------------------------------------------------------------
TEXT_COLUMNS = {
    "reason_not_willing_physical_health": {
        "keywords": {
            "job_relevance_impact": ["relevan", "irrelevan", "relavent", "depend", "affect", "impact", "bearing on", "matter", "get in the way"],
            "fear_hiring_risk": ["afraid", "fear", "scared", "nervous", "risk", "chances", "wouldn't hire", "not hire", "hurt my", "kill my", "lower my", "less likely to get", "reject", "get the job", "get a job"],
            "discrimination_stigma": ["discriminat", "stigma", "prejudice", "bias", "judg", "negativ", "less attractive", "disadvantage", "taboo"],
            "privacy_personal": ["private", "personal", "none of", "business", "confidential"],
            "honesty_trust": ["honest", "upfront", "trust", "fair", "transparent", "hide", "disclos", "open"],
            "accommodation_disability": ["accommodat", "disabilit", "equipment", "assistive", "protected"],
            "timing_later": ["later", "after i", "after being hired", "offer stage", "wait", "once hired", "down the road"],
            "not_applicable": ["don't have", "doesn't have any", "never come up", "not applicable", "n/a", "no reason", "nothing to", "never had"],
            "productivity_performance": ["productiv", "perform"],
            "embarrassment_shame": ["embarrass", "ashamed", "shame"],
        }
    },
    "reason_not_willing_mental_health": {
        "keywords": {
            "job_relevance_impact": ["relevan", "irrelevan", "relavent", "depend", "affect", "impact", "bearing on", "matter", "get in the way"],
            "fear_hiring_risk": ["afraid", "fear", "scared", "nervous", "risk", "chances", "wouldn't hire", "not hire", "hurt my", "kill my", "lower my", "less likely to get", "reject", "get the job", "get a job", "worried"],
            "discrimination_stigma": ["discriminat", "stigma", "prejudice", "bias", "judg", "negativ", "less attractive", "disadvantage", "taboo", "weakness", "weak", "frowned upon", "unstable", "instability"],
            "privacy_personal": ["private", "personal", "none of", "business", "confidential"],
            "honesty_trust": ["honest", "upfront", "trust", "fair", "transparent", "hide", "disclos", "open"],
            "accommodation_disability": ["accommodat", "disabilit", "equipment", "assistive", "protected"],
            "timing_later": ["later", "after i", "after being hired", "offer stage", "wait", "once hired", "down the road"],
            "not_applicable": ["don't have", "doesn't have any", "never come up", "not applicable", "n/a", "no reason", "nothing to", "never had"],
            "productivity_performance": ["productiv", "perform"],
            "embarrassment_shame": ["embarrass", "ashamed", "shame"],
            "understanding_support": ["understand", "support", "empath", "compassion"],
        }
    },
}

# ---------------------------------------------------------------------------
# 8) Structural non-applicability values.
# ---------------------------------------------------------------------------
SPECIAL_NA_AS_CATEGORY = {
    "*": [
        "N/A (not currently aware)",
        "Not applicable to me",
        "Not applicable to me (I do not have a mental illness)",
    ],
    "medical_leave_request": ["I don't know"],
    "formal_mental_health_discussion": ["I don't know"],
    "anonymity_protected": ["I don't know"],
    "employer_takes_mental_health_seriously": ["I don't know"],
    "family_history_mental_illness": ["I don't know"],
    "mental_health_resources": ["I don't know"],
    "previous_employers_anonymity_protected": ["I don't know"],
    "previous_employers_mental_health_seriously": ["I don't know"],
    "previous_employers_mental_health_benefits": ["I don't know"],
    "previous_employers_negative_consequences": ["I don't know"],
    "previous_employers_comfortable_discussing_supervisor": ["I don't know"],
    "previous_employers_mental_health_discussion": ["I don't know"],
}

# ---------------------------------------------------------------------------
# 9) Pre-defined column groups for filter feature selection
# ---------------------------------------------------------------------------
FEATURE_FILTER_GROUPS = [
    # negative_consequences 
    ("negative_consequences_discussion", "negative_consequences_physical_health"),
    ("negative_consequences_discussion", "negative_consequences_open_about_mental_health"),
    ("negative_consequences_physical_health", "negative_consequences_open_about_mental_health"),

    # comfortable discussing (coworker vs. supervisor, current employer)
    ("comfortable_discussing_with_coworkers", "comfortable_discussing_with_supervisor"),

    # awareness (current vs. previous employer)
    ("awareness_previous_employers", "awareness_mental_health_care"),

    # benefits (current vs. previous employer)
    ("mental_health_benefits", "previous_employers_mental_health_benefits"),

    # reveal frequency (client vs. coworker) -- NOTE: columns renamed after direction/basis split
    ("reveal_to_clients_direction", "reveal_to_coworkers_direction"),

    # negative impact of revealing (client vs. coworker)
    ("negative_impact_reveal", "negative_impact_reveal_coworker"),

    # previous employer: coworker vs. supervisor comfort
    ("previous_employers_comfortable_discussing_coworkers", "previous_employers_comfortable_discussing_supervisor"),

    # current vs. previous employer: supervisor comfort
    ("previous_employers_comfortable_discussing_supervisor", "comfortable_discussing_with_supervisor"),

    # current vs. previous employer: coworker comfort
    ("previous_employers_comfortable_discussing_coworkers", "comfortable_discussing_with_coworkers"),

    # potential employer interview willingness (physical vs. mental health)
    ("potential_employer_physical_health", "potential_employer_mental_health"),

    # career impact vs. team view -- NOTE: columns renamed after direction/basis split
    ("career_impact_mental_health_direction", "team_view_mental_health_direction"),

    # openness vs. observed unsupportive response -- NOTE: renamed after direction/basis split
    ("willingness_share_mental_illness", "unsupportive_response_mental_health_direction"),

    # family history vs. own diagnosis (NOTE: different purpose than the rest -- this tests a
    # genuine expected clinical relationship, not a redundancy/overlap check; keep even if
    # significant, don't treat "related" as grounds to drop one)
    ("family_history_mental_illness", "past_mental_health_disorder"),
    ("family_history_mental_illness", "current_mental_health_disorder"),
    ("past_mental_health_disorder", "current_mental_health_disorder")
]