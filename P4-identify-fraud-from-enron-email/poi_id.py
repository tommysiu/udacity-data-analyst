#!/usr/bin/python
'''The final estimator and result:
AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None,
          learning_rate=1.0, n_estimators=10, random_state=42)
        Accuracy: 0.87885       Precision: 0.63898      Recall: 0.48850 F1: 0.55370     F2: 0.51265
        Total predictions: 13000        True positives:  977    False positives:  552   False negatives: 1023   True negatives: 10448
'''
import sys
import pickle

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier
from tester import dump_classifier_and_data

from sklearn.ensemble import AdaBoostClassifier

from sklearn.metrics import f1_score
from sklearn.metrics import make_scorer


def create_new_features(dataset):
    for key in dataset.keys():
        # Create new feature 'poi_message_ratio'
        from_messages = dataset[key]['from_messages']
        to_messages = dataset[key]['to_messages']
        from_poi_messages = dataset[key]['from_poi_to_this_person']
        to_poi_messages = dataset[key]['from_this_person_to_poi']

        from_messages = from_messages if from_messages != 'NaN' else 0
        to_messages = to_messages if to_messages != 'NaN' else 0
        from_poi_messages = from_poi_messages if from_poi_messages != 'NaN' else 0
        to_poi_messages = to_poi_messages if to_poi_messages != 'NaN' else 0

        total_messages = from_messages + to_messages
        if total_messages > 0:
            dataset[key]['poi_message_ratio'] = \
                .1*(from_poi_messages + to_poi_messages)/total_messages
        else:
            dataset[key]['poi_message_ratio'] = 0.0

        # Create feature 'major_payment'
        features_to_sum = ['salary', 'bonus', 'exercised_stock_options']
        sum = 0.0
        for f in features_to_sum:
            if (dataset[key][f] != 'NaN'):
                sum = sum + dataset[key][f]
        dataset[key]['major_payment'] = sum

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

# The features list contains a newly created feature 'major_payment'
features_list = ['poi','major_payment', 'exercised_stock_options']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
data_dict.pop('TOTAL', 0)
data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict
create_new_features(my_dataset)

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

### Two classifiers have been tested, namely DecisionTreeClassifier and
### AdaBoostClassifier. The details can be found in tuning.py

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

### The tuning of classifiers were done in tuning.py
clf = AdaBoostClassifier(random_state=42, n_estimators=10)

test_classifier(clf, my_dataset, features_list)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)
