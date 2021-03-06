#import packages
import pandas as pd
import seaborn as sea
import sklearn as skl
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import datasets
from sklearn import svm
from tqdm import tqdm
import os


#split data
if os.path.isfile('output_data/output_train_x.csv') == False or os.path.isfile('output_data/output_train_y.csv') == False or os.path.isfile('output_data/output_test_x.csv') == False or os.path.isfile('output_data/output_test_y.csv') == False:
  #load data
  flightsdata = pd.read_csv("Dataset/flights.csv")

  #missing values treatment and data cleaning
  flightsdata = flightsdata.loc[flightsdata['CANCELLED'] == 0,:]
  flightsdata = flightsdata.loc[flightsdata['MONTH'] != 10,:]
  flightsdata = flightsdata[['MONTH', 'DAY_OF_WEEK', 'AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'DEPARTURE_TIME', 'SCHEDULED_DEPARTURE', 'DEPARTURE_DELAY', 'SCHEDULED_TIME', 'SCHEDULED_ARRIVAL', 'ARRIVAL_DELAY']]
  flightsdata = flightsdata.loc[flightsdata.isna().sum(axis=1) == 0, :]
  flightsdata = flightsdata.sample(1000000)

  #dummy data treatment

  #dummy airline
  dummy_AIRLINE_concat_set = None

  airlines = pd.read_csv("Dataset/airlines.csv")
  dummy_AIRLINE = airlines['IATA_CODE']
  dummy_rep_AIRLINE = []
  for i in range(14):
    dummy_rep_AIRLINE.append(i)

  airline_replace = {}
  airline_replace['dummy_rep_AIRLINE'] = dummy_rep_AIRLINE
  airline_replace = pd.DataFrame(airline_replace)
  dummy_AIRLINE = pd.concat([airline_replace, dummy_AIRLINE], axis=1)

  flightsdata_airline = flightsdata['AIRLINE'].tolist()
  flightsdata1 = None
  dummy_AIRLINE_list = []
  for i in tqdm(range(1000000)):
    num=0
    for airline in dummy_AIRLINE['IATA_CODE']:
      if flightsdata_airline[i] == airline:
        dummy_AIRLINE_list.append(num)
      else:
        num = num + 1
  flightsdata['dummy_AIRLINE'] = dummy_AIRLINE_list

  # dummy OG airport
  ogairport = pd.read_csv("Dataset/airports.csv")
  dummy_OGAIRPORT = ogairport['IATA_CODE']
  dummy_rep_OGAIRPORT = []
  for i in range(322):
    dummy_rep_OGAIRPORT.append(i)
 
  ogairport_replace = {}
  ogairport_replace['dummy_rep_OGAIRPORT'] = dummy_rep_OGAIRPORT
  ogairport_replace = pd.DataFrame(airline_replace)
  dummy_OGAIRPORT = pd.concat([ogairport_replace, dummy_OGAIRPORT], axis=1)

  flightsdata_ogairport = flightsdata['ORIGIN_AIRPORT'].tolist()
  flightsdata1 = None
  dummy_OGAIRPORT_list = []
  for i in tqdm(range(1000000)):
    num=0
    for ogairport in dummy_OGAIRPORT['IATA_CODE']:
      if flightsdata_ogairport[i] == ogairport:
        dummy_OGAIRPORT_list.append(num)
      else:
        num = num + 1
  flightsdata['dummy_OGAIRPORT'] = dummy_OGAIRPORT_list

  #dummy destination airport
  destination_airport = pd.read_csv("Dataset/airports.csv")
  dummy_DAIRPORT = destination_airport['IATA_CODE']
  dummy_rep_DAIRPORT = []
  for i in range(322):
    dummy_rep_OGAIRPORT.append(i)
 
  dairport_replace = {}
  dairport_replace['dummy_rep_OGAIRPORT'] = dummy_rep_DAIRPORT
  dairport_replace = pd.DataFrame(airline_replace)
  dummy_DAIRPORT = pd.concat([dairport_replace, dummy_DAIRPORT], axis=1)

  flightsdata_dairport = flightsdata['DESTINATION_AIRPORT'].tolist()
  print(type(flightsdata_dairport))
  flightsdata1 = None
  dummy_DAIRPORT_list = []
  for i in tqdm(range(1000000)):
    num=0
    for dairport in dummy_DAIRPORT['IATA_CODE']:
      if flightsdata_dairport[i] == dairport:
        dummy_DAIRPORT_list.append(num)
      else:
        num = num + 1
  print(len(dummy_DAIRPORT_list))
  flightsdata['dummy_DAIRPORT'] = dummy_DAIRPORT_list

  flightsdata.to_csv('input_data_df.csv')

  target_flightsdata = flightsdata[['ARRIVAL_DELAY']]
  cont_flightsdata = flightsdata[['MONTH', 'DAY_OF_WEEK', 'dummy_AIRLINE', 'dummy_OGAIRPORT', 'dummy_DAIRPORT', 'DEPARTURE_TIME', 'SCHEDULED_DEPARTURE', 'DEPARTURE_DELAY', 'SCHEDULED_TIME', 'SCHEDULED_ARRIVAL']]
  x_train, x_test, y_train, y_test = train_test_split(cont_flightsdata, target_flightsdata, test_size=0.2, random_state=100)
  x_train.to_csv('output_data/output_train_x.csv' ,index=None)
  x_test.to_csv('output_data/output_test_x.csv' ,index=None)
  y_train.to_csv('output_data/output_train_y.csv' ,index=None)
  y_test.to_csv('output_data/output_test_y.csv',index=None)

flightsdata = pd.read_csv("input_data_df.csv")

#bivariate analysis
corrmatrix = flightsdata.corr()
sea.heatmap(corrmatrix, annot=True)
plt.savefig('Charts/FULL_correlation_heatmap.png')

#Univariate analysis
flightsdata.hist()
plt.savefig('Charts/FULL_flights_histogram.png')

#correlation bar chart
def imp_clean_corr_data():
    if os.path.isfile('Charts/correlation_matrix.csv') == False:
      corrmatrix = flightsdata.corr()
      sea.heatmap(correlation_matrix, annot=False)
      corrmatrix = corrmatrix.stack()
      corrmatrix = corrmatrix.reset_index()
      corrmatrix = corrmatrix.rename(columns={'level_0': 'feature_1', 'level_1': 'feature_2', '0': 'correlation'})
      corrmatrix.to_csv('correlation_matrix.csv')
    else:
      corrmatrix = pd.read_csv('Charts/correlation_matrix.csv')
      corrmatrix = corrmatrix.rename(columns={'level_0': 'feature_1', 'level_1': 'feature_2'})
      corrmatrix.sort_values(by=['correlation'], inplace=True, ascending=False)
    list_of_indexes = []
    for i in range(0,587):
      list_of_indexes.append(i)
    corrmatrix = corrmatrix.replace(to_replace=corrmatrix.index, value=list_of_indexes, inplace=False, limit=None, regex=False, method='pad')
    corrmatrix = corrmatrix.loc[corrmatrix['correlation'] != 1, :]
    corrmatrix = corrmatrix.loc[corrmatrix['correlation'] != 253.0, :]
    cleaned_correlation_matrix = None
    list_of_want_indexes = []
    for i in range(0,587,2):
      list_of_want_indexes.append(i)
    for index in list_of_want_indexes:
        temp_correlation_matrix = corrmatrix.loc[corrmatrix['index'] == index, :]
        cleaned_correlation_matrix = pd.concat([cleaned_correlation_matrix, temp_correlation_matrix], axis=0)
    cleaned_correlation_matrix.sort_values(by=['correlation'], inplace=True, ascending=False)
    return cleaned_correlation_matrix
def corr_bar_chart(file):
  corrmatrix = pd.read_csv(file)
  corrmatrix = corrmatrix.head(8)
  corrmatrix['feature_both'] = corrmatrix['feature_1'] + "\nand\n" + corrmatrix['feature_2']
  corrmatrix.drop(columns=['feature_1', 'feature_2', 'Unnamed: 0', 'index'])
  corrmatrix.plot(kind='barh', x='feature_both', y='correlation', figsize=(25,16), width=.6)
  plt.xlabel('Correlation (R^2)', fontsize=20)
  plt.ylabel('Combinations of Features from Dataset', fontsize=20)
  plt.yticks(fontsize=20)
  plt.xticks(fontsize=14)
  plt.savefig('Charts/flights_correlation_bar_chart.png')

corrmatrix = imp_clean_corr_data()
corrmatrix.to_csv('Charts/cleaned_airplane_correlation_table.csv')
corr_bar_chart('Charts/cleaned_airplane_correlation_table.csv')










