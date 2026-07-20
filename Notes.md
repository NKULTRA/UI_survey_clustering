# General column descriptions

- Are you self employed
0 stands probably for 'No'
0    1146
1     28

- How many employees does your company or organization have?
categorical 
26-100            292
NaN               287
More than 1000    256
100-500           248
6-25              210
500-1000           80
1-5                60

- Is your employer primarily a tech company/organization?
here should be 0 as well 'No'
1.0    883
NaN    287
0.0    263

- Is your primary role within your company related to tech/IT?
a lot of missing numbers 
-> also as this is for HR in Tech, only keep 1, but this would create a really small dataset -> what is the best approach here?
NaN    1170
1.0     248
0.0      15

- Does your employer provide mental health benefits as part of healthcare coverage?
how to treat i don't know here, might make sense to set them to NA?
Yes                                531
I don't know                       319
NaN                                287
No                                 213
Not eligible for coverage / N/A     83

- Do you know the options for mental health care available under your employer-provided coverage?
NaN              420
No               354
I am not sure    352
Yes              307

- Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?
No              813
NaN             287
Yes             230
I don't know    103

- Does your employer offer resources to learn more about mental health concerns and options for seeking help?
No              531
I don't know    320
Yes             295
NaN             287

- Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources provided by your employer?
I don't know    742
Yes             320
NaN             287
No               84

- If a mental health issue prompted you to request a medical leave from work, asking for that leave would be:
this is normally a likert (ordinal) scale, but how to treat I dont know?
NaN                           287
Somewhat easy                 281
Very easy                     220
Somewhat difficult            199
Neither easy nor difficult    178
I don't know                  150
Very difficult                118

- Do you think that discussing a mental health disorder with your employer would have negative consequences?
Maybe    487
No       438
NaN      287
Yes      221

- Do you think that discussing a physical health issue with your employer would have negative consequences?
No       837
NaN      287
Maybe    268
Yes       41

- Would you feel comfortable discussing a mental health disorder with your coworkers?
Maybe    479
No       392
NaN      287
Yes      275

- Would you feel comfortable discussing a mental health disorder with your direct supervisor(s)?
Yes      428
Maybe    382
No       336
NaN      287

- Do you feel that your employer takes mental health as seriously as physical health?
I don't know    493
Yes             350
No              303
NaN             287

- Have you heard of or observed negative consequences for co-workers who have been open about mental health issues in your workplace?
No     1048
NaN     287
Yes      98

- Do you have medical coverage (private insurance or state-provided) which includes treatment of mental health issues?
what is here yes and no? probably right to assume that this is consistent in this dataset (so 0 is no)
NaN    1146
1.0     185
0.0     102

- Do you know local or online resources to seek help for a mental health disorder?
standardize to Yes, No - but what about I know some?
NaN                     1146
I know some              141
Yes, I know several       83
No, I don't know any      63

- If you have been diagnosed or treated for a mental health disorder, do you ever reveal this to clients or business contacts?
almost a scale?
NaN                                          1146
Not applicable to me                          101
No, because it would impact me negatively      83
Sometimes, if it comes up                      57
No, because it doesn't matter                  44
Yes, always                                     2

- If you have revealed a mental health issue to a client or business contact, do you believe this has impacted you negatively?
subset of previous question?
NaN             1289
I'm not sure      66
No                42
Yes               36

- If you have been diagnosed or treated for a mental health disorder, do you ever reveal this to coworkers or employees?
NaN                                          1146
Not applicable to me                          111
Sometimes, if it comes up                      99
No, because it would impact me negatively      51
No, because it doesn't matter                  15
Yes, always                                    11

- If you have revealed a mental health issue to a coworker or employee, do you believe this has impacted you negatively?
also subset of previous question?
NaN                     1146
Not applicable to me     133
I'm not sure              62
No                        57
Yes                       35

- Do you believe your productivity is ever affected by a mental health issue?
NaN                     1146
Yes                      204
Unsure                    38
Not applicable to me      31
No                        14

