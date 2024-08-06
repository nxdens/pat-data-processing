# pat_data_processing

[![codecov](https://codecov.io/gh/nxdens/pat-data-processing/branch/main/graph/badge.svg?token=pat-data-processing_token_here)](https://codecov.io/gh/nxdens/pat-data-processing)
[![CI](https://github.com/nxdens/pat-data-processing/actions/workflows/main.yml/badge.svg)](https://github.com/nxdens/pat-data-processing/actions/workflows/main.yml)

Processing pipeline for PAT data

## Install it from PyPI
Not yet set up on PyPI
```bash
pip install pat_data_processing
```

## Usage

```bash
$ python -m pat_data_processing --help
#or
$ pat_data_processing --help
```

See help message for available parameters. Must be run with valid data folder as first positional argument. Data folder must contain folder of PAT data files and questionaire data cooresponding to the PAT each PAT ID contained in the PAT data folder.

There are currently 3 stages to this pipeline. 
  1. Parses the `data.json` files for each PAT ID
  2. Compiles the `data.json` into a "simple" csv format containing 5 columns: PAT ID, Block Type, Question Type, Question, and Score
  3. Combines the data from the previous two stages into a single csv file. In addition, the difference and ratios between the neutral and manipulation blocks are calculated alongside the accuracy of each players self assessed performance.


