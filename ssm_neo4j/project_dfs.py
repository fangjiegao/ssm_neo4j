# coding=utf-8


class PDFS(object):
    """PDFS class."""

    def __init__(self, edge=None, prev=None):
        """Initialize PDFS instance."""
        self.edge = edge  # type is Neo4jMiningEdge
        self.prev = prev

    def __repr__(self):
        return str(self.edge) + "  ->  " + str(self.prev)
