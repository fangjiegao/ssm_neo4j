# coding=utf-8
"""The main program that runs gSpan."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ssm_neo4j


def main():
    """Run gSpan."""
    ssm_neo4j_instance = ssm_neo4j.neo4j_gSpan(
        ip='http:/127.0.0.1:7474',
        username='neo4j',
        password='123456',
        min_num_vertices=1,  # min_num_vertices must > 1
        max_num_vertices=4,  # max_num_vertices cannot be too large
        visible=False
    )

    ssm_neo4j_instance.run()
    return ssm_neo4j_instance


if __name__ == '__main__':
    ssm_neo4j_instance_ = main()
    print("print all subgraph structure:")
    for _ in ssm_neo4j_instance_.frequent_subgraphs:
        print(type(_), _)
