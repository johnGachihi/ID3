from math import log2
import pandas


class ID3:

    def __init__(self, in_attr_list, out_attr, data):
        self.in_attr_list = in_attr_list
        self.out_attr = out_attr
        self.data = data

        self.tree = dict()

    def compute(self):
        self.id3(self.in_attr_list, self.data)
        return self.tree

    def id3(self, in_attr_list: list, data: pandas.DataFrame, grouping_value="", prev_node="", ancestors=[]):
        """
        :param in_attr_list: A list of input attributes
        :param data: A Dataframe containing all the data
        :param grouping_value: The value used to group the data
        :type grouping_value: str
        :param prev_node: The previous established node
        :type prev_node: str
        """
        print('tree', self.tree)

        if data.empty:
            self.__print_node(prev_node, 'Failed', grouping_value)
            # ...
            return

        if data[self.out_attr].unique().size == 1:
            node = data[self.out_attr].unique()[0]
            self.__print_node(ancestors, node, grouping_value)
            self.add_to_tree(self.tree, ancestors, node)
            return

        if not in_attr_list:
            node = data[self.out_attr].value_counts().idxmax()
            self.__print_node(ancestors, node, grouping_value)
            self.add_to_tree(self.tree, ancestors, node)
            return

        largest_ig_attr = self.__largest_ig_attr(in_attr_list, self.out_attr, data)
        self.add_to_tree(self.tree, ancestors, largest_ig_attr, True)
        self.__print_node(ancestors, largest_ig_attr, grouping_value)

        temp_in_attr_list = in_attr_list.copy()
        temp_in_attr_list.remove(largest_ig_attr)
        for grouping_value, group in data.groupby([largest_ig_attr]):
            self.id3(
                in_attr_list   = temp_in_attr_list,
                data           = group.drop([largest_ig_attr], axis=1),
                grouping_value = grouping_value,
                prev_node      = largest_ig_attr,
                ancestors      = ancestors + [(largest_ig_attr, grouping_value)]
            )

        return

    @classmethod
    def __largest_ig_attr(cls, in_attr_list, out_attr, data):
        """
        Gets the attribute, from among @in_attr_list, that has
        the greatest Information Gain.

        :param in_attr_list: List of input attributes
        :param out_attr: The output attribute
        :param data: A Dataframe with columns for all input
         attributes and the output attribute
        :return:
        """
        highest_ig_attr = in_attr_list[0]
        highest_ig = cls.information_gain(highest_ig_attr, out_attr, data)

        for attr in in_attr_list[1:]:
            cur_ig = cls.information_gain(attr, out_attr, data)
            if highest_ig < cur_ig:
                highest_ig_attr = attr
                highest_ig = cur_ig

        return highest_ig_attr

    @classmethod
    def information_gain(cls, in_attr, out_attr, data):
        return cls.entropy(data[out_attr]) - cls.in_attr_entropy(in_attr, out_attr, data)

    @staticmethod
    def entropy(data):
        """
        Calculate entropy. (Not relative entropy). Takes in
        a Series object with a single column.

        :param data: Single row column data
        :type data: pandas.core.series.Series
        :return:
        """
        row_count = data.count()
        entropy = 0

        for value, value_count in data.value_counts().items():
            probability = value_count / row_count
            entropy -= probability * log2(probability)

        return entropy

    @staticmethod
    def in_attr_entropy(in_attr, out_attr, data):
        """
        Calculates entropy of @in_attr in relation to @out_attr
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
    def add_to_tree(cls, tree, ancestors, node, node_is_attr=False):
        if not ancestors:
            tree[node] = dict()
            return

        tree = cls.get_subtree(tree, ancestors)

        if node_is_attr:
            tree[ancestors[-1][1]] = {node: dict()}
        else:
            tree[ancestors[-1][1]] = node

    @classmethod
    def get_subtree(cls, tree, ancestors):
        for attr, val in ancestors[:-1]:
            tree = tree[attr]
            tree = tree[val]

        tree = tree[ancestors[-1][0]]

        return tree

    @staticmethod
    def __print_node(prev_node, cur_node, edge_label):
        print('{} --{}-- {}'.format(prev_node, edge_label, cur_node))
