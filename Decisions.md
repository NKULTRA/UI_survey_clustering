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

- Free-text "why or why not" columns were handled via simple keyword-presence flags rather than 
  full TF-IDF/bag-of-words, given the small-per-response sample size and high vocabulary 
  variability relative to the number of responses

- The SPECIAL_NA_AS_CATEGORY global ("*") list initially included "Maybe"/"I don't know"/
  "I am not sure"/"Unsure" alongside structural non-applicability values like "Not applicable 
  to me". This caused a double-encoding bug: for the ~12 columns using one of these values as 
  an intentional ORDINAL MIDPOINT (e.g. negative_consequences_discussion: No < Maybe < Yes), 
  the value was being captured a second time as a redundant "_special" flag column, on top of 
  its ordinal encoding. Fixed by narrowing the global list to ONLY values that are always 
  structural non-applicability (e.g. "Not applicable to me", "N/A (not currently aware)"), 
  and instead listing "I don't know" under specific column keys where the question asks about 
  an EXTERNAL FACT rather than the respondent's own degree of certainty, and "I don't know" 
  should therefore be captured as a separate uncertainty flag rather than an ordinal midpoint

- A second instance of the same double-encoding bug was later found in mental_health_benefits: 
  "Not eligible for coverage / N/A" was in the global special-NA list AND mental_health_benefits 
  was separately one-hot encoded as a NOMINAL column with that same value as one of its own 
  categories -- confirmed via a perfect (r=1.0) Spearman correlation between the two resulting 
  columns. Fixed by removing "Not eligible for coverage / N/A" from the global list, letting the 
  nominal encoding be the single source of truth for that value

- interferes_with_work_not_treated was verified against its actual value_counts() (Often 538, 
  Not applicable to me 468, Sometimes 363, Rarely 52, Never 12) and confirmed to use the same 
  category set as its sibling column (interferes_with_work_treated), just with a very different 
  distribution (unsurprisingly, most respondents report MORE interference when untreated)

- Ordinal column direction was standardized: for stigma/comfort/awareness-type questions, the 
  FAVORABLE outcome (less stigma, more support, more openness) is consistently encoded as the 
  LOWEST value, so a "high" value means the same general kind of thing (more unfavorable/more 
  stigma-associated) across features when interpreting cluster centroids later. Two explicit 
  exceptions were left in their natural, non-favorability order instead:
  - works_remotely: frequency-of-remote-work, not an attitude/outcome measure -- no inherent 
    "favorable" direction to align to
  - past_mental_health_disorder / current_mental_health_disorder: self-reported health status 
    (absent/uncertain/confirmed), not a stigma/comfort measure -- No/Maybe/Yes reflects degree 
    of presence/certainty, not favorability

- reveal_to_coworkers and reveal_to_clients were split into two orthogonal dimensions rather than 
  one 4-point ordinal scale: a "direction" (frequency of disclosure: Never < Sometimes < Always) 
  and a "basis" (reason for NOT disclosing: indifference vs. fear of negative impact). Forcing 
  "No, because it doesn't matter" and "No, because it would impact me negatively" onto a single 
  ordered scale would have required deciding which of two very different non-disclosure reasons 
  counts as "more/less" favorable than "sometimes discloses" -- an unjustified ordering the two-
  dimension split avoids. A later correlation check (r=0.79 between reveal_to_coworkers_direction 
  and reveal_to_coworkers_basis_fear) showed these two dimensions are not fully independent in 
  practice -- people who fear negative consequences also tend to disclose less often, which is 
  intuitively sensible (fear plausibly causes lower disclosure). The split still captures 
  conceptually distinct information (frequency vs. motivation), but this correlation is 
  acknowledged rather than presented as if the split produced fully orthogonal features

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
  stage. This is intentionally left for the formal feature selection step (variance 
  thresholding), so that removal of near-zero-variance features follows a documented, 
  principled threshold rather than an ad-hoc frequency cutoff decided by eye

