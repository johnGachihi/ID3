from math import log2

class ID3:

    @staticmethod
    def output_attribute_entropy(self, data):
        """
        :param self:
        :param data: Output attribute column data
        :type data: pandas.core.series.Series
        :return:
        """
        row_count = data.count()
        entropy = 0

        for value, value_count in data.value_counts().items():
            probability = value_count/row_count
            entropy -= probability * log2(probability)

        return entropy

    def input_attribute_entropy(self, input_attribute_data, output_attribute_data):
        """

        :param input_attribute_data:
        :type input_attribute_data: pandas.core.series.Series
        :param output_attribute_data:
        :type output_attribute_data: pandas.core.series.Series
        """

