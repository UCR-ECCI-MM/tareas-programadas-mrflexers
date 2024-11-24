import networkx as nx

from src.experiment.graph import CostReliabilityGraph

class CostReliabilityNetwork(CostReliabilityGraph):

    def __init__(self):
        super().__init__()

    @property
    def is_feasible(self):
        return self.is_connected and self.is_reliable

    @property
    def is_connected(self):
        if len(self.nodes) == 0:
            return False
        return nx.is_connected(self._graph)

    @property
    def is_reliable(self):
        if len(self.nodes) == 0:
            return False
        return all(self._graph.nodes[node].get('reliability_sum', 0) >= 1 for node in self._graph.nodes())
