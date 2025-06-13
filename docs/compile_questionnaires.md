# `Compile_Questionnaires.py` 

Processes self-reported questionnaire data collected in CSV format. This file compiles:

* `Everyday Discrimination Scale (EDS)`

* `Social Well-Being Scale (SWBS)` 
    * `WB_Integ` (Social Integration)
    * `WB_Acce` (Social Acceptance)
    * `WB_Contri` (Social Contribution)
    * `WB_Actua` (Social Actualization)
    * `WB_Coher` (Social Coherence)

* `Race in Context (RiC)`
    * leisure
    * work
    * online environments

* `Collective Self-Esteem Scale (CSE) looks at total score (CSEsum)`
    * `CSEmember` (membership esteem)
    * `CSEprivate` (private regard)
    * `CSEpublic` (public regard)
    * `CSEidentity` (identity importance)
    
* `Satisfaction With Life Scale (SWLS)`

* `Multidimensional Scale of Perceived Social Support (MSPSS)`
    * `MSPSS_SigOther` (significant others)
    * `MSPSS_Family` (family members) 
    * `MSPSS_Friend` (friends)
    
* `Chronic Strains Scale`

Merges all compiled scores by participant ID and outputs a unified DataFrame for analysis.


Tabular summary:

| Category                                                | Function                    | Scale + Subscales                                                                  |
|---------------------------------------------------------|-----------------------------|------------------------------------------------------------------------------------|
| Everyday Discrimination Scale (EDS)                     | `compile_EDS`               | `EDS_total`, `EDS_ChroTotal` (chronic weights applied)                            |
| Social Well-Being Scale (SWBS)                          | `compile_SWBS`              | `WB_Integ`, `WB_Acce`, `WB_Contri`, `WB_Actua`, `WB_Coher`, `WellBeingSum`        |
| Race in Context (RiC)                                   | `compile_RiC`               | Frequency and quality across leisure, work, online   |
| Collective Self-Esteem Scale (CSE)                      | `compile_CSE`               | `CSEsum`, `CSEmember`, `CSEprivate`, `CSEpublic`, `CSEidentity`                   |
| Satisfaction With Life Scale (SWLS)                     | `compile_SWLS`              | `SWLSSum`                                                                          |
| Multidimensional Scale of Perceived Social Support (MSPSS) | `compile_MSPSS`           | `MSPSS_total`, `MSPSS_SigOther`, `MSPSS_Family`, `MSPSS_Friend`                   |
| Chronic Strains Scale                                   | `compile_Chronic_Strains`   | `ChroStrain_total`                                                                 |


---

### `compile_EDS(df, drop_cols=True)`

Calculates Everyday Discrimination Scale scores from the passed in DataFrame.

Calculates `EDS_total` through summing raw EDS item responses which is extracted from the DataFrame passed in. 

Calculates `EDS_ChroTotal` through mapping each response to a fixed weight (based on frequency) and summing the result across items. The weights used are: `[0, 0.5, 3, 36, 104, 260]`. 

Returns a DataFrame with EDS scores. Drops raw item columns if `drop_cols=True`.

---

### `compile_SWBS(df, subscales=True, drop_cols=True)`

Calculates Social Well-Being Scale total through summing the subscales `WB_Integ`, `WB_Acce`, `WB_Contri`, `WB_Actua`, and `WB_Coher`. 

If `subscales=True`, calculates five subscale scores:

* `WB_Integ`: Social Integration
* `WB_Acce`: Social Acceptance
* `WB_Contri`: Social Contribution
* `WB_Actua`: Social Actualization
* `WB_Coher`: Social Coherence

Returns a DataFrame with total (and subscale scores if `subscales=True`). Drops raw item columns if `drop_cols=True`.

---

### `compile_RiC(df, subscales=True, drop_cols=True)`

Processes Race in Context data.

Calculates:

* `RiC_Frequency`: frequency of interactions across racial contexts  
* `RiC_Quality`: quality of interactions across racial contexts  
* `RiC_AveSameRace_freq`: average frequency of same-race interactions  
* `RiC_AveDiffRace_freq`: average frequency of different-race interactions  
* `RiC_AveSameRace_quali`: average quality of same-race interactions  
* `RiC_AveDiffRace_quali`: average quality of different-race interactions  

If `subscales=True`, also includes frequency and quality metrics for:

* leisure
* work
* online contexts

Returns a DataFrame with derived `RiC` metrics. Drops raw item columns if `drop_cols=True`.

---

### `compile_CSE(df, subscales=True, drop_cols=True)`

Calculates Collective Self-Esteem (CSE) metrics from the passed in DataFrame.

Calculates:

* `CSEsum`: total CSE score by summing all items

If `subscales=True`, calculates the four subscale scores:

* `CSEmember`: membership esteem
* `CSEprivate`: private evaluation
* `CSEpublic`: public evaluation
* `CSEidentity`: identity importance

Returns a DataFrame with CSE score(s). Drops raw item columns if `drop_cols=True`.

---

### `compile_SWLS(df, drop_cols=True)`

Calculates Satisfaction With Life Scale (SWLS) total score by summing all SWLS items.

Returns a DataFrame with `SWLS` score. Drops raw item columns if `drop_cols=True`.

---

### `compile_MSPSS(df, subscales=True, drop_cols=True)`

Calculates Multidimensional Scale of Perceived Social Support.

Calculates:

* `MSPSS_total`: average of all MSPSS raw items

If `subscales=True`, also calculates:

* `MSPSS_SigOther`: support from significant others
* `MSPSS_Family`: support from family
* `MSPSS_Friend`: support from friends

Returns a DataFrame with score(s). Drops raw item columns if `drop_cols=True`.

---

### `compile_Chronic_Strains(df, drop_cols=True)`

Calculates the total score from the chronic strains scale as the sum of raw Chronic Stains items.

Returns a DataFrame with score. Drops raw item columns if `drop_cols=True`.

---

### `main(data_path)`

Loads the raw questionnaire CSV, calls each compilation function, merges all score DataFrames on participant ID, writes the merged DataFrame to `data/questionaire_scores.csv`.

---
