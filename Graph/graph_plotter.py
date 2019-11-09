import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
from random import random


class GraphPlotter:
    def __init__(self, decision_tree=None):
        if decision_tree is None:
            decision_tree = dict()

        self.decision_tree = decision_tree
        self.G = nx.DiGraph()
        self.node_counter = 0

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

    def plot_tree(self, tree, level=0):
        root = next(iter(tree))

        for edge, node in tree[root].items():
            if isinstance(node, dict):
                # print(node)
                self.G.add_edge(
                    root+str(level),
                    (next(iter(node)))+str(level+1),
                    label=edge
                )
                self.plot_tree(node, level+1)
            else:
                self.G.add_edge(root+str(level), node+str(level+1), label=edge)
                print(root+str(level), node+str(level+1), edge)


