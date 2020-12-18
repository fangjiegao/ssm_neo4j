# coding=utf-8
from .import neo4j_mining_Edge
import collections
from .import project_dfs
from .import neo4j_mining_tool


def get_forward_root_edges(graph, start_node):
    """
        Args:
            graph: pyneo4j graph.
            start_node: source vertex id.
    """
    result = []
    start_label = neo4j_mining_tool.get_labels_by_id(graph, start_node)
    id_labels = neo4j_mining_tool.get_1D_node_by_startnode_id(graph, start_node)
    for end_node, end_label, relation_name in id_labels:
        if start_label <= end_label:
            result.append(
                (neo4j_mining_Edge.Neo4jMiningEdge(start_node, end_node, relation_name, start_label, end_label),
                 start_label, end_label, relation_name)
            )
    return result


def init_all_root(graph):
    """
        Args:
            graph: pyneo4j graph.
    """
    root = collections.defaultdict(list)

    for node_id_list in neo4j_mining_tool.node_id_generator(graph):
        for node_id in node_id_list:
            edges_tuple = get_forward_root_edges(graph, node_id)
            for edge_tuple in edges_tuple:
                root[(edge_tuple[1], edge_tuple[3], edge_tuple[2])].append(project_dfs.PDFS(edge_tuple[0], None))
    return root


def init_all_root_generator(graph):
    """
        Args:
            graph: pyneo4j graph.
    """
    all_labels = neo4j_mining_tool.get_all_lables(graph)
    all_relation = neo4j_mining_tool.get_all_relations(graph)
    for start_label in all_labels:
        for end_label in all_labels:
            for relation in all_relation:
                if start_label <= end_label:
                    hrt = neo4j_mining_tool.get_data_by_hrt_lable(graph, start_label, relation, end_label)
                    if len(hrt) != 0:
                        yield {(start_label, relation, end_label):
                               [project_dfs.PDFS(
                                   # frm, to, elb, frmlb, tolb
                                   neo4j_mining_Edge.Neo4jMiningEdge(_[0], _[2], _[1], start_label, end_label),
                                   None) for _ in hrt]}
                else:
                    pass
    print("all node Done......", all_labels, all_relation)


def get_backward_edge(dfscode, e1, e2, history):
    """
        Args:
            dfscode: DFScode
            e1: neo4j_mining_Edge.Neo4jMiningEdge.
            e2: neo4j_mining_Edge.Neo4jMiningEdge.
            history: neo4j_mining_History.Neo4jMiningHistory
    """
    if e1 == e2:
        return None
    from_e2_list = dfscode.get_1D_node_by_startnode_id_2_Neo4jMiningEdge(e2.to)
    for from_e2_edge in from_e2_list:
        if history.has_edge(from_e2_edge.eid) or from_e2_edge.to != e1.frm:
            continue

        if e1.elb < from_e2_edge.elb or (
                e1.elb == from_e2_edge.elb and e1.tolb <= e2.tolb):
            return from_e2_edge

    return None


def get_neo4j_backward_edge(graph, e1, e2, history):
    """
        Args:
            graph: neo4j graph
            e1: neo4j_mining_Edge.Neo4jMiningEdge.
            e2: neo4j_mining_Edge.Neo4jMiningEdge.
            history: neo4j_mining_History.Neo4jMiningHistory
    """
    if e1 == e2:
        return None
    from_e2_list = neo4j_mining_tool.get_1D_node_by_startnode_id_2_Neo4jMiningEdge(graph, e2.to)
    for from_e2_edge in from_e2_list:
        if history.has_edge(from_e2_edge.eid) or from_e2_edge.to != e1.frm:
            continue

        if e1.elb < from_e2_edge.elb or (
                e1.elb == from_e2_edge.elb and e1.tolb <= e2.tolb):
            return from_e2_edge

    return None


def get_neo4j_forward_pure_edges(graph, rm_edge, min_vlb, history):
    """
        Args:
            graph: neo4j graph
            rm_edge: neo4j_mining_Edge.Neo4jMiningEdge(start edge).
            min_vlb: min_vlb
            history: neo4j_mining_History.Neo4jMiningHistory
    """
    result = []
    from_rm_edge_list = neo4j_mining_tool.get_1D_node_by_startnode_id_2_Neo4jMiningEdge(graph, rm_edge.to)
    for from_rm_edge in from_rm_edge_list:
        # difference with get_forward_root_edges is history.has_vertex
        if min_vlb <= from_rm_edge.tolb and not history.has_vertex(from_rm_edge.to):
            result.append(from_rm_edge)

    return result


def get_forward_pure_edges(dfscode, rm_edge, min_vlb, history):
    """
        Args:
            dfscode: DFScode
            rm_edge: neo4j_mining_Edge.Neo4jMiningEdge(start edge).
            min_vlb: min_vlb
            history: neo4j_mining_History.Neo4jMiningHistory
    """
    result = []
    from_rm_edge_list = dfscode.get_1D_node_by_startnode_id_2_Neo4jMiningEdge(rm_edge.to)
    for from_rm_edge in from_rm_edge_list:
        # difference with get_forward_root_edges is history.has_vertex
        if min_vlb <= from_rm_edge.tolb and not history.has_vertex(from_rm_edge.to):
            result.append(from_rm_edge)

    return result


def get_forward_rmpath_edges(dfscode, rm_edge, min_vlb, history):
    """
        Args:
            dfscode: DFScode
            rm_edge: neo4j_mining_Edge.Neo4jMiningEdge(start edge).
            min_vlb: min_vlb
            history: neo4j_mining_History.Neo4jMiningHistory
    """
    result = []
    to_vlb = rm_edge.tolb
    # print(rm_edge.tolb, rm_edge)
    from_rm_edge_list = dfscode.get_1D_node_by_startnode_id_2_Neo4jMiningEdge(rm_edge.frm)
    for from_rm_edge in from_rm_edge_list:
        new_to_vlb = from_rm_edge.tolb
        # print(new_to_vlb, from_rm_edge)
        if rm_edge.to == from_rm_edge.to or min_vlb > new_to_vlb or history.has_vertex(from_rm_edge.to):
            continue
        if rm_edge.elb < from_rm_edge.elb or (rm_edge.elb == from_rm_edge.elb and to_vlb <= new_to_vlb):
            result.append(from_rm_edge)

    return result


def get_neo4j_forward_rmpath_edges(graph, rm_edge, min_vlb, history):
    """
        Args:
            graph: neo4j graph
            rm_edge: neo4j_mining_Edge.Neo4jMiningEdge(start edge).
            min_vlb: min_vlb
            history: neo4j_mining_History.Neo4jMiningHistory
    """
    result = []
    to_vlb = rm_edge.tolb
    from_rm_edge_list = neo4j_mining_tool.get_1D_node_by_startnode_id_2_Neo4jMiningEdge(graph, rm_edge.frm)
    for from_rm_edge in from_rm_edge_list:
        new_to_vlb = from_rm_edge.tolb
        if rm_edge.to == from_rm_edge.to or min_vlb > new_to_vlb or history.has_vertex(from_rm_edge.to):
            continue
        if rm_edge.elb < from_rm_edge.elb or (rm_edge.elb == from_rm_edge.elb and to_vlb <= new_to_vlb):
            result.append(from_rm_edge)

    return result