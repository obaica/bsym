# From http://stackoverflow.com/questions/6284396/permutations-with-unique-values

class unique_element:
    def __init__( self, value, occurrences ):
        self.value = value
        self.occurrences = occurrences

def unique_permutations( elements ):
    set_of_elements = set( elements )
    unique_list = [ unique_element( e, elements.count( e ) ) for e in set_of_elements ]
    u = len( elements )
    return unique_permutation_helper( unique_list, [0]*u, u-1 )

def unique_permutation_helper( unique_list, result_list, d ):
    if d < 0:
        yield tuple( result_list )
    else:
        for i in unique_list:
            if i.occurrences > 0:
                result_list[d] = i.value
                i.occurrences -= 1
                for g in unique_permutation_helper( unique_list, result_list, d-1 ):
                    yield g
                i.occurrences += 1

def flatten_list( this_list ):
    return [ item for sublist in this_list for item in sublist ]

def all_permutations( labels, number_of_sites=None ):
    # labels is a list of site occupations and their number in this system
    occupation_list = flatten_list( [ [ key ] * labels[key] for key in labels ] )
    if number_of_sites:
        assert( len( occupation_list ) == number_of_sites )
    return list( unique_permutations( occupation_list ) )

def next_permutationS(l):
    # from https://raw.githubusercontent.com/shreevatsa/misc-math/master/pypermutations.py
    # discussion at http://stackoverflow.com/questions/6534430/why-does-pythons-itertools-permutations-contain-duplicates-when-the-original
    '''Changes a list to its next permutation, in place.
    Returns true unless wrapped around so result is lexicographically smaller. '''
    n = len(l)
    #Step 1: Find tail
    last = n-1 #tail is from `last` to end
    while last>0:
        if l[last-1] < l[last]: break
        last -= 1
    #Step 2: Increase the number just before tail
    if last>0:
        small = l[last-1]
        big = n-1
        while l[big] <= small: big -= 1
        l[last-1], l[big] = l[big], small
    #Step 3: Reverse tail
    i = last
    j = n-1
    while i < j:
        l[i], l[j] = l[j], l[i]
        i += 1
        j -= 1
    return last > 0, l

