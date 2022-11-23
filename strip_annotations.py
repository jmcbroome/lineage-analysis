'''
Script for the removal of nextclade or other extraneous annotations to prepare a tree for automated Pango lineage annotation.
Nextclade annotations are stored in the first index of standard public trees, so this script overwrites the first index with the second,
except where the second is an automatically maintained lineage, as curated lineages take precedent.
The output tree will contain a single column of annotation containing pango and auto lineages and a blank column.
'''

import bte
import sys
t = bte.MATree(sys.argv[1])
nannd = {}
for n in t.depth_first_expansion():
    if len(n.annotations) >= 2:
        # printer = any(["(" in a for a in n.annotations])
        # if printer:
            # print("ORIGINAL:",n.annotations)
        #overwrite the first column with the value of the second column, then blank the second column.
        #unless the second column is an auto annotation AND there's something in the first column, in which case we retain the first column.
        #also, retain the first column if the second is blank. No need to throw away information. 
        newann = ["", ""]
        #if the second entry is blank, use the first. It may be blank also, which is fine.
        if len(n.annotations[1]) == 0 and " " not in n.annotations[0]:
            #special case- remove annotations with whitespace in them to handle nextclade annotations with no corresponding pango annotation.
            newann[0] = n.annotations[0]
        #if the second entry is auto and the first is not blank, retain the first.
        elif "auto." in n.annotations[1] and len(n.annotations[0]) > 0:
            newann[0] = n.annotations[0]
        #if the second entry is not auto and not blank, overwrite the first with it.
        else:
            newann[0] = n.annotations[1]
        # if printer:
            # print("AFTER FILTERING",newann)
        nannd[n.id] = newann
t.apply_annotations(nannd)
t.save_pb(sys.argv[2])