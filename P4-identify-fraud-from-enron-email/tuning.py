#!/usr/bin/python

import sys
import pickle

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from tester import test_classifier

from sklearn.feature_selection import SelectKBest

from sklearn.preprocessing import MinMaxScaler

from sklearn.grid_search import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

from sklearn.metrics import f1_score
from sklearn.metrics import make_scorer

def get_data(create_feature = True):
    with open("final_project_dataset.pkl", "r") as data_file:
        data_dict = pickle.load(data_file)

    # Remove outliers
    data_dict.pop('TOTAL', 0)
    data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)

    # Create new features
    if create_feature:
        create_new_features(data_dict)

    return data_dict

def check_feature_poi_ratio(data, feature):
    count_val = 0
    count_val_NaN = 0
    count_poi = 0
    count_poi_NaN = 0

    for k in data:
        poi = data[k]['poi']
        val = data[k][feature]
        if val != 'NaN':
            count_val += 1
            if poi:
                count_poi += 1
        else:
            count_val_NaN += 1
            if poi:
                count_poi_NaN += 1

    print "Feature [%s]:\n\t non-NaN count = %d (with %d POI), NaN count = %d (with %d POI)" % \
        (feature, count_val, count_poi, count_val_NaN, count_poi_NaN)

def get_full_feature_list():
    features = ['poi', 'to_messages', 'deferral_payments', 'expenses', 'deferred_income', \
        'from_poi_to_this_person', 'restricted_stock_deferred', 'shared_receipt_with_poi', \
        'loan_advances', 'from_messages', 'other', 'director_fees', 'bonus', 'total_stock_value', \
        'from_this_person_to_poi', 'long_term_incentive', 'restricted_stock', 'salary', \
        'total_payments', 'exercised_stock_options']
    return features

def get_feature_list():
    features = ['poi','major_payment', 'exercised_stock_options', 'bonus', 'salary', \
        'deferred_income', 'long_term_incentive', 'restricted_stock', \
        'shared_receipt_with_poi', 'loan_advances', 'poi_message_ratio', \
        'director_fees', 'deferral_payments', 'restricted_stock_deferred']
    return features

def get_features_and_labels(dataset, features_list):
    data = featureFormat(dataset, features_list)
    labels, features = targetFeatureSplit(data)

    return data, labels, features

def get_feature_scores(dataset, features_list):
    data,labels,features = get_features_and_labels(dataset, features_list)

    k = len(features_list) - 1
    kbest = SelectKBest(k=k)
    kbest.fit(features, labels)

    # exclude the first poi feature from the feature list
    pairs = zip(features_list[1:], kbest.scores_)
    pairs = list(reversed(sorted(pairs, key = lambda x:x[1])))
    for t in pairs:
        print t[0], ": ", t[1]
    tmp_list,score_list = zip(*pairs)
    return tmp_list[0:k]

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

def tune_classifier(classifier, clf_params, max_features):
    ### features_list is a list of strings, each of which is a feature name.
    ### The first feature must be "poi".
    features_list = get_feature_list()

    ### Create new feature(s)
    ### Store to my_dataset for easy export below.
    my_dataset = get_data()

    ### Extract features and labels from dataset for local testing
    features_list = features_list[0:max_features+1]
    data, labels, features = get_features_and_labels(my_dataset, features_list)

    ### Tune your classifier to achieve better than .3 precision and recall
    ### using our testing script. Check the tester.py script in the final project
    ### folder for details on the evaluation method, especially the test_classifier
    ### function. Because of the small size of the dataset, the script uses
    ### stratified shuffle split cross validation. For more info:
    ### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

    from sklearn.cross_validation import train_test_split
    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.3, random_state=42)

    # Testing
    clf = GridSearchCV(classifier, param_grid=clf_params, scoring=make_scorer(f1_score))
    clf.fit(features_train, labels_train)
    clf_final = clf.best_estimator_
    print "The best estimator = ", clf_final
    test_classifier(clf_final, my_dataset, features_list, 1000)

def explore_data():
    print "=================================="
    print "Explore the dataset"
    print "=================================="
    data = get_data(False)

    ## Data Exploration part
    print "Size of dataset =", len(data)
    n_poi = 0
    for k in data:
        if data[k]['poi'] == True:
            n_poi = n_poi + 1
    print "# of POI =", n_poi
    print "# of non-POI =", len(data) - n_poi
    print "# of features =", len(data.values()[0])

    count = {}
    for k in data.values()[0]:
        count[k] = 0

    for k in data:
        d = data[k]
        for name in d:
            if isinstance(d[name], int) and d[name] > 0:
                count[name] = count[name] + 1
            else:
                if d[name] != '' and d[name] != 'NaN':
                    count[name] = count[name] + 1

    print "The counts of non-empty features are:", count

def check_all_features():
    print "========================================="
    print "Check NaN and POI counts for all features"
    print "========================================="
    data = get_data(False)
    for feature in data.values()[0]:
        if feature not in ['poi', 'email_address']:
            check_feature_poi_ratio(data, feature)

def select_features():
    print "=================================="
    print "Find the univariate feature scores"
    print "=================================="
    my_dataset = get_data()
    features_list = get_full_feature_list()
    get_feature_scores(my_dataset, features_list)

    print "=================================="
    print "Find the target feature scores"
    print "=================================="
    features_list = get_feature_list()
    get_feature_scores(my_dataset, features_list)

def tune_algorithm():
    print "=================================="
    print "Tune the Decision Tree classifier"
    print "=================================="
    classifier = DecisionTreeClassifier(random_state=42)
    clf_params = dict(min_samples_split=range(2,10))
    for n in range(1, 14):
        print "Tune algorithm for {0} features:".format(n)
        tune_classifier(classifier, clf_params, n)

    print "=================================="
    print "Tune the AdaBoost classifier"
    print "=================================="
    classifier = AdaBoostClassifier(random_state=42)
    clf_params = dict(n_estimators=[10,20,30,40,50,60,70])
    for n in range(1, 14):
        print "Tune algorithm for {0} features:".format(n)
        tune_classifier(classifier, clf_params, n)

def main():
    explore_data()
    check_all_features()
    select_features()
    tune_algorithm()
