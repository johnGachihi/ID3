# @uthor Edmond Menya
# ID3 Algorithm Illustration for Decision Trees
import math
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import networkx as nx
import matplotlib.pyplot as plt
import operator
from ID3.id3 import ID3


def entropy(attr_name):
    entropy = 0
    row_del_dict = dict()
    inner_row_del_dict = dict()
    # getting column contents of current attribute name from data extracted from csv file
    attr_list = list(data[attr_name])
    if attr_name == 'fast':
        class_attr_list = set(attr_list)  # get number of unique classes in attribute
        all_classes = list(class_attr_list)  # convert back to list
        # print(all_classes)
        for x in all_classes:
            probability = attr_list.count(x) / len(attr_list)
            entropy -= (probability * math.log2(probability))
            # print(len(attr_list))
    else:
        merged_class = list(zip(attr_list, list(data['fast'])))
        # entropy=0
        class_attr_list = set(merged_class)  # get number of unique classes in attribute
        all_classes = list(class_attr_list)  # convert back to list
        # uniq_list=unique_attr_clases(attr_list)
        print('all_classes', all_classes)
        for x in all_classes:
            probability = merged_class.count(x) / attr_list.count(x[0])
            # print(attr_list.count(x[0]),len(attr_list),probability,math.log2(probability))
            # entropy of child combinations
            sub_entropy = probability * math.log2(probability)
            # dictionary to determine rows to be deleted in table reduction
            inner_row_del_dict[x[0]] = sub_entropy
            row_del_dict[attr_name] = inner_row_del_dict
            entropy -= (attr_list.count(x[0]) / len(attr_list)) * (sub_entropy)
        print('row del dict', row_del_dict)
    # print("Target Attribute Entropy: ",entropy, "\n")
    return entropy, row_del_dict


def information_gain(target_entopy, attr_entopy):
    info_gain = target_entopy - attr_entopy
    return info_gain


def root_node_election(target_entopy):
    rst_dict = dict()
    for x in data_headers[:-1]:  # calculate entopies of all minus the target
        # print("Entropy of ",x," is ",entropy(x))
        attr_entopy, attr_row_del_dict = entropy(x)
        info_gain = information_gain(target_entopy, attr_entopy)
        print("IG of ", x, " is ", info_gain)
        # store results in a dictionary
        rst_dict[x] = info_gain
    return max(rst_dict.items(), key=operator.itemgetter(1))[0], attr_row_del_dict


# tree construction using networkx
# def construct_decision_tree():

# training data table reduction for next iteration
def reduce_training_dataset(data, delete_rows, selected_root_node):
    for item in delete_rows:
        data = data[data.eval(selected_root_node) != item]
    # print(data)
    data = data.drop(selected_root_node, axis=1)
    # print(data.head(0))
    # data_headers.remove(selected_root_node) #delete header of choosen root node
    return data


# code loads from here
# using pandas to read csv file containing training dataset
data_headers = ['engine', 'turbo', 'weight', 'fueleco', 'fast']
data = pd.read_csv("id3_data.csv", names=data_headers, header=None)

############################################################
a = [1,2,3,4,5]
print(a[:len(a)-1])

# attr, count = data['fast'].value_counts()[0]
# print(data['fast'].value_counts().idxmax())
id_3 = ID3(data_headers[:len(data_headers)-1], 'fast')
# id_3.id3(data_headers[:len(data_headers)-1], 'fast', data)
print(id_3.generate_decision_tree(data))
# print(ID3.information_gain('fueleco', 'fast', data[['fueleco', 'fast']]))
print('\n\n\n')

############################################################
#2516291673878229
#251629167388
for group_name, group in data.groupby(['engine']):
    print(group_name)
data2 = data.groupby(['fueleco', 'fast'])
print(data['fast'].unique().size)
# if data['fast'].unique()


print(data.groupby(['fueleco', 'fast']).get_group(('average', 'no')))


gb = data[['fueleco', 'fast']].groupby(['fueleco'])
groups = [gb.get_group(x) for x in gb.groups]

# for group_name, group in data[['fueleco', 'fast']].groupby(['fueleco']):
#     print(len(group.index))
#     for subgroup_name, subgroup in group.groupby(['fast']):
#         print(subgroup_name, len(subgroup.index))
#         print(subgroup.drop(['fast'], axis=1))
# print('data', data)
# print(entropy(list(data['fast'])))
##############################################################################

target_entopy, attr_row_del_dict = entropy('fast')
print("Entropy of fast is: ", target_entopy)
selected_root_node, delete_rows = root_node_election(target_entopy)
print("Smaller entopies of root node are: ", delete_rows)
delete_row = []
for row, value in delete_rows[selected_root_node].items():
    if value == 1 or value == 0:  # arrest values with extreem entopies
        delete_row.append(row)  # store them in a list

print("The selected root node is: ", selected_root_node)
print("The rows to be deleted are: ", delete_row)
data = reduce_training_dataset(data, delete_row, selected_root_node)
print("New data set for next iteration is: \n", data)

