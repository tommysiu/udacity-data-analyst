A supplementary python script tuning.py has been provided. Here is the list
of functions for me to work on the project:

1) explore_data()

Function to explore the dataset to find out the size of dataset, the number of
POI and non-POI, and the number of features. It also counts any non-empty values
of each feature.

2) check_all_features()

Function to check the NaN and POI counts for all features. It helps me to see
which features are less important or should be excluded from feature selection.

3) select_features()

Function to print out the SelectKBest scores of selected features.

4) tune_algorithm()

Function to tune the selected algorithms (i.e. DecisionTree and AdaBoost) by
looping through the number of features and using GridSearchCV() to find the
optimal parameter.