- country_live: the raw column had 40+ distinct countries, most with very low counts (long tail 
  down to n=1). Bucketed to the top countries by frequency plus a residual "Other" category, 
  rather than one-hot encoding the full long tail, which would have produced dozens of 
  near-empty, uninformative columns

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

- Free-text keyword themes were derived empirically from the actual response data (word 
  frequency analysis + manual review), not guessed from a handful of examples, and verified 
  for coverage (~67-70% of responses match at least one theme; unmatched responses are mostly 
  single-word non-answers or highly idiosyncratic personal narratives). The same theme 
  taxonomy was used for both reason_not_willing_physical_health and 
  reason_not_willing_mental_health to allow direct comparison: discrimination_stigma is by far 
  the dominant theme for the mental health version (296 matches) versus a more even split 
  favoring job_relevance_impact for the physical health version (250 vs. 189/147 for fear and 
  stigma respectively) -- a substantively interesting difference given the two questions are 
  otherwise structurally identical

## Feature selection

- ANOVA was initially considered for pre-clustering feature selection, but on closer reading, its 
  natural fit is testing a CONTINUOUS feature against a CATEGORICAL grouping (or another 
  continuous feature, for redundancy checks) -- not something meaningfully applicable across 
  most of this dataset, since nearly all features are ordinal/categorical rather than continuous 
  (age being the one clear exception). Chi-square (categorical vs. categorical) is the more 
  appropriate filter method for the bulk of the feature set instead.
  
  ANOVA's actual value for this project was identified as POST-HOC cluster validation rather than 
  pre-clustering feature selection: using the final cluster assignment as the categorical grouping 
  variable and testing whether age differs significantly across clusters gives a statistically 
  defensible backing for cluster interpretation, rather than relying on descriptive statistics 
  alone. This will be applied in the cluster-interpretation stage, not the feature-selection stage

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
  than an exhaustive blind sweep

- Two of the chosen chi-square pairs (reveal_to_clients_direction vs. reveal_to_coworkers_
  direction; negative_impact_reveal vs. negative_impact_reveal_coworker) produced very low 
  p-values driven partly by data sparsity rather than a reliable signal: their contingency 
  tables had multiple expected cell counts below 5 (the standard validity threshold for the 
  chi-square approximation) and small effective sample sizes (~172 and ~126 respectively, due 
  to compounding missingness on both columns being required non-missing simultaneously). These 
  two results were flagged as not reliably interpretable rather than trusted at face value, 
  while the other pairs (large effective samples, all expected counts comfortably above 5) 
  were treated as trustworthy

- Mutual Information (MI): same bivariate/pairwise structure as ANOVA and chi-square -- no 
  version tests one feature against all others simultaneously. Unlike chi-square, the book 
  EXPLICITLY confirms the unsupervised-redundancy interpretation directly: "In unsupervised 
  learning, it is often the features that have a low MI value among themselves contribute the 
  most information" -- i.e. LOW MI between two features = independent/complementary = keep 
  both; HIGH MI = overlapping information = likely redundant, consider dropping one. Same 
  redundancy direction as ANOVA conceptually, despite using a different underlying statistic

- MI is more computationally expensive than ANOVA/chi-square (involves density estimation), 
  and its main advantage per the book is capturing NONLINEAR relationships that the other two 
  can miss. Given the cost, MI was applied to the same small, deliberately chosen set of 
  feature pairs already selected for chi-square testing, rather than a separate/exhaustive 
  pairwise sweep -- avoiding both the multiple-comparisons problem and unnecessary runtime cost. 
  MI rankings broadly aligned with chi-square effect-size rankings; notably, the one pair 
  chi-square found not statistically significant (willingness_share_mental_illness vs. 
  unsupportive_response_mental_health_direction, p~=0.065) also showed by far the lowest MI 
  score of all tested pairs -- cross-validating that these two are genuinely unrelated

