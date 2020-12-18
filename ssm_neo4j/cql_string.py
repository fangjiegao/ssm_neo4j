# coding=utf-8

# 查找所有节点标签
get_all_lable = "call db.labels"

# 统计某种节点标签的数量
get_lable_count = "MATCH (n:%s) RETURN count(n) as %s"

# 统计某以关系的数量
get_all_relation_count = "MATCH (n)-[r:%s]->() RETURN COUNT(r) as %s"

# 查找所有关系
get_all_relations = "match (n)-[relation]->(c) return distinct type(relation) as relation"

# 查找所有关系结构
get_all_1_hrt_shape = "MATCH (n)-[r]->(m) RETURN distinct labels(n) as h_label,type(r) as r_label,labels(m) as t_label"

# 根据节点和关系的标签查找关系的数量
get_all_1_hrt_shape_count = "MATCH (n:%s)-[r:%s]->(m:%s) RETURN count(r) as %s"

# 根据节点和关系的标签查找关系,分页
match_data_by_hrt_lable = "MATCH (n:%s)-[r:%s]->(m:%s) return id(n) as h, type(r) as r, id(m) as t skip %s limit %s"

# 根据节点和关系的标签查找关系,不分页
match_data_by_hrt_lable_no_batch = "MATCH (n:%s)-[r:%s]->(m:%s) return id(n) as h, type(r) as r, id(m) as t"

# 根据节点id查找节点的标签
get_nodelable_by_id = "MATCH (n) where id(n) = %s RETURN labels(n) as label"

# 通过头尾节点的id查找关系
get_relation_by_hid_tid = "MATCH (n)-[r]->(c) where id(n) = %s and id(c) = %s RETURN type(r) as relation"

# 得到所有节点的id,就是得到所有的节点
get_all_node_id = "MATCH (n) RETURN id(n) as node_id"

# 得到所有节点的id,就是得到所有的节点,分页
get_all_node_id_batch = "MATCH (n) RETURN id(n) as node_id skip %s limit %s"

# 得到节点的数量
get_all_node_count = "MATCH (n) RETURN count(1) as node_count"

# 得到节点的所有一度关系节点
get_1D_node_by_startnode_id_and_relationname = \
    "MATCH (n)-[r]-(m) where id(n) = %s RETURN id(m) as node_id, labels(m) as node_label, type(r) as relation_name"

# 根据节点和关系的标签查找关系
get_data_by_hrt_lable = "MATCH (n:%s)-[r:%s]-(m:%s) return id(n) as h, type(r) as r, id(m) as t"