- If yes, what percentage of your work time (time performing primary or secondary job functions) is affected by a mental health issue?
here a subset again of the previous question
NaN        1229
1-25%        92
26-50%       72
51-75%       26
76-100%      14

- Do you have previous employers?
1    1264
0     169

- Have your previous employers provided mental health benefits?
Some did             391
No, none did         372
I don't know         313
Yes, they all did    188
NaN                  169

- Were you aware of the options for mental health care provided by your previous employers?
N/A (not currently aware)          582
I was aware of some                384
Yes, I was aware of all of them    181
NaN                                169
No, I only became aware later      117

- Did your previous employers ever formally discuss mental health (as part of a wellness campaign or other official communication)?
None did             890
Some did             255
NaN                  169
I don't know          86
Yes, they all did     33

- Did your previous employers provide resources to learn more about mental health issues and how to seek help?
None did             842
Some did             371
NaN                  169
Yes, they all did     51

- Was your anonymity protected if you chose to take advantage of mental health or substance abuse treatment resources with previous employers?
I don't know    860
NaN             169
Yes, always     164
No              121
Sometimes       119

- Do you think that discussing a mental health disorder with previous employers would have negative consequences?
Some of them        615
I don't know        310
Yes, all of them    226
NaN                 169
None of them        113

- Do you think that discussing a physical health issue with previous employers would have negative consequences?
Some of them        631
None of them        559
NaN                 169
Yes, all of them     74

- Would you have been willing to discuss a mental health issue with your previous co-workers?
Some of my previous employers           740
No, at none of my previous employers    430
NaN                                     169
Yes, at all of my previous employers     94

- Would you have been willing to discuss a mental health issue with your direct supervisor(s)?
Some of my previous employers           654
No, at none of my previous employers    416
NaN                                     169
I don't know                            101
Yes, at all of my previous employers     93

- Did you feel that your previous employers took mental health as seriously as physical health?
None did             463
Some did             427
I don't know         331
NaN                  169
Yes, they all did     43

- Did you hear of or observe negative consequences for co-workers with mental health issues in your previous workplaces?
None of them        758
Some of them        444
NaN                 169
Yes, all of them     62

- Would you be willing to bring up a physical health issue with a potential employer in an interview?
Maybe    633
No       441
Yes      359

- Why or why not?
a lot of different answers in this one, here i need to apply some of the described methods from the script (bag of words e.g.)
NaN                                                                                              338
Not relevant                                                                                       3
Fear of discrimination                                                                             3
I don't know                                                                                       3
None of their business.                                                                            2
                                                                                                ... 
I would be afraid it would reflect poorly on me.                                                   1
I believe my health information is my personal business                                            1
 QF                                                                                                1
Fear that doing so would cause the employer to factor in additional health insurance expense.      1
Stigma with some diseases  

- Would you bring up a mental health issue with a potential employer in an interview?
No       883
Maybe    438
Yes      112

- Why or why not?.1
same as before, also this column has the same name as the other one.. Also directly visible is Stigma. / Stigma or only "E"
this probably needs a lot of manual corrections?
also this is a subset of the previous question
NaN                                                                                                                         307
Stigma                                                                                                                       14
Stigma.                                                                                                                       9
Same as above                                                                                                                 7
See above                                                                                                                     4
                                                                                                                           ... 
I would be certain it would reflect poorly on me.                                                                             1
As previously stated, my health information is personal                                                                       1
E                                                                                                                             1
Fear that the employer would consider additional health insurance expense and would doubt my ability to execute my work.      1
Feels like I'm making a mountain out of a molehill

- Do you feel that being identified as a person with a mental health issue would hurt your career?
is this ordinal?
Maybe                         588
Yes, I think it would         563
No, I don't think it would    147
Yes, it has                   105
No, it has not                 30

- Do you think that team members/co-workers would view you more negatively if they knew you suffered from a mental health issue?
Maybe                           591
Yes, I think they would         403
No, I don't think they would    348
No, they do not                  49
Yes, they do                     42

- How willing would you be to share with friends and family that you have a mental illness?
again a likert scale here
Somewhat open                                            640
Very open                                                251
Somewhat not open                                        214
Neutral                                                  141
Not applicable to me (I do not have a mental illness)    112
Not open at all                                           75

