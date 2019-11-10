NODE = 0
EDGE = 1


class DecisionTree:
    def __init__(self, tree=None):
        if tree is None:
            tree = dict()
        self.__tree = tree

    def get_tree(self):
        return self.__tree

    def add_to_tree(self, path, node, node_is_tree_root=False):
        if not path:
            self.__tree[node] = dict()
            return

        tree = self.__get_subtree(self.__tree, path)

        if node_is_tree_root:
            tree[path[-1][EDGE]] = {node: dict()}
        else:
            tree[path[-1][EDGE]] = node

    @classmethod
    def __get_subtree(cls, tree, path):
        for attr, val in path[:-1]:
            tree = tree[attr]
            tree = tree[val]

        tree = tree[path[-1][NODE]]

        return tree