- Note: sklearn's mutual_info_classif/mutual_info_regression are built for feature-vs-LABEL use 
  (via the SelectKBest API, as in the book's Iris example) -- for pure feature-vs-feature MI 
  with no label, mutual_info_score applied pairwise between two columns directly is the correct 
  approach instead, not the SelectKBest-style call

- Feature variance thresholding: the book's example (threshold=0.6 on the Iris dataset) doesn't 
  transfer to this dataset directly, because raw variance is SCALE-DEPENDENT (measured in 
  squared units of whatever scale a feature happens to use). This dataset mixes binary (0/1, 
  variance mathematically capped at 0.25), ordinal (0-2/0-3/0-4 coded, similarly bounded), and 
  one continuous unscaled feature (age, variance in the hundreds) -- a single flat threshold 
  like 0.6 would eliminate every binary column outright regardless of information content, 
  while age would never be flagged regardless of its actual usefulness. Resolved by min-max 
  scaling every column to [0,1] BEFORE applying VarianceThreshold, so every feature shares the 
  same maximum theoretical variance ceiling (0.25) regardless of its original units or category 
  count, making one global threshold meaningful across the whole mixed-type feature set

- The threshold value itself (0.0099) was derived from a real-world quantity rather than picked 
  by eye: "a condition/category flagged by fewer than ~1% of respondents (~14 people out of 
  1433) is too rare to plausibly define a distinguishable cluster segment" -> p=0.01 -> 
  variance = p(1-p) ~= 0.0099 for a binary feature at that rate. This is a deliberately 
  conservative/permissive threshold (only catches near-constant columns); a higher threshold 
  with a correspondingly different real-world justification (e.g. 5%) would cut more columns