- Have you observed or experienced an unsupportive or badly handled response to a mental health issue in your current or previous workplace?
No                    567
Maybe/Not sure        346
Yes, I observed       264
Yes, I experienced    167
NaN                    89

- Have your observations of how another individual who discussed a mental health disorder made you less likely to reveal a mental health issue yourself in your current workplace?
NaN      776
Yes      246
No       234
Maybe    177

- Do you have a family history of mental illness?
Yes             670
No              488
I don't know    275

- Have you had a mental health disorder in the past?
Yes      736
No       451
Maybe    246

- Do you currently have a mental health disorder?
Yes      575
No       531
Maybe    327

- If yes, what condition(s) have you been diagnosed with?
NaN                                                                                                                                                                             865
Anxiety Disorder (Generalized, Social, Phobia, etc)|Mood Disorder (Depression, Bipolar Disorder, etc)                                                                           117
Mood Disorder (Depression, Bipolar Disorder, etc)                                                                                                                               102
Anxiety Disorder (Generalized, Social, Phobia, etc)                                                                                                                              47
Anxiety Disorder (Generalized, Social, Phobia, etc)|Mood Disorder (Depression, Bipolar Disorder, etc)|Attention Deficit Hyperactivity Disorder                                   26
                                                                                                                                                                               ... 
Eating Disorder (Anorexia, Bulimia, etc)                                                                                                                                          1
Anxiety Disorder (Generalized, Social, Phobia, etc)|Mood Disorder (Depression, Bipolar Disorder, etc)|Attention Deficit Hyperactivity Disorder|Dissociative Disorder              1
Schizotypal Personality Disorder                                                                                                                                                  1
Anxiety Disorder (Generalized, Social, Phobia, etc)|Post-traumatic Stress Disorder|Stress Response Syndromes|Autism spectrum disorder                                             1
Obsessive-Compulsive Disorder|Eating Disorder (Anorexia, Bulimia, etc)|Mood Disorder (Depression, Bipolar Disorder, etc)|Anxiety Disorder (Generalized, Social, Phobia, etc)      1

- If maybe, what condition(s) do you believe you have?
here but also in the previous are some answers seperated by a pipe, so in order to have this i need to seperate them and bring them together
NaN  1111
Mood Disorder (Depression, Bipolar Disorder, etc)     55
Anxiety Disorder (Generalized, Social, Phobia, etc)|Mood Disorder (Depression, Bipolar Disorder, etc)           49
Anxiety Disorder (Generalized, Social, Phobia, etc)        35
Mood Disorder (Depression, Bipolar Disorder, etc)|Attention Deficit Hyperactivity Disorder         10
....                                                                                                              ... 
Anxiety Disorder (Generalized, Social, Phobia, etc)|Mood Disorder (Depression, Bipolar Disorder, etc)|Attention Deficit Hyperactivity Disorder|Post-traumatic Stress Disorder|Addictive Disorder            1
Stress Response Syndromes|Post-traumatic Stress Disorder|Personality Disorder (Borderline, Antisocial, Paranoid, etc)|Attention Deficit Hyperactivity Disorder|Mood Disorder (Depression, Bipolar Disorder, etc)             1
Substance Use Disorder|Obsessive-Compulsive Disorder             1
Addictive Disorder                                               1
Anxiety Disorder (Generalized, Social, Phobia, etc)|Mood Disorder (Depression, Bipolar Disorder, etc)|Attention Deficit Hyperactivity Disorder|Personality Disorder (Borderline, Antisocial, Paranoid, etc)|Addictive Disorder 1

- Have you been diagnosed with a mental health condition by a medical professional?
half of them ?!
No     717
Yes    716

- If so, what condition(s) were you diagnosed with?
NaN                                                             722
Mood Disorder (Depression, Bipolar Disorder, etc)               187
Anxiety Disorder (Generalized, Social, Phobia, etc)|Mood Disorder (Depression, Bipolar Disorder, etc)             150
Anxiety Disorder (Generalized, Social, Phobia, etc)                64
Anxiety Disorder (Generalized, Social, Phobia, etc)|Mood Disorder (Depression, Bipolar Disorder, etc)|Attention Deficit Hyperactivity Disorder           33
 ... 
