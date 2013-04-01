#!/usr/bin/python
import sys

def get_overlap_len(fragment_a,fragment_b):
    best_overlap = 0
    min_len = min(len(fragment_a),len(fragment_b))+1
    for overlap_len in xrange(1,min_len):
        if(fragment_a[-overlap_len:] == fragment_b[0:overlap_len]):
            best_overlap = max(overlap_len,best_overlap)
    for overlap_len in xrange(1,min_len):
        if(fragment_b[-overlap_len:] == fragment_a[0:overlap_len]):
            best_overlap = max(overlap_len,best_overlap)
    if(fragment_a.find(fragment_b) > -1):
        return len(fragment_b)
    if(fragment_b.find(fragment_a) > -1):
        return len(fragment_a)
    return best_overlap

def assemble(fragments):
    remaining_fragments = set(xrange(len(fragments)))
    overlaps = dict()
    while(len(remaining_fragments) > 1):
        fragments_list = list(remaining_fragments)
        for i in fragments_list:
            for j in fragments_list:
                if(i >= j):
                    continue
                overlap = get_overlap_len(fragments[i],fragments[j])
                overlaps[tuple([i,j])] = overlap

        join_a = len(fragments_list) + 1
        join_b = len(fragments_list) + 1
        max_overlap = -1
        for i in overlaps:
            if(overlaps[i] > max_overlap):
                max_overlap = overlaps[i]
                join_a = i[0]
                join_b = i[1]

        if(max_overlap <= 0):
            for i in fragments_list:
                print fragments[i]
            return "Wrong"

        for i in fragments_list:
            if(i != join_a):
                key = tuple([min(i,join_a),max(i,join_a)])
                del overlaps[key]
            if(i != join_b and i != join_a):
                key = tuple([min(i,join_b),max(i,join_b)])
                del overlaps[key]
        remaining_fragments.remove(join_a)
        remaining_fragments.remove(join_b)

        if(fragments[join_a][0:max_overlap] == fragments[join_b][-max_overlap:]):
            new_fragment = fragments[join_b] + fragments[join_a][max_overlap:]
        elif(fragments[join_b][0:max_overlap] == fragments[join_a][-max_overlap:]):
            new_fragment = fragments[join_a] + fragments[join_b][max_overlap:]
        elif(fragments[join_b].find(fragments[join_a]) >= 0):
            new_fragment = fragments[join_b]
        elif(fragments[join_a].find(fragments[join_b]) >= 0):
            new_fragment = fragments[join_a]
        else:
            return "Wrong"

        if(len(fragments[join_a]) + len(fragments[join_b]) - max_overlap != len(new_fragment)):
            return "Wrong combining"

        fragments.append(new_fragment)
        remaining_fragments.add(len(fragments)-1)
    return fragments[-1]

test_cases = open(sys.argv[1], 'r')
for test in test_cases:
    test = test.rstrip()
    if(0 == len(test)):
        continue
    fragments = test.split(";")
    print assemble(fragments)
test_cases.close()
