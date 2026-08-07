## All decisions which were made during data cleansing

- Gender was separated into three buckets Male / Female / Other — non-serious/ambiguous answers 
  (e.g. "Human", "Unicorn", joke responses) also fall into Other by default, since they can't be 
  meaningfully distinguished from genuine non-binary/genderqueer responses at n=1 each

- Age column was set to min 18 and max 75; values outside this range (e.g. 3, 15, 17, and clear 
  placeholder/junk entries like 99 and 323) don't make sense for a workplace survey and were set 
  to missing rather than dropping the row

- For Yes/No columns with a third answer option, the treatment depends on what the third option 
  actually represents, not just its wording:
  - If the question asks about the respondent's own DEGREE/LEVEL of something (e.g. "do you KNOW 
    the options"), an uncertain answer ("I am not sure") is a genuine midpoint and was encoded as 
    ORDINAL (No < I am not sure/Maybe < Yes)
  - If the question asks about an EXTERNAL FACT (e.g. "IS your anonymity protected", "HAS your 
    employer discussed...", "do you HAVE a family history"), "I don't know" reflects an information 
    gap rather than a middle value, and was instead split into a binary Yes/No column PLUS a 
    separate "uncertain" flag column, so the uncertainty isn't forced onto a spectrum it doesn't 
    belong on
  - Columns with 4 genuinely distinct categories that don't form a single clean order (e.g. 
    "mental_health_benefits": Yes / No / I don't know / Not eligible for coverage) were treated as 
    NOMINAL (one-hot) instead of forced into ordinal or binary

- "Not eligible for coverage / N/A" was kept as its own explicit category, separate from true NaN — 
  it's an actively selected answer (no healthcare coverage at all) rather than a skipped/inapplicable 
  question, and merging the two would blur genuinely different respondent situations

- Direction/basis splits were used for columns with an orthogonal belief-vs-experience (or 
  observed-vs-experienced) dimension, because forcing e.g. "Yes, it has" (lived experience) and 
  "Yes, I think it would" (anticipated belief) onto one ordinal scale would impose an ordering 
  between them that isn't actually justified — they're two different kinds of signal, not two 
  points on the same line

- "percentage_affected" and "works_remotely" were encoded as ordinal rather than one-hot/binary, 
  since their categories have a clear natural order (e.g. Never < Sometimes < Always)

- US state/territory columns (live and work) were dropped — too high-cardinality for meaningful 
  one-hot encoding at this sample size, and not central to the analysis goals

- Multi-select columns (pipe-separated values, e.g. diagnosed mental health conditions) were split 
  into one binary flag per distinct condition, rather than treated as a single high-cardinality 
  categorical or via keyword text extraction — this preserves full information without inflating 
  dimensionality through one-hot on near-unique combinations

- Free-text "why or why not" columns were handled via simple keyword-presence flags (e.g. mentions 
  of "stigma", "fear") rather than full TF-IDF/bag-of-words, given the small sample size and high 
  vocabulary variability relative to the number of responses
  - The SPECIAL_NA_AS_CATEGORY global ("*") list initially included "Maybe"/"I don't know"/
  "I am not sure"/"Unsure" alongside structural non-applicability values like "Not applicable 
  to me". This caused a double-encoding bug: for the ~12 columns using one of these values as 
  an intentional ORDINAL MIDPOINT (e.g. negative_consequences_discussion: No < Maybe < Yes), 
  the value was being captured a second time as a redundant "_special" flag column, on top of 
  its ordinal encoding. Fixed by narrowing the global list to ONLY values that are always 
  structural non-applicability (e.g. "Not applicable to me", "N/A (not currently aware)"), 
  and instead listing "I don't know" under specific column keys 
  (formal_mental_health_discussion, anonymity_protected, employer_takes_mental_health_seriously, 
  family_history_mental_illness, mental_health_resources) where the question asks about an 
  EXTERNAL FACT rather than the respondent's own degree of certainty, and "I don't know" 
  should therefore be captured as a separate uncertainty flag rather than an ordinal midpoint

- interferes_with_work_not_treated was verified against its actual value_counts() (Often 538, 
  Not applicable to me 468, Sometimes 363, Rarely 52, Never 12) and confirmed to use the same 
  category set as its sibling column (interferes_with_work_treated), just with a very different 
  distribution (unsurprisingly, most respondents report MORE interference when untreated)

- Ordinal column direction is NOT currently standardized across all columns -- some run 
  negative-to-positive (e.g. willingness_share_mental_illness: closed -> open), others 
  positive-to-negative (e.g. medical_leave_request: easy -> difficult). This doesn't affect 
  the clustering algorithm itself, but will need to be accounted for explicitly when 
  interpreting cluster centroids/profiles later, since a "high" value doesn't consistently 
  mean the same thing (more stigma vs. less stigma) across features

  - works_remotely is ordinal by frequency (Never < Sometimes < Always), but unlike the 
  stigma/comfort/awareness-type ordinal columns, it has no inherent "favorable" direction 
  to align to -- it's a work-arrangement context variable, not an attitude or outcome 
  measure. Left in its natural Never->Always order rather than forced into the 
  favorable=low convention used elsewhere.

  - diagnosed_conditions/believed_conditions/diagnosed_conditions_professional were canonicalized 
  before multi-select splitting: each pipe-separated raw value was mapped to one of ~16 
  canonical condition categories, consolidating spelling/casing variants (e.g. "Autism", 
  "autism spectrum disorder", "Asperger's" -> Autism) and folding historical/informal 
  terminology (e.g. "MCD" -> Attention Deficit Hyperactivity Disorder, since MCD is the old 
  clinical term for ADHD). Genuine free-text write-ins and one-off sarcastic/explanatory 
  sentences that didn't correspond to a checklist category were routed to a residual "Other" 
  bucket rather than each becoming their own column (only 2 respondents ended up in "Other", 
  confirming the mapping captured nearly all actual responses)

- PDD-NOS was merged into Autism, and Schizotypal Personality Disorder was merged into 
  Personality Disorder, since both are clinically considered subtypes/related conditions of 
  the broader category rather than fully distinct diagnoses, and keeping them separate would 
  have created near-empty categories

- "Sexual addiction", "Substance Use Disorder", and "Addictive Disorder" were consolidated into 
  a single Addictive Disorder category, treating substance and behavioral addiction as one 
  broader category for this analysis rather than preserving a fine-grained clinical distinction

- Burn out was deliberately kept as its own separate canonical category rather than merged into 
  Mood Disorder or Adjustment Disorder, despite very low frequency (n=1). The WHO's ICD-11 
  classifies burnout as an occupational phenomenon (chronic unmanaged workplace stress) 
  distinct from a mental health diagnosis, and given this survey's specific focus on mental 
  health in tech workplaces, it was judged conceptually important enough to preserve as its 
  own label even if it doesn't survive later variance thresholding

- Low-frequency canonical condition categories (e.g. Burn out n=1, Sleeping Disorder n=1, 
  Gender Dysphoria n=2) were deliberately NOT manually merged into a catch-all bucket at this 
  stage. This is intentionally left for the upcoming formal feature selection step (variance 
  thresholding), so that removal of near-zero-variance features follows a documented, 
  principled threshold rather than an ad-hoc frequency cutoff decided by eye

  - country_live: the raw column had 40+ distinct countries, most with very low counts (long tail 
  down to n=1). Bucketed to the top 11 countries by frequency (down to Brazil/Switzerland, tied 
  at n=10) plus a residual "Other" category, rather than one-hot encoding the full long tail, 
  which would have produced dozens of near-empty, uninformative columns

- country_work was dropped entirely (not bucketed) rather than kept alongside country_live: the 
  two columns were ~98% identical (most respondents work in the same country they live in), so 
  keeping both would have double-weighted essentially the same signal in clustering

- A hidden non-breaking space character (\xa0, invisible in normal text editors) was found in one 
  raw column header ("...treatment of [nbsp]mental health issues?"), which silently prevented 
  that column from matching the rename map and caused it to skip all downstream processing 
  entirely. Fixed by normalizing all raw column headers (replacing non-breaking spaces, 
  collapsing repeated whitespace) before applying the rename map, rather than patching this one 
  column specifically -- since the same class of hidden-character issue could plausibly affect 
  other columns too

- reveal_to_coworkers and reveal_to_clients were split into two orthogonal dimensions rather than 
  one 4-point ordinal scale: a "direction" (frequency of disclosure: Never < Sometimes < Always) 
  and a "basis" (reason for NOT disclosing: indifference vs. fear of negative impact). Forcing 
  "No, because it doesn't matter" and "No, because it would impact me negatively" onto a single 
  ordered scale would have required deciding which of two very different non-disclosure reasons 
  counts as "more/less" favorable than "sometimes discloses" -- an unjustified ordering the two-
  dimension split avoids

  - ANOVA was initially considered for pre-clustering feature selection, but on closer reading, its 
  natural fit is testing a CONTINUOUS feature against a CATEGORICAL grouping (or another 
  continuous feature, for redundancy checks) -- not something meaningfully applicable across 
  most of this dataset, since nearly all features are ordinal/categorical rather than continuous 
  (age being the one clear exception). Chi-square (categorical vs. categorical) is the more 
  appropriate filter method for the bulk of the feature set instead.
  
  ANOVA's actual value for this project was identified as POST-HOC cluster validation rather than 
  pre-clustering feature selection: using the final cluster assignment as the categorical grouping 
  variable and testing whether age differs significantly across clusters (e.g. "Cluster 3 skews 
  significantly younger, p < 0.01") gives a statistically defensible backing for cluster 
  interpretation, rather than relying on descriptive statistics alone. This will be applied in 
  the cluster-interpretation stage, not the feature-selection stage.

  - Chi-square, like ANOVA, is inherently a PAIRWISE test (one categorical feature vs. another, 
  or vs. a label) -- there is no version that evaluates one feature against all others 
  simultaneously. For unsupervised redundancy-checking, the interpretation direction is 
  OPPOSITE to ANOVA's: chi-square's null hypothesis is independence, so a LOW p-value 
  (independence rejected -> features are significantly associated) suggests possible 
  redundancy, while a HIGH p-value (independence not rejected) suggests the two features 
  carry distinct information and both should be kept. (Note: the course book does not 
  explicitly state this unsupervised-redundancy framing for chi-square the way it does for 
  ANOVA -- this is my own extension by analogy, not a direct textbook claim.)

- Decided against exhaustively testing all pairwise combinations of ordinal/categorical 
  features (~130+ columns would mean 8,000+ pairwise tests). Two reasons: (1) many resulting 
  significant pairs would be statistically real but substantively uninterpretable/not useful 
  for the analysis, and (2) the multiple-comparisons problem -- at alpha=0.05, roughly 5% of 
  8,000+ tests (400+) would show "significant" results by pure chance alone, even with no real 
  underlying relationship, without correction (e.g. Bonferroni). Instead, a small, deliberately 
  chosen set of feature pairs was selected for testing, based on domain reasoning about which 
  pairs plausibly capture overlapping information (e.g. similarly-worded questions like 
  comfortable_discussing_with_coworkers vs. comfortable_discussing_with_supervisor), rather 
  than an exhaustive blind sweep.