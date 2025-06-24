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


## results
V1 and V2 have significantly different absolute mood scores (all) but mostly no significant changes in mood
  speed disadvantage hapiness and confidence different in v2 (higher rating in v2)
very different performance in the speed much the perception is similar so the accuracy is higher in v2

The game is "more fair" but players rated it as less fair

ran IAT processing script now comparing D1 scores to PAT variables for v1 and v2
  no correlation with mood or changes in coins collected after manipulation
  or 'How much would you like to keep playing this game?', 'How well are you playing this game right now?'
  or how fair, how enjoyable, how likely would you recommend this game to a friend
  no correlation with accuracy in v1 but weak correlation in v2 (-.451 pearson r sample size 36 needed for significance)
  
tried creating a composite score like the IAT 
  advantage - disavantage average (absolute and minus neutral)
  combined score of happiness had r (.49)

iat questionaires
first 20 of v1 did not have questionaires
demographic shifts

coin positive - coin negative avg with speed diffs


# Executable instructions

* Run `pip install pyinstaller`
* Build the CLI through the custom spec file `pyinstaller pat-cli.spec`
* Run the tool through `./dist/pat-cli [arguments] [path/to/data]`