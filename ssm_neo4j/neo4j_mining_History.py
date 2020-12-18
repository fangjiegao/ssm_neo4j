# coding=utf-8
import collections


class Neo4jMiningHistory(object):
    """History class."""

    def __init__(self, pdfs):
        """Initialize History instance."""
        # 对所有的pdfs分解处理
        super(Neo4jMiningHistory, self).__init__()
        self.edges = list()  # list<Neo4jMiningEdge>

        self.vertices_used = collections.defaultdict(int)  # {100: 1}:id=100 was used
        self.edges_used = collections.defaultdict(int)

        if pdfs is None:
            return
        while pdfs:
            """
                 pdfs.edge, pdfs.prev
            """
            e = pdfs.edge  # Neo4jMiningEdge
            self.edges.append(e)
            # set and mark
            (self.vertices_used[e.frm],
                self.vertices_used[e.to],
                self.edges_used[e.eid]) = 1, 1, 1

            pdfs = pdfs.prev
        self.edges = self.edges[::-1]  # reverse

    def has_vertex(self, vid):
        """Check if the vertex with vid exists in the history."""
        return self.vertices_used[vid] == 1

    def has_edge(self, eid):
        """Check if the edge with eid exists in the history."""
        return self.edges_used[eid] == 1

    def __repr__(self):
        return "vertices_used:" + str(self.vertices_used) + "\n" \
               + "edges_used:" + str(self.edges_used) + "\n" \
               + "edges:" + str(self.edges)
