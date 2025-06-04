# `Compile_Questionnaires.py` 

Processes self-reported questionnaire data collected in CSV format

---

### `compile_EDS(df, drop_cols=True)`

Calculates Everyday Discrimination Scale scores from the passed in DataFrame.

Returns a DataFrame with EDS scores. Drops raw item columns if `drop_cols=True`.

---

### `compile_SWBS(df, subscales=True, drop_cols=True)`

Computes Social Well-Being Scale total and subscale scores.

Computes five subscale scores if `subscales=True`: `WB_Integ`, `WB_Acce`, `WB_Contri`, `WB_Actua`, `WB_Coher`

---

### `compile_RiC(df, subscales=True, drop_cols=True)`

Processes Race in Context data:

Calculates frequency and quality of interactions across racial contexts and adds specific metrics for leisure, work, and online contexts if `subscales=True`.


---

### `compile_CSE(df, subscales=True, drop_cols=True)`

Calculates Collective Self-Esteem metrics such as total score `CSEsum` Computes four subscales if `subscales=True`:  `CSEmember`, `CSEprivate`, `CSEpublic`, `CSEidentity`

---

### `compile_SWLS(df, drop_cols=True)`

Calculates Satisfaction With Life Scale total score by summing all five SWLS items.

---

### `compile_MSPSS(df, subscales=True, drop_cols=True)`

Calculates Multidimensional Scale of Perceived Social Support.

Returns `MSPSS_total` as the mean across all items. Calculates three subscale means if `subscales=True`: `MSPSS_SigOther`, `MSPSS_Family`, `MSPSS_Friend`

---

### `compile_Chronic_Strains(df, drop_cols=True)`

Calculates the total score from the chronic strains scale as the sum of all relevant items.

---

### `main(data_path)`

Loads the raw questionnaire CSV, calls all compilation functions, merges all score DataFrames on articipant ID, writes the merged DataFrame to `data/questionaire_scores.csv`.

---
