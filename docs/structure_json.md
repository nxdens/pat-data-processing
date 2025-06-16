# `structure.json`

Block structure defined in the JSON configuration used during the PAT study.

---

### Overview

The `structure.json` file defines:

* The content and layout of each block
* The different possible block orders (`structure0` - `structure7`) used for counterbalancing
* A special structure (`structure8`) containing `"test"` and `"end"`

Participants are assigned one of the `structure0` - `structure7` structures via their condition number in [`rand.yaml`](rand_yaml.md).

---

### `blocks`

Each entry under `"blocks"` defines:

* `description`: a label of the experimental manipulation (e.g., `"coin: neutral -> positive"`).
* `layout`: a sequence of `[segment_name, repeat_count]` pairs that define how the block is structured.

#### Example:

```json
"block2": {
  "description": "coin: neutral -> positive",
  "layout": [
    ["neutral", 2],
    ["questions", 1],
    ["goodCoin", 4],
    ["questions", 1],
    ["after_block_questions", 1]
  ]
}
```