import networkx as nx
import numpy as np


class CostReliabilityGraph:

    @classmethod
    def generate_random_solvable_graph(cls, n, c_max=20, R_min=1.8):
        """
        Generates a fully connected graph with n nodes.
        Each edge has a "cost" (>0) and "reliability" (0 < reliability <= 1).
        Ensures that for each node, the sum of reliabilities of incident edges >= R_min.
        """
        # Start with a complete graph to ensure full connectivity
        G = nx.complete_graph(n)

        # Initialize dictionaries to hold reliability assignments
        node_edge_reliabilities = {node: {} for node in G.nodes()}

        # Step 1: Assign costs randomly
        for (u, v) in G.edges():
            G[u][v]["cost"] = np.random.randint(1, c_max)  # Cost > 0

        # Step 2: Assign reliabilities using Dirichlet distribution
        for node in G.nodes():
            neighbors = list(G.neighbors(node))
            degree = len(neighbors)
            if degree == 0:
                continue  # Isolated node, skip

            # Use Dirichlet distribution to generate reliabilities summing to R_min
            # Adjust alpha parameter to control variability
            # alpha = np.random.uniform(0.5, 1.5, degree)
            alpha = np.ones(degree)
            reliabilities = np.random.dirichlet(alpha) * R_min

            # Assign reliabilities to edges incident to this node
            for neighbor, reliability in zip(neighbors, reliabilities):
                node_edge_reliabilities[node][neighbor] = reliability

        # Step 3: Compute average reliabilities for each edge
        for (u, v) in G.edges():
            # Get reliabilities assigned from both ends
            r_uv = node_edge_reliabilities[u].get(v, 0)
            r_vu = node_edge_reliabilities[v].get(u, 0)

            # Compute average reliability
            r_avg = (r_uv + r_vu) / 2

            # Ensure reliability is within (0, 1]
            r_avg = min(max(r_avg, 0.01), 1.0)  # Set a minimum to avoid zero reliability

            G[u][v]["reliability"] = r_avg

        # Step 4: Verify that the sum of reliabilities at each node is >= R_min
        for node in G.nodes():
            total_reliability = sum(G[node][neighbor]["reliability"] for neighbor in G.neighbors(node))
            if total_reliability < R_min:
                # Adjust reliabilities proportionally to meet R_min
                scaling_factor = R_min / total_reliability
                for neighbor in G.neighbors(node):
                    G[node][neighbor]["reliability"] *= scaling_factor
                    # Ensure reliability does not exceed 1
                    G[node][neighbor]["reliability"] = min(G[node][neighbor]["reliability"], 1.0)

        # Step 5: Update the reliability sum for each node
        for node in G.nodes():
            total_reliability = sum(G[node][neighbor]["reliability"] for neighbor in G.neighbors(node))
            G.nodes[node]["reliability_sum"] = total_reliability

        cost_reliability_graph = cls()
        cost_reliability_graph._graph = G

        return cost_reliability_graph

    def __init__(self):
        self._graph = nx.Graph()

    @property
    def nodes(self):
        return list(self._graph.nodes(data=True))

    @property
    def edges(self):
        return list(self._graph.edges(data=True))

    def has_edge(self, u, v):
        return self._graph.has_edge(u, v)

    def get_node_reliability(self, node):
        return self._graph.nodes[node]['reliability_sum']

    def add_nodes(self, nodes):
        for node in nodes:
            node['reliability_sum'] = 0
        self._graph.add_nodes_from(nodes)

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge)

    def add_edge(self, edge):
        u, v, data = edge
        cost = data['cost']
        reliability = data['reliability']
        self._graph.add_edge(u, v, cost=cost, reliability=reliability)
        self._graph.nodes[u]['reliability_sum'] += reliability
        self._graph.nodes[v]['reliability_sum'] += reliability

    def remove_edge(self, u, v):
        if self._graph.has_edge(u, v):
            data = self._graph[u][v]
            self._graph.nodes[u]['reliability_sum'] -= data['reliability']
            self._graph.nodes[v]['reliability_sum'] -= data['reliability']
            self._graph.remove_edge(u, v)

    def draw(self):
        pos = nx.spring_layout(self._graph)

        nx.draw(self._graph, pos, with_labels=False, node_color='skyblue', edge_color='gray', node_size=2000,
                font_size=15)

        node_labels = {
            node: f"{node}\n{self._graph.nodes[node]["reliability_sum"]:.2f}"  # Format to 2 decimal places
            for node in self._graph.nodes()
        }
        nx.draw_networkx_labels(self._graph, pos, labels=node_labels, font_size=12, font_color="black")

        edge_labels = {
            (
            u, v): f"c = {self._graph.edges[u, v]["cost"]}, r = {self._graph.edges[u, v]["reliability"]:.2f}"
            # Format to 2 decimal places
            for u, v in self._graph.edges()
        }
        nx.draw_networkx_edge_labels(self._graph, pos, edge_labels=edge_labels, font_size=10)
