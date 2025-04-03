## Structure
* filter_data: A directory of domain names that need to be filtered. This can be used to manually block some domain names that you do not want to be added to the blacklist ranking list.
* high_value_TI.xlsx: List of malicious domain names identified by professional organizations.
* DivideSet.py: Divide the training set and test set of the scorecard algorithm according to high_value_TI.xlsx.
* TagTheMatrix.py: Binary labeling of the data in the matrix based on the training set and test set (particularly malicious/generally malicious).
* GenScoreCard.py: Generate a scorecard based on the annotated matrix.
* ScoreTheMatrix.py: The maliciousness of the domain names in the matrix is ​​scored according to the scorecard to generate a ranking.
* run_full_rank.sh: Portable ranking script.

## Usage
```
    ./run_full_rank.sh <input_file> <output_file>
```
* <input_file>: The indicator matrix obtained after data processing.
* <output_file>: The csv file where the ranked list will be stored.