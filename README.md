# symmetry

This library has been written to identify symmetry inequivalent arrangements of objects on an arbitrary lattice.
It's intended application is for enumeration of atom configurations on crystalline surfaces.
An example application is described in [this publication][LTO surfaces paper].

The initial version was written by [Benjamin J. Morgan][my site] in 2014.

Source code is available as a git repository at [https://github.com/bjmorgan/symmetry][github]

Please direct any enquiries to b.j.morgan@bath.ac.uk.

[LTO surfaces paper]: TODO
[my site]: http://analysisandsynthesis.com
[github]: https://github.com/bjmorgan/symmetry

# introduction

A simple example of this code if provided in `./examples/first_example.py`. This enumerates the possible ways to occupy two sites (out of four) on a square 2x2 lattice.

Sites in a square lattice can be represented by numerical labels:
 
      - -
    | 1 2 |
    | 3 4 |
      - -

The script first constructs the "space group" by reading a file containing all relevant symmetry operations.

    spacegroup_filename = '../spacegroups/cubic_spacegroup_annotated'
    sg = sym.SpaceGroup.read_from_file( spacegroup_filename )

This file contains a list of integer vectors. Each entry describes the mapping from the current site (given by its position in the vector) to the equivalent site under this operation.
e.g.

- the identity keeps all sites unchanged: `1 2 3 4`
- a 90 degree rotation clockwise maps 1 -> 2, 2 -> 4, 4 -> 3, and 3 -> 1, and is encoded as `2 4 1 3`.
- a translation by half the cell to the right maps 1 -> 2, 2 -> 1, 3 -> 4, and 4 -> 3, and is encoded as `2 1 4 3`.

We then define the distribution of different sites, e.g. for 2 occupied and 2 unoccupied sites:

    site_dist = { 1 : 2, 
                  0 : 2 }
                  
 with each entry in the dictionary `label : number`. Here we define two sites will have occupation label `1` and 2 will have occupation label `2`.
 
 The unique configurations are generated by
 
     unique_configurations = sym.process.unique_configurations_from_sites( site_dist, sg, verbose=True )
     
 A clean print of the occupation vectors for the results is generated with:
 
 [ config.pprint() for config in unique_configurations ] 
 
 In this case we get:
 
     1 1 0 0
     1 0 0 1
     
 (or equivalent), which represent adjacent and diagonal occupation patterns:
 
      - -        - -
    | 1 1 |    | 1 0 |
    | 0 0 |    | 0 1 |
      - -        - -
     
 More example scripts (those used generating the surface atom configurations in [this paper][LTO surfaces paper] are in ./examples/LTO_surfaces

# spacegroups and symmetry operations

For the purposes of this code, a symmetry operation defines the mapping between two equivalent sets of positions. For example, a 2x2 square lattice supercell has 4 (equivalent) site:

      - -
    | 1 2 |
    | 3 4 |
      - -

A rotation of 90 degrees clockwise moves these to:

      - -
    | 3 1 |
    | 4 2 |
      - -

which can be described with a vector `2 4 1 3`: each entry encodes the initial site as the index within the vector, and the final site as the value at that index.
Internally "SpaceGroup" objects are stored as matrices that map from the initial to final coordinates (these are [generalized permutation matrices][gpm]), but can be initialised from vector notation using

    SpaceGroup.from_vector( <vector> )

and a SpaceGroup object `symmetry_operation` can be converted back to vector notation using

    symmetry_operation.as_vector()

Symmetry operations can operate on a vector describing lattice occupations using

    symmetry_operation.operate_on( configuration )

Symmetry operations can also be labelled, in order to reference them amongst a space group set, using

    symmetry_operation.set_label( label )

where `label` is a string.

Finally, a useful method for generating new symmetry operations is

    symmetry_operation.similarity_transform( symmetry_operation_2 )

which calculates S^{-1}.A.S
This can be used to build up the full set of symmetry operations for a space group using e.g.

    sg.append( s5_1.similarity_transform( c3_4 ).set_label( 's5_2' ) )

where `sg` is the SpaceGroup object, and `s5_1` and `c3_4` are SymmetryOperation objects. This example also illustrates appending a symmetry operation to a preexisting space group, and in line labelling of the new symmetry operation.

A SpaceGroup object is a set of SymmetryOperation objects. The simplest way to generate this is to use

    SpaceGroup.read_from_file( filename )

which will read a file of symmetry operations in vector notation, ignoring blank lines and comments marked with `#`.
An alternative initialisation method is

    SpaceGroup.read_from_file_with_labels( filename )
   
which will read lines such as

    E  1 2 3 4
    S1 2 4 1 3 

which now have identifying strings in the first entry of each line to be read.

The full set of labels for a SpaceGroup object `sg` can be obtained using

    sg.labels()

and individual symmetry operations can be referenced using

    sg.by_label( label )

Once generated, the set of mapping vectors (symmetry operations) that make up a space group can be save to a file using

    sg.save_symmetry_operation_vectors_to( filename )

[gpm]: https://en.wikipedia.org/wiki/Generalized_permutation_matrix