ADD (w/o Hyperactivity)                       1
Addictive Disorder|Anxiety Disorder (Generalized, Social, Phobia, etc)|Mood Disorder (Depression, Bipolar Disorder, etc)|Eating Disorder (Anorexia, Bulimia, etc)|Attention Deficit Hyperactivity Disorder|Obsessive-Compulsive Disorder|Post-traumatic Stress Disorder|Dissociative Disorder      1
Eating Disorder (Anorexia, Bulimia, etc)           1
Schizotypal Personality Disorder         1
autism spectrum disorder

- Have you ever sought treatment for a mental health issue from a mental health professional?
1    839
0    594

- If you have a mental health issue, do you feel that it interferes with your work when being treated effectively?
likert scale
Not applicable to me    557
Sometimes               369
Rarely                  322
Never                   120
Often                    65

- What is your age?
someone said 15? maybe some implausbile values in here
30     94
31     82
29     79
28     74
35     74
32     72
34     69
33     69
26     64
27     63
37     59
39     55
38     54
36     50
25     44
24     42
40     36
22     32
44     31
43     30
42     29
45     27
41     24
23     24
...
15      1
65      1
74      1
70      1

- What is your gender?
Male                                       610
male                                       249
Female                                     153
female                                      95
M                                           86
 ... 
female-bodied; no feelings about gender      1
cis man                                      1
AFAB                                         1
Transgender woman                            1
MALE                                         1

- What country do you live in?
United States of America    840
United Kingdom              180
Canada                       78
Germany                      58
Netherlands                  48
Australia                    35
Sweden                       19
France                       16
Ireland                      15
Brazil                       10
Switzerland                  10
Russia                        9
India                         9
New Zealand                   9
Denmark                       7
Finland                       7
Bulgaria                      7
Belgium                       5
Italy                         5
Poland                        4
Spain                         4
South Africa                  4
Austria                       4
Romania                       4
...
China                         1
Guatemala                     1
Taiwan                        1
Serbia                        1

- What US state or territory do you live in?
NaN                     593
California              130
Illinois                 56
Michigan                 48
New York                 45
Washington               43
Texas                    43
Minnesota                42
Oregon                   37
Pennsylvania             33
Colorado                 28
Tennessee                27
Indiana                  25
Ohio                     25
Massachusetts            23
Florida                  21
North Carolina           21
Maryland                 16
Virginia                 15
Georgia                  14
Kansas                   14
Wisconsin                13
Oklahoma                 13
Nebraska                 12
...
Alaska                    2
South Carolina            1
Montana                   1
Delaware                  1

- What country do you work in?
maybe bring this down to continents?
United States of America    851
United Kingdom              183
Canada                       74
Germany                      58
Netherlands                  47
Australia                    34
Sweden                       20
Ireland                      15
France                       14
Brazil                       10
Switzerland                  10
Russia                        9
India                         9
New Zealand                   9
Denmark                       7
Finland                       7
Bulgaria                      7
Belgium                       5
Poland                        4
South Africa                  4
Austria                       4
Czech Republic                3
Spain                         3
Norway                        3
...
Ecuador                       1
China                         1
Guatemala                     1
Serbia                        1

- What US state or territory do you work in?
NaN                     582
California              141
Illinois                 58
New York                 49
Michigan                 47
Texas                    44
Minnesota                43
Washington               42
Oregon                   34
Pennsylvania             32
Tennessee                28
Colorado                 28
Indiana                  25
Ohio                     25
Massachusetts            25
North Carolina           21
Florida                  19
Georgia                  14
Kansas                   14
Maryland                 14
Oklahoma                 14
Wisconsin                14
Virginia                 13
Nebraska                 12
...
West Virginia             1
South Carolina            1
Montana                   1
Delaware                  1

- Do you work remotely?
Sometimes    757
Always       343
Never        333



