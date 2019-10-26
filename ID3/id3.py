from math import log2
import pandas
import networkx as nx
import matplotlib.pyplot as plt

class ID3:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.G = nx.Graph()

    @staticmethod
    def entropy(data):
        """

        :param data: Single row column data
        :type data: pandas.core.series.Series
        :return:
        """
        row_count = data.count()
        entropy = 0

        for value, value_count in data.value_counts().items():
            probability = value_count/row_count
            entropy -= probability * log2(probability)

        return entropy

    @staticmethod
    def in_attr_entropy(in_attr, out_attr, data):
        """
        Calculates entropy of @in_attr with relation to @out_attr
        :param in_attr: Name of input attribute
        :type in_attr: str
        :param out_attr: Name of output attribute
        :type out_attr: str
        :param data: DataFrame containing columns for the input and output attributes
        :type data: pandas.core.frame.DataFrame
        """

        row_count = len(data.index)

        entropy = 0

        for group_name, group in data.groupby([in_attr]):
            group_size = len(group.index)
            entropy_acc = 0

            for subgroup_name, subgroup in group.groupby([out_attr]):
                probability = len(subgroup.index) / group_size
                entropy_acc -= probability * log2(probability)

            entropy_acc *= group_size / row_count
            entropy += entropy_acc

        return entropy

    @classmethod
    def information_gain(cls, in_attr, out_attr, data):
        return cls.entropy(data[out_attr]) - cls.in_attr_entropy(in_attr, out_attr, data)

    def id3(self, in_attr_list: list, out_attr: str, data: pandas.DataFrame, prev_node=None):
        """
        :param in_attr_list: A list of input attributes
        :param out_attr: The output attribute
        :param data: A Dataframe containing all the data
        """

        if data.empty:
            self.y += 2
            self.__addnode(self.G, 'failed', self.x, self.y)

        if data[out_attr].unique().size == 1:
            value = data[out_attr].unique()[0]
            self.y += 2
            self.__addnode(self.G, value, self.x, self.y)

        if not in_attr_list:
            value = data[out_attr].value_counts().idxmax()
            self.y += 2
            self.__addnode(self.G, value, self.x, self.y)

        largest_ig_attr = self.__largest_ig_attr(in_attr_list, out_attr, data)
        self.y += 1
        self.__addnode(self.G, largest_ig_attr, self.x, self.y)
        if prev_node:
            self.G.add_edge(prev_node, largest_ig_attr, )


        nx.draw_networkx(
            self.G,
            nx.get_node_attributes(self.G, 'pos'),
            node_color='blue',
            node_size=450
        )
        plt.show()


    @classmethod
    def __largest_ig_attr(cls, in_attr_list, out_attr, data):
        highest_IG_attr = in_attr_list[0]
        highest_IG = cls.information_gain(highest_IG_attr, out_attr, data)

        for attr in in_attr_list[1:]:
            cur_IG = cls.information_gain(attr, out_attr, data)
            if highest_IG < cur_IG:
                highest_IG_attr = attr
                highest_IG = cur_IG

        return highest_IG_attr

    @staticmethod
    def __addnode(G, nodename, x, y):
        G.add_node(nodename)
        G.node[nodename]['pos'] = (x, y)
