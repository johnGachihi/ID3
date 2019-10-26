from math import log2
import pandas

class ID3:

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
    def input_attribute_entropy(input_attribute, output_attribute, data):
        """

        :param input_attribute: Name of input attribute
        :type input_attribute: str
        :param output_attribute: Name of output attribute
        :type output_attribute: str
        :param data: DataFrame containing columns for the input and output attributes
        :type data: pandas.core.frame.DataFrame
        """

        row_count = len(data.index)

        entropy = 0

        for group_name, group in data.groupby([input_attribute]):
            group_size = len(group.index)
            entropy_acc = 0

            for subgroup_name, subgroup in group.groupby([output_attribute]):
                probability = len(subgroup.index) / group_size
                entropy_acc -= probability * log2(probability)

            entropy_acc *= group_size / row_count
            entropy += entropy_acc

        return entropy

    @classmethod
    def information_gain(cls, in_attr, out_attr, data):
        return cls.entropy(data[out_attr]) - cls.input_attribute_entropy(in_attr, out_attr, data)