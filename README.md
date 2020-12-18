# ssm_neo4j
subgraph structure mining based on neo4j using gSpan algorithm
使用gSpan算法基于neo4j图库的子图结构挖掘

# sh install
pip install ssm-neo4j==1.0

# How use
demo_with_visible.py
demo_without_visible.py

demo_with_visible.py will save subgraph structure as png
demo_with_visible.py 会将子图结构保存成图片
demo_without_visible.py will not save subgraph structure as png
demo_without_visible.py 不会将子图结构保存成图片

#Parameter Suggest
min_num_vertices:How many nodes in subgraph structure at least
min_num_vertices:表示子图结构中最少有多少个节点
max_num_vertices:How many nodes in subgraph structure at most
max_num_vertices:表示子图结构中最多有多少个节点
min_num_vertices must greater than 1
min_num_vertices:必须大于1
max_num_vertices cannot be too large
max_num_vertices:不建议太大

### Reference
https://sites.cs.ucsb.edu/~xyan/software/gSpan.htm
https://github.com/betterenvi/gSpan


