# coding=utf-8
from .import cql_string
from py2neo import Graph, RelationshipMatcher, NodeMatcher
from .neo4j_mining_Edge import Neo4jMiningEdge


BATCH_SIZE = 10000


def get_neo4j_connect(ip, username, password):
    return Graph(ip, username=username, password=password)


def get_relation_matcher(graph):
    relation_matcher = RelationshipMatcher(graph)
    node_selector = NodeMatcher(graph)
    return relation_matcher, node_selector


def run_cql(graph, cql):
    cypher = graph.run
    return cypher(cql)


def get_all_lables(graph):
    label_name = run_cql(graph, cql_string.get_all_lable)
    # return [list(_.values())[0] for _ in res.data()]
    return [_["label"] for _ in label_name.data()]


def get_all_relations(graph):
    relation_name = run_cql(graph, cql_string.get_all_relations)
    # return [list(_.values())[0] for _ in res.data()]
    return [_["relation"] for _ in relation_name.data()]


def get_lable_num(graph):
    lables = get_all_lables(graph)
    lables_sql = [cql_string.get_lable_count % (_, "num") for _ in lables]
    print(lables_sql)
    nums = [run_cql(graph, _).data()[0]["num"] for _ in lables_sql]
    return dict(zip(lables, nums))


def get_relation_num(graph):
    relations = get_all_relations(graph)
    relations_sql = [cql_string.get_all_relation_count % (_, "num") for _ in relations]
    print(relations_sql)
    nums = [run_cql(graph, _).data()[0]["num"] for _ in relations_sql]
    return dict(zip(relations, nums))


def get_all_1_degree_shape(graph):
    shape = run_cql(graph, cql_string.get_all_1_hrt_shape)
    # print(shape.data())
    # for _ in shape.data():
    #     print(_["h_label"][0], _["r_label"], _["t_label"][0])
    return [(_["h_label"][0], _["r_label"], _["t_label"][0]) for _ in shape.data()]


def get_1_degree_shape_count(graph):
    h_r_t = get_all_1_degree_shape(graph)
    print(h_r_t)
    h_r_t_count_sql = [cql_string.get_all_1_hrt_shape_count % (_[0], _[1], _[2], "num") for _ in h_r_t]
    print(h_r_t_count_sql)
    nums = [run_cql(graph, _).data()[0]["num"] for _ in h_r_t_count_sql]
    return dict(zip(h_r_t, nums))


def match_by_hrt_lable(graph, hrt_lable, num):
    return match_by_hrt_lable_(graph, hrt_lable[0], hrt_lable[1], hrt_lable[2], num)


def match_by_hrt_lable_(graph, h_lable, r_lable, t_lable, num):
    batchsize = BATCH_SIZE
    batch = 0
    res_list = []
    while batch < num:
        batchcql = cql_string.match_data_by_hrt_lable % (h_lable, r_lable, t_lable, batch, batchsize)
        batch = batch + batchsize
        print(batchcql)
        relation = run_cql(graph, batchcql)
        res_list = res_list + relation.data()
    return res_list


def hrt_lable_generator(graph, h_lable, r_lable, t_lable, num):
    batchsize = 1
    batch = 0
    while batch < num:
        batchcql = cql_string.match_data_by_hrt_lable % (h_lable, r_lable, t_lable, batch, batchsize)
        batch = batch + batchsize
        print(batchcql)
        relation = run_cql(graph, batchcql).data()[0]
        yield relation["h"], relation["r"], relation["t"]
    """
    batchcql = cql_string.match_data_by_hrt_lable_no_batch % (h_lable, r_lable, t_lable)
    relation = run_cql(graph, batchcql)
    print(type(relation))
    while True:
        try:
            s = next(relation)
            print(s["h"], s["r"], s["t"])
        except StopIteration:
            print("StopIteration....")
            return
    """


def get_labels_by_id(graph, node_id):
    label_cql = cql_string.get_nodelable_by_id % node_id
    label = run_cql(graph, label_cql).data()[0]["label"][0]
    return label


def get_relation_by_hid_tid(graph, h_node_id, t_node_id):
    relation_cql = cql_string.get_relation_by_hid_tid % (h_node_id, t_node_id)
    print(relation_cql)
    relation = run_cql(graph, relation_cql)
    relation = relation.data()
    if len(relation) != 0:
        relation = relation[0]["relation"]
        return relation
    else:
        return None


def get_all_node_id(graph):
    id_cql = cql_string.get_all_node_id
    id_s = run_cql(graph, id_cql)
    id_s = id_s.data()
    if len(id_s) != 0:
        id_s = [_["node_id"] for _ in id_s]
        return id_s
    else:
        return None


def node_id_generator(graph):
    node_count = get_all_node_count(graph)
    batchsize = BATCH_SIZE
    batch = 0
    while batch < node_count:
        batch_nodeid_cql = cql_string.get_all_node_id_batch % (batch, batchsize)
        batch = batch + batchsize
        print(batch_nodeid_cql)
        node_ids = run_cql(graph, batch_nodeid_cql)
        node_ids = [_["node_id"] for _ in node_ids]
        yield node_ids
    print("all node Done......", node_count, node_count)


def get_all_node_count(graph):
    count_cql = cql_string.get_all_node_count
    count = run_cql(graph, count_cql)
    count = count.data()
    print(count)
    return count[0]["node_count"]


def node_generator(graph):
    count = len(graph.nodes)
    node_index = 0
    all_graph_nodes = 0
    # MATCH (n) WHERE id(n)=215 RETURN n;
    while all_graph_nodes < count:
        temp_node = graph.nodes.get(node_index)
        if temp_node is not None:
            yield temp_node
            all_graph_nodes += 1
        node_index += 1
    print("all node Done......", count, all_graph_nodes)


def get_1D_node_by_startnode_id(graph, node_id):
    id_labels_cql = cql_string.get_1D_node_by_startnode_id_and_relationname % node_id
    id_labels = run_cql(graph, id_labels_cql)
    id_labels = id_labels.data()
    id_labels = [(_["node_id"], _["node_label"][0], _["relation_name"]) for _ in id_labels]
    print(id_labels)
    return id_labels


def get_1D_node_by_startnode_id_2_Neo4jMiningEdge(graph, node_id):
    start_lable = get_labels_by_id(graph, node_id)
    # [(16213, 'person', 'former_colleague')......]
    id_labels_cql = cql_string.get_1D_node_by_startnode_id_and_relationname % node_id
    id_labels = run_cql(graph, id_labels_cql)
    id_labels = id_labels.data()
    # Neo4jMiningEdge(frm, to, elb, frmlb, tolb)
    edges = [Neo4jMiningEdge(node_id, _["node_id"], _["relation_name"], start_lable, _["node_label"][0])
             for _ in id_labels]
    return edges


def get_data_by_hrt_lable(graph, h_label, r_label, t_label):
    hrt_cql = cql_string.get_data_by_hrt_lable % (h_label, r_label, t_label)
    hrt = run_cql(graph, hrt_cql)
    hrt = hrt.data()
    hrt = [(_["h"], _["r"], _["t"]) for _ in hrt]
    # print(hrt)
    return hrt
