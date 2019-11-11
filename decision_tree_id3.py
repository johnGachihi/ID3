import pandas as pd
from ID3.id3 import ID3
from sklearn.metrics import confusion_matrix
from Graph.tree_plotter import TreePlotter

"""Read Training Data"""
data_headers = ['engine', 'turbo', 'weight', 'fueleco', 'fast']
data = pd.read_csv("id3_data.csv", names=data_headers, header=None)

"""Create ID3 class instance"""
id_3 = ID3(
    in_attr_list=data_headers[:-1],  # Input Attribute List
    out_attr=data_headers[-1]        # Output Attribute
)

"""Generate Decision Tree"""
decision_tree = id_3.generate_decision_tree(data)

"""Plot Decision Tree"""
tp = TreePlotter(decision_tree)
tp.plot()

"""Classify Test Data"""
test_data = pd.read_csv("test_data.csv", names=data_headers, header=None)
id3_classifications = id_3.classify(test_data)

"""Calculate Model Accuracy using the Confusion Matrix"""
print("\n\nConfusion Matrix:")
print(confusion_matrix(test_data['fast'].to_list(), id3_classifications))