- Variance thresholding must run BEFORE any standardization/scaling step used for the final 
  model input, not after -- since after StandardScaler, every feature has variance exactly 1 
  by construction, which would make a variance-based filter meaningless. (Note: the min-max 
  scaling used for the threshold check itself is a separate, throwaway scaling step, not the 
  final model input's scaling -- see clustering-prep notes.)

- Spearman (not Pearson) correlation was used for the full pairwise correlation matrix, since 
  Spearman is rank-based and valid for ordinal data (only assumes a genuine order exists, not 
  equal-sized intervals between categories) -- unlike Pearson, which assumes roughly continuous, 
  linearly-related variables. At threshold 0.9, three structural findings emerged: (1) the 
  mental_health_benefits double-encoding bug (r=1.0, see above), (2) gender_cleaned_male vs. 
  gender_cleaned_female (r=-0.93), the expected one-hot "dummy variable trap" pattern, and 
  (3) reveal_to_clients_special_not_applicable_to_me vs. reveal_to_coworkers_special_not_
  applicable_to_me (r=0.91), a genuine substantive finding (not redundancy) -- people who never 
  disclosed to clients also tend to have never disclosed to coworkers, plausibly reflecting a 
  shared underlying cause (no diagnosis to disclose, or general non-disclosure tendency)

- At a lower threshold (0.7), the correlation matrix surfaced a clear structural pattern: 
  diagnosed_conditions__X and diagnosed_conditions_professional__X are strongly correlated 
  across most conditions (ADHD 0.80, OCD 0.75, autism 0.74, anxiety 0.73, psychotic disorder 
  0.72), while believed_conditions__X is notably NOT part of this pattern -- consistent with 
  self-reported and professionally-confirmed diagnoses largely agreeing, while "what I believe 
  I might have" captures a genuinely different signal. This is the single largest redundancy 
  finding in the whole feature set and the primary candidate for consolidating the three 
  parallel condition-flag families down to fewer columns

## Imputation

- Missing values were classified into two groups before choosing an imputation strategy: (1) 
  structural missingness explained by survey skip-logic (a gating question determines whether 
  a follow-up question was shown at all), and (2) genuine/residual non-response with no 
  identified structural explanation

- For structural missingness, each gated column gets a dedicated "_not_applicable" flag column 
  (preserving the TRUE reason for missingness) plus a NEUTRAL fill value (the column's own mean, 
  among valid non-missing responses) for the original column. The neutral-fill choice is 
  specifically tied to the downstream algorithm being K-means (distance-based, Euclidean): a 
  fabricated out-of-range value (e.g. max+1) would distort distance calculations by implying 
  "further along the scale than the highest real answer", whereas the mean places a 
  not-applicable respondent at the center of the existing distribution, adding no false 
  directional signal. This reasoning would NOT apply the same way to a tree-based algorithm 
  (which splits on thresholds rather than computing distances), for which an out-of-range 
  sentinel value is a common, legitimate technique instead

- Structural gates were verified empirically (not assumed from question wording) by checking 
  whether the gated column's missingness count matches the gate's predicted group size:
  - previous_employers==0 -> all 11 previous_employers_* columns: a clean, exact match (169/169 
    for every column), confirming this as a reliable structural gate
  - self_employed: found to be a TWO-WAY branch, not a single-direction gate -- self_employed==0 
    (employed) gates ~14 employer-provided-benefit questions, while self_employed==1 
    (self-employed) gates a different pair of questions (medical_coverage, awareness_resources) 
    about personal coverage instead
  - reveal_to_clients_direction=="Never" / reveal_to_coworkers_direction=="Never" were tested as 
    gates for negative_impact_reveal / negative_impact_reveal_coworker: a small mismatch (11 
    rows out of ~1100+ answered despite no valid disclosure-frequency answer) was found and 
    accepted as normal real-world survey-response inconsistency rather than evidence against 
    the gate, given how small it is relative to the total
  - A compound "diagnosed-or-treated" gate (diagnosed_by_professional==0 AND sought_treatment==0) 
    was tested for reveal_to_coworkers/clients_direction, productivity_affected, and 
    interferes_with_work_treated/not_treated. Match quality varied substantially: ~80-84% for 
    the interferes_with_work pair, but only ~42-46% for the other three. Rather than pursue 
    further per-column investigation to find a better explanation for the weaker three, all 
    five were treated uniformly as residual/genuine missingness (plain mean fill, no 
    _not_applicable flag) -- a deliberate scope/consistency trade-off, made explicit rather than 
    implying all five were equally well-explained

- Two config bugs were caught and fixed while building the structural-gate list: 
  (1) negative_impact_reveal was initially listed under both the self_employed==0 group and its 
  correct gate (reveal_to_clients_direction=="Never") -- since imputation fills NaN as it 
  processes each gate in order, whichever group ran first would silently consume the missing 
  values, making the second entry a no-op and misattributing the _not_applicable flag to the 
  wrong (untested) gate; (2) percentage_affected's gate was initially backwards (checked 
  productivity_affected=="Yes" for missingness, the opposite of the real skip-logic, which shows 
  it only when the answer IS "Yes") and additionally referenced the wrong encoded value

- family_history_mental_illness and willingness_share_mental_illness's remaining NaN after 
  extract_special_na_flags exactly match their known "I don't know" / "Not applicable to me (I 
  do not have a mental illness)" counts from the raw data -- confirming these are NOT additional 
  structural gates needed, just the residual after the special-flag mechanism already captured 
  the real signal; plain mean fill is sufficient for what remains

- age's remaining missingness (5 rows) stems from clean_age's outlier removal (invalid ages set 
  to NaN), not survey skip-logic -- treated as genuine missing data requiring plain 
  (median/mean) imputation, not a _not_applicable flag

## Clustering algorithm choice

- K-means was selected despite Euclidean distance being a theoretically imperfect fit for a 
  predominantly binary/ordinal (mostly one-hot and 0-N coded) feature matrix, with only age 
  being genuinely continuous. More theoretically appropriate alternatives for mixed-type data 
  were considered and set aside: K-Prototypes (combines Euclidean distance for numeric features 
  with a matching-based distance for categorical ones) and Gower-distance-based hierarchical 
  clustering (each feature type gets its own appropriate comparison method). K-means was chosen 
  for its simplicity, its role as the course's primary/introductory clustering method, and 
  because it remains extremely common in real-world practice even on encoded mixed-type data, 
  as long as scaling is applied carefully -- this trade-off is acknowledged explicitly rather 
  than presented as if K-means were the objectively optimal choice

