# coding=utf-8
from .import gspan_tool
from .import neo4j_mining_tool
import collections
import copy
from .DFScode import DFScode
from .DFSedge import DFSedge
from .project_dfs import PDFS
from .neo4j_mining_History import Neo4jMiningHistory


class GSpan(object):
    """`gSpan` algorithm."""

    def __init__(self,
                 ip="127.0.0.1",
                 username="neo4j",
                 password="123456",
                 min_num_vertices=2,
                 max_num_vertices=16,
                 visible=False):
        self.graph = neo4j_mining_tool.get_neo4j_connect(ip, username, password)
        self.DFS_tree_code = DFScode()
        self.support = 0
        self.frequent_subgraphs = list()
        self._min_num_vertices = min_num_vertices
        self._max_num_vertices = max_num_vertices
        self.visible = visible

    def run(self):
        for root in gspan_tool.init_all_root_generator(self.graph):
            for vevlb, projected in root.items():  # projected is list of PDFS
                self.DFS_tree_code.append(DFSedge(0, 1, vevlb))
                self.subgraph_mining(projected)
                self.DFS_tree_code.pop()

        for _ in self.frequent_subgraphs:
            print(_)

    def subgraph_mining(self, projected):
        print("subgraph_mining start.....")
        if not self.is_min():  # DFS_tree_code is min
            return
        self.report()  # store
        num_vertices = self.DFS_tree_code.get_num_vertices()
        self.DFS_tree_code.build_rmpath()
        rmpath = self.DFS_tree_code.rmpath
        print("subgraph_mining rmpath is:", rmpath)
        maxtoc = self.DFS_tree_code[rmpath[0]].to  # most right path end node (dfs)id
        min_vlb = self.DFS_tree_code[0].vevlb[0]  # most right path start node label
        print("subgraph_mining maxtoc is:{}, min_vlb is:{}".format(maxtoc, min_vlb))

        forward_root = collections.defaultdict(list)  # list<PDFS>
        backward_root = collections.defaultdict(list)  # list<PDFS>
        print("subgraph_mining len(projected) is:{}".format(len(projected)))
        for p in projected:  # this projected is data from neo4j
            history = Neo4jMiningHistory(p)

            # backward
            for rmpath_i in rmpath[::-1]:
                e = gspan_tool.get_neo4j_backward_edge(
                    self.graph,
                    history.edges[rmpath_i],  # node in most right path
                    history.edges[rmpath[0]],  # rmpath[0]:most right path end edge
                    history)

                if e is not None:
                    backward_root[(self.DFS_tree_code[rmpath_i].frm, e.elb)].append(PDFS(e, p))  # p->e
            if bool(backward_root):
                print("subgraph_mining backward_root key is:{}".format(backward_root.keys()))
            # pure forward
            if num_vertices >= self._max_num_vertices:  # num of vertices greater than _max_num_vertices
                continue

            edges = gspan_tool.get_neo4j_forward_pure_edges(
                self.graph,
                history.edges[rmpath[0]],  # rmpath[0]:most right path end edge
                min_vlb,  # most right path start node label
                history)

            for e in edges:
                forward_root[
                    (maxtoc, e.elb, e.tolb)
                ].append(PDFS(e, p))  # p->e
            # rmpath forward
            for rmpath_i in rmpath:  # search most right path from down to up
                edges = gspan_tool.get_neo4j_forward_rmpath_edges(
                    self.graph,
                    history.edges[rmpath_i],
                    min_vlb,
                    history)
                for e in edges:
                    forward_root[
                        (self.DFS_tree_code[rmpath_i].frm,
                         e.elb, e.tolb)
                    ].append(PDFS(e, p))  # p->e
        if bool(forward_root):
            print("subgraph_mining forward_root key is:{}".format(forward_root.keys()))
        # backward
        for to, elb in backward_root:
            frm_label = backward_root[(to, elb)][0].edge.frmlb
            to_label = backward_root[(to, elb)][0].edge.tolb
            new_vevlb = (frm_label, elb, to_label)
            self.DFS_tree_code.append(DFSedge(maxtoc, to, new_vevlb))
            print("subgraph_mining for backward_root key:", to, elb)
            print("subgraph_mining for backward_root len is:", len(backward_root[(to, elb)]))
            self.subgraph_mining(backward_root[(to, elb)])
            self.DFS_tree_code.pop()
        # forward
        for frm, elb, vlb2 in forward_root:
            frm_label = forward_root[(frm, elb, vlb2)][0].edge.frmlb
            new_vevlb = (frm_label, elb, vlb2)
            self.DFS_tree_code.append(DFSedge(frm, maxtoc + 1, new_vevlb))
            self.subgraph_mining(forward_root[(frm, elb, vlb2)])
            self.DFS_tree_code.pop()

        return self

    def is_min(self):
        print("is_min start...")
        if len(self.DFS_tree_code) == 1:
            return True

        dfs_code_min = DFScode()
        min_vevlb, root = self.DFS_tree_code.get_min_vevlb_and_dfsproject()
        dfs_code_min.append(DFSedge(0, 1, min_vevlb))  # pull in dfs_code_min is list of DFSedge

        res = self.project_is_min(root[min_vevlb], dfs_code_min)
        print("is_min end, res is:", res)
        return res

    # all projected in this function is DFS_tree_code projected not from neof4j
    def project_is_min(self, projected, dfs_code_min):  # projected is list of PDFS
        print("project_is_min start...")
        dfs_code_min.build_rmpath()
        rmpath = dfs_code_min.rmpath
        print("project_is_min rmpath is:", rmpath)
        min_vlb = dfs_code_min[0].vevlb[0]  # most rigth path root label
        maxtoc = dfs_code_min[rmpath[0]].to  # most rigth path end node id

        backward_root = collections.defaultdict(list)  # list<PDFS>
        """
            step 1: backward_edge
            step 2: forward_edge
        """
        flag, newto = False, 0,
        end = -1  # have direction
        for i in range(len(rmpath) - 1, end, -1):
            if flag:
                break
            for p in projected:  # PDFS
                history = Neo4jMiningHistory(p)
                for rmpath_i in rmpath[::-1]:
                    # rmpath_i: any node id in most rigth path
                    # rmpath[0]: most rigth path end node id
                    e = gspan_tool.get_backward_edge(self.DFS_tree_code,
                                                     history.edges[rmpath_i],
                                                     history.edges[rmpath[0]],
                                                     history)

                    if e is not None:
                        backward_root[e.elb].append(PDFS(e, p))  # p->e
                        newto = dfs_code_min[rmpath[i]].frm
                        flag = True

        if flag:
            backward_min_elb = min(backward_root.keys())
            frm_label = backward_root[backward_min_elb][0].edge.frmlb
            to_label = backward_root[backward_min_elb][0].edge.tolb
            new_vevlb = (frm_label, backward_min_elb, to_label)
            dfs_code_min.append(DFSedge(maxtoc, newto, new_vevlb))
            idx = len(dfs_code_min) - 1
            if self.DFS_tree_code[idx] != dfs_code_min[idx]:
                return False
            return self.project_is_min(backward_root[backward_min_elb], dfs_code_min)

        forward_root = collections.defaultdict(list)  # list<PDFS>
        flag, newfrm = False, 0
        for p in projected:
            history = Neo4jMiningHistory(p)
            edges = gspan_tool.get_forward_pure_edges(self.DFS_tree_code,
                                                      history.edges[rmpath[0]],
                                                      min_vlb,
                                                      history)

            if len(edges) > 0:
                flag = True
                newfrm = maxtoc
                for e in edges:
                    forward_root[(e.elb, e.tolb)].append(PDFS(e, p))  # p->e

        for rmpath_i in rmpath:
            if flag:
                break
            for p in projected:
                history = Neo4jMiningHistory(p)
                edges = gspan_tool.get_forward_rmpath_edges(
                    self.DFS_tree_code, history.edges[rmpath_i], min_vlb, history)

                if len(edges) > 0:
                    flag = True
                    newfrm = dfs_code_min[rmpath_i].frm
                    for e in edges:
                        forward_root[(e.elb, e.tolb)].append(PDFS(e, p))  # p->e

        if not flag:
            return True

        forward_min_evlb = min(forward_root.keys())
        frm_label = forward_root[forward_min_evlb][0].edge.frmlb
        new_vevlb = (frm_label, forward_min_evlb[0], forward_min_evlb[1])
        dfs_code_min.append(DFSedge(newfrm, maxtoc + 1, new_vevlb))

        idx = len(dfs_code_min) - 1
        if self.DFS_tree_code[idx] != dfs_code_min[idx]:
            return False
        return self.project_is_min(forward_root[forward_min_evlb], dfs_code_min)

    def report(self):
        if self.DFS_tree_code.get_num_vertices() < self._min_num_vertices:
            return
        self.frequent_subgraphs.append(copy.deepcopy(self.DFS_tree_code))
        if self.visible:
            self.DFS_tree_code.plot()
