# coding=utf-8

VACANT_EDGE_ID = -1
VACANT_VERTEX_ID = -1
VACANT_EDGE_LABEL = -1
VACANT_VERTEX_LABEL = -1
VACANT_GRAPH_ID = -1
AUTO_EDGE_ID = -1
AUTO_VERTEX_ID = -1
VERTEX_LABEL = -1


class Neo4jMiningEdge(object):
    """Edge class."""
    def __init__(self,
                 # eid=VACANT_EDGE_ID,
                 frm=VACANT_VERTEX_ID,
                 to=VACANT_VERTEX_ID,
                 elb=VACANT_EDGE_LABEL,
                 frmlb=VERTEX_LABEL,
                 tolb=VERTEX_LABEL):
        """Initialize Edge instance.
        Args:
            frm: source vertex id in neo4j.
            to: destination vertex id in neo4j.
            elb: edge label.
            frmlb: source vertex label.
            tolb: destination vertex label.
        """
        self.frm = frm  # head node id in neo4j
        self.to = to  # tail node id in neo4j
        self.elb = elb  # edge label
        self.frmlb = frmlb  # head node label
        self.tolb = tolb  # tail node label
        self.eid = str(frm) + "_" + str(to)

    def __repr__(self):
        return str(self.eid) + ":" + str(self.frm) + "(" + str(self.frmlb) + ")" + "-" + \
               str(self.elb) + "->" + str(self.to) + "(" + str(self.tolb) + ")"
