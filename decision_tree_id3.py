import pandas as pd
from ID3.id3 import ID3
from sklearn.metrics import confusion_matrix
from Graph.graph_plotter import GraphPlotter


data_headers = ['engine', 'turbo', 'weight', 'fueleco', 'fast']
data = pd.read_csv("id3_data.csv", names=data_headers, header=None)

id_3 = ID3(data_headers[:-1], data_headers[-1])
decision_tree = id_3.generate_decision_tree(data)

test_data = pd.read_csv("test_data.csv", names=data_headers, header=None)
id3_classifications = id_3.classify(test_data)

print(confusion_matrix(test_data['fast'].to_list(), id3_classifications))

print('Gold standard', test_data['fast'].to_list())
print('System labels', id3_classifications)

print('\n\n\n')
gp = GraphPlotter(decision_tree)
gp.plot()