## Feature matrix assembly (pending -- to finalize before clustering)

- age_group is PROFILING-ONLY (created for describing cluster demographics in plain language 
  after clustering, e.g. "Cluster 3 skews 45-54") and must be excluded from the model input 
  matrix entirely -- it is never encoded numerically anywhere in the pipeline
- All features must be scaled (StandardScaler, consistent with K-means/Euclidean distance) 
  before clustering -- age's raw range (18-75) would otherwise dominate distance calculations 
  compared to 0/1 binary and 0-1-2/0-1-2-3 ordinal columns


  - All ten chi-square-significant candidate pairs were further checked via contingency-table 
  diagonal concordance (fraction of respondents giving matching answers on both columns). 
  Concordance ranged 40.6%-75.8% across all pairs -- well below a threshold that would 
  justify calling either redundant (compare: past/current_mental_health_disorder at 73%, 
  also judged non-redundant given its ~27% divergent, interpretable subgroup). No column 
  was dropped on redundancy grounds from chi-square testing; the varying context (audience, 
  employer/time period, health domain) across near-identically-worded question pairs 
  consistently produces substantively different answer patterns, not duplicated information.

  - mental_health_benefits vs. previous_employers_mental_health_benefits was tested on the 
  hypothesis that disengaged respondents ("I don't know") would show a consistent pattern 
  across both questions. The two columns also have mismatched category structures (current 
  has 4 categories including "Not eligible for coverage", previous only 3) and the "I don't 
  know" responses did not show a clearly interpretable concentration on the previous-employer 
  side -- the hypothesis was not clearly confirmed. Both columns were kept, as no strong case 
  for redundancy emerged and the association, while chi-square-significant, does not clearly 
  correspond to overlapping information.

  - Mutual Information rankings were compared against chi-square effect-size rankings for all 
  tested pairs. The two methods converged: pairs with the highest chi2 (past/current_mental_
  health_disorder, previous_employers_comfortable_discussing_coworkers/supervisor, career_
  impact/team_view, comfortable_discussing_with_coworkers/supervisor) also showed the highest 
  MI scores, and the one chi-square-nonsignificant pair (willingness_share_mental_illness vs. 
  unsupportive_response_mental_health_direction) also showed by far the lowest MI. This 
  convergence, combined with the contingency-table concordance checks (all pairs 40-76%, well 
  below a redundancy threshold), confirms that no pair tested carries near-duplicate 
  information -- chi-square and MI both correctly flagged genuine associations, but neither 
  corresponds to redundant columns. No features were dropped based on chi-square/MI testing.

  - Two columns flagged as low-variance (post-imputation) were checked against their PRE-imputation 
  variance to distinguish a genuine low-information feature from a mean-imputation artifact:
  - reveal_to_clients_direction: pre-imputation variance = 0.243 (near the 0.25 theoretical max, 
    genuinely well-varying among the 186 respondents who answered) -- the post-imputation 
    near-zero variance was an artifact of ~87% of the column being an identical mean-filled 
    placeholder (this column had very high structural+residual missingness). Overridden and 
    KEPT despite failing the variance threshold, since the underlying feature is genuinely 
    informative among applicable respondents.
  - tech_role: pre-imputation variance = 0.054, still well below the 0.25 max even among the 
    263 respondents who answered (real answers are heavily skewed ~94% Yes / 6% No). This is 
    a genuine property of the data, not an imputation artifact -- DROPPED as originally flagged.

  - All *_not_applicable flag columns gated by self_employed showed near-perfect correlation 
(r=+-1.0) with self_employed itself and with each other -- expected, since they are 
mathematically derived from the same gate condition by construction, not an independent 
finding. Dropped all ~15 self_employed-gated _not_applicable flags, keeping self_employed 
itself as the single, sufficient representation of this information -- unlike the chi-square 
candidate pairs, this is guaranteed redundancy rather than a judgment call.