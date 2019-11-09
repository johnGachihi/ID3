NODE = 0
EDGE = 1


class DecisionTree:
    def __init__(self, tree=None):
        if tree is None:
            tree = dict()

        self.tree = tree

    def get_tree(self):
        return self.tree

    def add_to_tree(self, path, node, node_is_attr=False):
        if not path:
            self.tree[node] = dict()
            return

        tree = self.__get_subtree(self.tree, path)

        if node_is_attr:
            tree[path[-1][EDGE]] = {node: dict()}
        else:
            tree[path[-1][EDGE]] = node

    @classmethod
    def __get_subtree(cls, tree, ancestors):
        for attr, val in ancestors[:-1]:
            tree = tree[attr]
            tree = tree[val]

        tree = tree[ancestors[-1][0]]

        return tree