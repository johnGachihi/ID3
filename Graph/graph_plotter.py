import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt


class TreePlotter:
    def __init__(self, decision_tree=None):
        if decision_tree is None:
            decision_tree = dict()

        self.decision_tree = decision_tree
        self.G = nx.DiGraph()
        self.node_counter = 1

    def plot(self):
        self.plot_tree(self.decision_tree)

        pos = graphviz_layout(self.G, prog='dot')
        nx.draw(self.G, pos, with_labels=True, arrows=True, )
        nx.draw_networkx_edge_labels(
            self.G,
            pos=pos,
            edge_labels=nx.get_edge_attributes(self.G, 'label')
        )
        plt.show()

    def plot_tree(self, tree, parent_node="", edge=""):
        root = next(iter(tree))
        root_unique = str(self.node_counter) + '. ' + root

        if parent_node:
            self.G.add_edge(parent_node, root_unique, label=edge)

        for edge, node in tree[root].items():
            if isinstance(node, dict):
                self.node_counter += 1
                self.plot_tree(node, root_unique, edge)
            else:
                self.node_counter += 1
                self.G.add_edge(
                    root_unique,
                    str(self.node_counter) + '. ' + node,
                    label=edge
                )