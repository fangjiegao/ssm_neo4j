# coding=utf-8
from .DFSedge import DFSedge
import collections
from .project_dfs import PDFS
from .neo4j_mining_Edge import Neo4jMiningEdge


class DFScode(list):
    """DFS tree code is a list of DFSedge."""

    def __init__(self):
        """Initialize DFS tree code."""
        super().__init__()
        self.rmpath = list()  # most right path

    def __eq__(self, other):
        """Check(Compare) equivalence of DFScode."""
        la, lb = len(self), len(other)
        if la != lb:
            return False
        for i in range(la):
            if self[i] != other[i]:  # call DFSedge.__eq__()
                return False
        return True

    def __ne__(self, other):
        """Check if not equal."""
        return not self.__eq__(other)

    def __repr__(self):
        """Represent DFS tree code in string way."""
        return ''.join(
            ['[', ','.join([str(dfsedge) for dfsedge in self]), ']']
        )

    def push_back(self, frm, to, vevlb):
        """Update(add) DFScode by adding one edge."""
        self.append(DFSedge(frm, to, vevlb))
        return self

    def build_rmpath(self):  # self: [five tuple,......]
        """Build right most path"""
        self.rmpath = list()
        old_frm = None
        for i in range(len(self) - 1, -1, -1):  # search five tuple list, from down to up
            dfsedge = self[i]
            frm, to = dfsedge.frm, dfsedge.to
            if frm < to and (old_frm is None or to == old_frm):  # tail node id < head node id
                self.rmpath.append(i)  # storage five tuple index in self, from down to up
                old_frm = frm
        return self

    def get_num_vertices(self):
        """
            Return number of vertices in the corresponding graph.
            see DFSedge
        """
        return len(set(
            [dfsedge.frm for dfsedge in self] +
            [dfsedge.to for dfsedge in self]
        ))

    def get_min_vevlb_and_dfsproject(self):
        root = []
        root_project = collections.defaultdict(list)  # list<PDFS>
        all_id = self.get_all_node_id()
        for _ in all_id:
            edges = self.forward_root_edges(_)
            for e in edges:
                root.append(e.vevlb)
                root_project[e.vevlb].append(PDFS(Neo4jMiningEdge(e.frm, e.to, e.vevlb[1], e.vevlb[0], e.vevlb[2]), None))
        print("forward_root_edges:", root)
        return min(root), root_project

    def get_all_node_id(self):
        all_node_id = set()

        def add_in_set(frm_id, to_id):
            all_node_id.add(frm_id)
            all_node_id.add(to_id)

        for _ in self:
            add_in_set(_.frm, _.to)
        return list(all_node_id)

    def forward_root_edges(self, vid):
        result = []
        edges = self.get_all_v_frm_edges(vid)  # edges is lis<DFSedge>
        for _ in edges:
            if _.vevlb[0] <= _.vevlb[2]:  # this node label < tail node label
                result.append(_)  # storage in result
        return result

    # get all edges which head node id is vid
    def get_all_v_frm_edges(self, vid):
        return [_ for _ in self if _.frm == vid]

    def get_1D_node_by_startnode_id_2_Neo4jMiningEdge(self, node_id):
        """
        edges = []
        for _ in self:
            # DFSedge (frm, to, vevlb, real_frm, real_to)
            if _.frm == node_id:
                edges.append(Neo4jMiningEdge(node_id, _.to, _.vevlb[1], _.vevlb[0], _.vevlb[2]))
        return edges
        """
        # _ is DFSedge(frm, to, vevlb, real_frm, real_to)
        return [Neo4jMiningEdge(node_id, _.to, _.vevlb[1], _.vevlb[0], _.vevlb[2]) for _ in self
                if _.frm == node_id]

    def get_all_vertex_label(self):
        return list(
            set([dfsedge.vevlb[0] for dfsedge in self] + [dfsedge.vevlb[2] for dfsedge in self])
        )

    def plot(self):
        """Visualize the graph."""
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
        except Exception as e:
            print('Can not plot graph: {}'.format(e))
            return
        gnx = nx.Graph()
        vlbs = dict()
        for _ in self:
            vlbs[_.frm] = _.vevlb[0]
            vlbs[_.to] = _.vevlb[2]
        elbs = {}
        for _ in self:
            gnx.add_node(_.frm, label=_.vevlb[0])
            gnx.add_node(_.to, label=_.vevlb[2])
            gnx.add_edge(_.frm, _.to, label=_.vevlb[1])
            elbs[(_.frm, _.to)] = _.vevlb[1]

        fsize = (min(16, 1 * self.get_num_vertices()),
                 min(16, 1 * self.get_num_vertices()))
        plt.figure(3, figsize=fsize)
        pos = nx.spectral_layout(gnx)
        nx.draw_networkx(gnx, pos, arrows=True, with_labels=True, labels=vlbs)
        nx.draw_networkx_edge_labels(gnx, pos, edge_labels=elbs)
        import time
        # plt.savefig(str(time.time()) + '.jpg')
        plt.savefig(str(time.time()) + '.png', dpi=500, bbox_inches='tight')
        # plt.show()
        # plt.pause(0.05)
        plt.close()