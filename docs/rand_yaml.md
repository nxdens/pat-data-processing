# `rand.yaml`

Defines how block structures are randomized for each participant. 

---

### Overview

During the study, participants were exposed to the blocks in a random order (counterbalancing conditions). The specific order of blocks each participant was given is indicated by the number assigned to them in `rand.yaml`. These numbers are 0 - 7 as there are 8 total ways to randomize the order of the blocks. 

#### Example:

```yaml
"60": 7
"51": 1
"52": 4
"53": 4
```

[`structure.json`](structure_json.md) adds more information to the type of block and the order of the blocks based on the structure number from `rand.yaml`. 
