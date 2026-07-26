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