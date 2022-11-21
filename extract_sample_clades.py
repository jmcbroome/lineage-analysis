import sys
sys.path.append("~/bin:")
import bte
import numpy as np
t = bte.MATree(sys.argv[1])
annd = t.dump_annotations()
for ann, nid in annd.items():
    n = t.get_node(nid)
    basesamples = set()
    count = 0
    #first, pick the earliest sample descended from each child of n- 
    #ensuring that the LCA of the representative set is the query node, assuming tree topology is consistent.
    for c in n.children:
        if c.is_leaf():
            print(ann, c.id, sep='\t')
            basesamples.add(c.id)
            count += 1
        else:
            for cn in t.breadth_first_expansion(c.id):
                if cn.is_leaf():
                    print(ann, cn.id, sep='\t')
                    basesamples.add(cn.id)
                    count += 1
                    break
    #then fill it out with additional breadth-first samples from the parent.
    for c in t.breadth_first_expansion(nid):
        if c.is_leaf() and c.id not in basesamples:
            print(ann, c.id, sep='\t')
            count += 1
            if count >= 1000:
                break
