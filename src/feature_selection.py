import pandas as pd
import numpy as np
from sklearn.feature_selection import chi2, SelectKBest


# Chi-square test for feature selection
def apply_chi_square():
    # select ordinal features which make sense to compare against each other
    # maybe they say the same thing in different ways, so we can remove one of them

# candidates:
    
    # negative_consequences (3-way -> 3 pairs)
    # negative_consequences_discussion vs. negative_consequences_physical_health
    # negative_consequences_discussion vs. negative_consequences_open_about_mental_health
    # negative_consequences_physical_health vs. negative_consequences_open_about_mental_health

    # comfortable discussing (coworker vs. supervisor, current employer)
    # comfortable_discussing_with_coworkers vs. comfortable_discussing_with_supervisor

    # awareness (current vs. previous employer)
    # awareness_previous_employers vs. awareness_mental_health_care

    # benefits (current vs. previous employer)
    # mental_health_benefits vs. previous_employers_mental_health_benefits

    # reveal frequency (client vs. coworker) -- NOTE: columns renamed after direction/basis split
    # reveal_to_clients_direction vs. reveal_to_coworkers_direction

    # negative impact of revealing (client vs. coworker)
    # negative_impact_reveal vs. negative_impact_reveal_coworker

    # previous employer: coworker vs. supervisor comfort
    # previous_employers_comfortable_discussing_coworkers vs. previous_employers_comfortable_discussing_supervisor

    # current vs. previous employer: supervisor comfort
    # previous_employers_comfortable_discussing_supervisor vs. comfortable_discussing_with_supervisor

    # current vs. previous employer: coworker comfort
    # previous_employers_comfortable_discussing_coworkers vs. comfortable_discussing_with_coworkers

    # potential employer interview willingness (physical vs. mental health)
    # potential_employer_physical_health vs. potential_employer_mental_health

    # career impact vs. team view -- NOTE: columns renamed after direction/basis split
    # career_impact_mental_health_direction vs. team_view_mental_health_direction

    # openness vs. observed unsupportive response -- NOTE: renamed after direction/basis split
    # willingness_share_mental_illness vs. unsupportive_response_mental_health_direction

    # family history vs. own diagnosis (NOTE: different purpose than the rest -- this tests a
    # genuine expected clinical relationship, not a redundancy/overlap check; keep even if
    # significant, don't treat "related" as grounds to drop one)
    # family_history_mental_illness vs. past_mental_health_disorder
    # family_history_mental_illness vs. current_mental_health_disorder
    # past_mental_health_disorder vs. current_mental_health_disorder

    pass


