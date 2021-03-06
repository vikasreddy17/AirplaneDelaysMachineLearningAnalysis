import pandas as pd
from sklearn import tree
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import r2_score
import pickle as pik
import os

#load in data
adaboost_cross_val_results = pd.read_csv("AdaBoost_full_crossval_results.csv")
output_test_x = pd.read_csv("output_data/output_test_x.csv")
output_test_y = pd.read_csv("output_data/output_test_y.csv")
output_train_x = pd.read_csv("output_data/output_train_x.csv")
output_train_y = pd.read_csv("output_data/output_train_y.csv")

#test and score
clf = tree.DecisionTreeRegressor(max_depth=4)
clf1 = AdaBoostRegressor(base_estimator=clf, n_estimators=27, learning_rate=(90/1000), random_state=0)
clf1.fit(output_train_x,output_train_y['ARRIVAL_DELAY'])
pik.dump(clf1, open( 'best_AdaBoost_model.pickle','wb'))
predict_val = clf1.predict(output_test_x)
r2_score = r2_score(predict_val, output_test_y)
print('AdaBoost test score using r-squared metric is')
print(r2_score)

#create full dataframe for testing scores from the various models
adaboost_cross_val_best_results = adaboost_cross_val_results.loc[adaboost_cross_val_results['n_estimators'] == 27,:]
adaboost_cross_val_best_results = adaboost_cross_val_best_results.loc[adaboost_cross_val_best_results['max_depth'] == 4,:]
model_test_scores = {'model': [], 'model_test_scores': []}
model_test_scores['model'].append('AdaBoost')
model_test_scores['model_test_scores'].append(r2_score)
model_test_scores = pd.DataFrame(model_test_scores)
model_test_scores['fit_time'] = adaboost_cross_val_best_results['fit_time']
model_test_scores['crossval_train_score'] = adaboost_cross_val_best_results['train_score']
model_test_scores['crossval_test_score'] = adaboost_cross_val_best_results['test_score']
model_test_scores['crossval_train_minus_test'] = adaboost_cross_val_best_results['train_minus_test']
model_test_scores['crossval_train_minus_test'] = adaboost_cross_val_best_results['train_minus_test']
if os.path.isfile('FinalModelScores.csv') == False:
	model_test_scores.to_csv('FinalModelScores.csv', index=None)
else:
	exist_model_test_scores = pd.read_csv('FinalModelScores.csv')
	exist_model_test_scores = pd.concat([exist_model_test_scores, model_test_scores], axis=0)
	exist_model_test_scores.to_csv('FinalModelScores.csv', index=None)

