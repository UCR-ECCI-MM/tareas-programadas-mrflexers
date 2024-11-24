import pytest
from experiment.network import CostReliabilityNetwork

@pytest.fixture
def empty_network():
    return CostReliabilityNetwork()

@pytest.fixture
def network_with_nodes():
    network = CostReliabilityNetwork()
    network.add_nodes([0, 1, 2])
    return network

@pytest.fixture
def network_with_edges(network_with_nodes):
    network = network_with_nodes
    network.add_edge((0, 1, {'cost': 5, 'reliability': 0.6}))
    network.add_edge((1, 2, {'cost': 3, 'reliability': 0.5}))
    return network

# Test Initialization
def test_network_initial_total_cost(empty_network):
    assert empty_network.total_cost == 0

def test_network_initial_nodes_empty(empty_network):
    assert len(empty_network.nodes) == 0

def test_network_initial_edges_empty(empty_network):
    assert len(empty_network.edges) == 0

def test_network_initial_not_feasible(empty_network):
    assert not empty_network.is_feasible

def test_network_initial_not_connected(empty_network):
    assert not empty_network.is_connected

def test_network_initial_not_reliable(empty_network):
    assert not empty_network.is_reliable

# Test Adding Nodes
def test_add_nodes_length(network_with_nodes):
    assert len(network_with_nodes.nodes) == 3

def test_add_nodes_reliability_sum_zero(network_with_nodes):
    for node in [0, 1, 2]:
        assert network_with_nodes.get_node_reliability(node) == 0

# Test Adding Edge
@pytest.fixture
def network_with_single_edge(network_with_nodes):
    network = network_with_nodes
    network.add_edge((0, 1, {'cost': 5, 'reliability': 0.6}))
    return network

def test_add_edge_total_cost(network_with_single_edge):
    assert network_with_single_edge.total_cost == 5

def test_add_edge_exists(network_with_single_edge):
    assert network_with_single_edge.has_edge(0, 1)

def test_add_edge_node0_reliability(network_with_single_edge):
    assert network_with_single_edge.get_node_reliability(0) == 0.6

def test_add_edge_node1_reliability(network_with_single_edge):
    assert network_with_single_edge.get_node_reliability(1) == 0.6

# Test Connectivity
def test_network_not_connected_with_single_edge(network_with_single_edge):
    assert not network_with_single_edge.is_connected

def test_network_connected(network_with_edges):
    assert network_with_edges.is_connected

# Test Reliability
def test_network_not_reliable_with_single_edge(network_with_single_edge):
    assert not network_with_single_edge.is_reliable

def test_node0_reliability_with_edges(network_with_edges):
    assert network_with_edges.get_node_reliability(0) == 0.6

def test_node1_reliability_with_edges(network_with_edges):
    assert network_with_edges.get_node_reliability(1) == 1.1

def test_node2_reliability_with_edges(network_with_edges):
    assert network_with_edges.get_node_reliability(2) == 0.5

def test_network_not_reliable_with_edges(network_with_edges):
    assert not network_with_edges.is_reliable

# Test Adding Edge to Meet Reliability
@pytest.fixture
def network_made_reliable(network_with_edges):
    network = network_with_edges
    network.add_edge((0, 2, {'cost': 2, 'reliability': 0.5}))
    return network

def test_node0_reliability_after_adding_edge(network_made_reliable):
    assert network_made_reliable.get_node_reliability(0) == 1.1

def test_node2_reliability_after_adding_edge(network_made_reliable):
    assert network_made_reliable.get_node_reliability(2) == 1.0

def test_network_reliable_after_adding_edge(network_made_reliable):
    assert network_made_reliable.is_reliable

# Test Feasibility
def test_network_not_feasible_before_reliability(network_with_edges):
    assert not network_with_edges.is_feasible

def test_network_feasible_after_reliability(network_made_reliable):
    assert network_made_reliable.is_feasible

# Test Removing Edge
@pytest.fixture
def network_after_edge_removal(network_with_single_edge):
    network = network_with_single_edge
    network.remove_edge(0, 1)
    return network

def test_total_cost_after_removal(network_after_edge_removal):
    assert network_after_edge_removal.total_cost == 0

def test_edge_removed(network_after_edge_removal):
    assert not network_after_edge_removal.has_edge(0, 1)

def test_node0_reliability_after_removal(network_after_edge_removal):
    assert network_after_edge_removal.get_node_reliability(0) == 0

def test_node1_reliability_after_removal(network_after_edge_removal):
    assert network_after_edge_removal.get_node_reliability(1) == 0

# Test Adding Multiple Edges
def test_add_edges_length(network_with_edges):
    assert len(network_with_edges.edges) == 2

def test_add_edges_total_cost(network_with_edges):
    assert network_with_edges.total_cost == 8

def test_node0_reliability_with_added_edges(network_with_edges):
    assert network_with_edges.get_node_reliability(0) == 0.6

def test_node1_reliability_with_added_edges(network_with_edges):
    assert network_with_edges.get_node_reliability(1) == 1.1

def test_node2_reliability_with_added_edges(network_with_edges):
    assert network_with_edges.get_node_reliability(2) == 0.5

# Test Feasibility with Insufficient Reliability
@pytest.fixture
def network_insufficient_reliability(network_with_nodes):
    network = network_with_nodes
    network.add_edge((0, 1, {'cost': 5, 'reliability': 0.4}))
    network.add_edge((1, 2, {'cost': 3, 'reliability': 0.4}))
    return network

def test_network_connected_insufficient_reliability(network_insufficient_reliability):
    assert network_insufficient_reliability.is_connected

def test_network_not_reliable_insufficient_reliability(network_insufficient_reliability):
    assert not network_insufficient_reliability.is_reliable

def test_network_not_feasible_insufficient_reliability(network_insufficient_reliability):
    assert not network_insufficient_reliability.is_feasible

# Test Improving Reliability
@pytest.fixture
def network_reliability_improved(network_insufficient_reliability):
    network = network_insufficient_reliability
    # Increase reliability for nodes 0 and 2
    network.add_edge((0, 2, {'cost': 2, 'reliability': 0.6}))
    return network

def test_node0_reliability_improved(network_reliability_improved):
    assert network_reliability_improved.get_node_reliability(0) == 1.0  # 0.4 + 0.6

def test_node2_reliability_improved(network_reliability_improved):
    assert network_reliability_improved.get_node_reliability(2) == 1.0  # 0.4 + 0.6

def test_node1_reliability_still_insufficient(network_reliability_improved):
    assert network_reliability_improved.get_node_reliability(1) == 0.8  # 0.4 + 0.4

def test_network_not_reliable_yet(network_reliability_improved):
    assert not network_reliability_improved.is_reliable

# Test Finalizing Reliability
@pytest.fixture
def network_finally_reliable(network_reliability_improved):
    network = network_reliability_improved
    # Increase reliability for node 1
    network.add_edge((1, 2, {'cost': 1, 'reliability': 0.2}))
    return network

def test_node1_reliability_final(network_finally_reliable):
    assert network_finally_reliable.get_node_reliability(1) == 1.0  # 0.8 + 0.2

def test_node2_reliability_final(network_finally_reliable):
    assert network_finally_reliable.get_node_reliability(2) == 1.2  # 1.0 + 0.2

def test_network_finally_reliable(network_finally_reliable):
    assert network_finally_reliable.is_reliable

def test_network_finally_feasible(network_finally_reliable):
    assert network_finally_reliable.is_feasible
