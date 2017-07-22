import numpy as np

class Configuration( np.matrix ):
    """
    A :any:`Configuration` describes a specific arrangement of objects in the vector space of possible positions.
    Objects are represented by integers, with indistinguishable objects denoted by identical integers.
    This class subclasses `numpy.matrix <https://docs.scipy.org/doc/numpy/reference/generated/numpy.matrix.html>`_. 
    Each configuration in the vector space of positions is represented as a column vector.
    """ 

    def __new__( cls, *args, **kwargs ):
        return super().__new__( cls, *args, **kwargs )

    def __init__( self, *args, **kwargs ):
        self.count = None
        self.lowest_numeric_representation = None
        super().__init__()

    def __arrary_finalize__( self, obj ):
        pass

    def matches( self, test_configuration ):
        """
        Test whether this configuration is equal to another configuration.

        Args:
            test_configuration (bsym.Configuration): The configuration to compare against.

        Returns:
            (bool): True | False.
        """
        return ( self == test_configuration ).all()

    def is_equivalent_to( self, test_configuration, symmetry_operations ):
        """
        Test whether this configuration is equivalent to another configuration
        under one or more of a set of symmetry operations.

        Args:
            test_configuration (bsym.Configuration): The configuration to compare against.
            symmetry_operations (list(bsym.SymmetryOperation): A list of SymmetryOperation objects.

        Returns:
            (bool): True | False
        """
        for symmetry_operation in symmetry_operations:
            if ( symmetry_operation.operate_on( self ).matches( test_configuration ) ):
                return True 
        else:
            return False

    def is_in_list( self, list ):
        """
        Test whether this configuration is in a list of configurations.

        Args:
            list (list(bsym.Comfiguration)): A list of Configuration instances.

        Returns:
            (bool): True | False
        """
        return next( ( True for c in list if self.matches( c ) ), False )

    def has_equivalent_in_list( self, list, symmetry_operations ):
        """
        Test whether this configuration is equivalent by symmetry to one or more
        in a list of configurations.

        Args:
            list (list(bsym.Configuration)): A list of :any:`Configuration` instances.
            symmetry_operations (list(bsym.SymmetryOperation)): A list of :any:`SymmetryOperation` objects.

        Returns:
            (bool): True | False 
        """
        return next( ( True for c in list if self.is_equivalent_to( c, symmetry_operations ) ), False )

    def set_lowest_numeric_representation( self, symmetry_operations ):
       """
       Sets `self.lowest_numeric_representation` to the lowest value numeric representation of this configuration when permutated under a set of symmetry operations.

       Args:
           symmetry_operations (list): A list of :any:`SymmetryOperation` instances.

       Returns:
           None
       """
       self.lowest_numeric_representation = min( [ symmetry_operation.operate_on( self ).as_number for symmetry_operation in symmetry_operations ] )

    def numeric_equivalents( self, symmetry_operations ):
        """
        Returns a list of all symmetry equivalent configurations generated by a set of symmetry operations
        with each configuration given in numeric representation.

        Args:
            symmetry_operations (list): A list of :any:`SymmetryOperation` instances.

        Returns:
            (list(int)): A list of numbers representing each equivalent configuration.
        """
        return [ symmetry_operation.operate_on( self ).as_number for symmetry_operation in symmetry_operations ]

    @property
    def as_number( self ):
        """
        A numeric representation of this configuration.
        """
        return int( ''.join( str(e) for e in self.tolist() ) )

    @classmethod
    def from_tuple( cls, this_tuple ):
        """
        Construct a :any:`Configuration` from a `tuple`,
        e.g.::
     
            Configuration.from_tuple( ( 1, 1, 0 ) )
 
        Args:
            this_tuple (tuple): The tuple used to construct this :any:`Configuration`.

        Returns:
            (:any:`Configuration`): The new :any:`Configuration`.
        """
        return( cls( np.asarray( this_tuple ) ).T )

    @classmethod
    def from_vector( cls, this_vector ):
        """
        Construct a :any:`Configuration` from a `vector`,
        e.g.::

            Configuration.from_vector( [ 1, 1, 0 ] )

        Args:
            this_vector (list): the vector used to construct this :any:`Configuration`.

        Returns:
            (:any:`Configuration`): The new :any:`Configuration`.
        """
        return( cls( np.asarray( this_vector ) ).T )

    def tolist( self ):
        """
        Returns the configuration data as a list.
        
        Args:
            None

        Returns:
            (List)
        """
        return [ e[0] for e in super().tolist() ]

    def pprint( self ):
        print( ' '.join( [ str(e) for e in self.tolist() ] ) )

    def position( self, label ):
        """
        Returns the vector indices where elements are equal to `label`.

        Args:
            label (int): The label used to select the vector positions.

        Returns:
            (list): A list of all positions that match `label`.
        """
        return [ i for i,x in enumerate( self.tolist() ) if x == label ]

    def __repr__( self ):
        to_return = "Configuration({})\n".format(self.tolist())
        return to_return

    def map_objects( self, objects ):
        """
        Returns a dict of objects sorted according to this configuration.

        Args:
            objects [list]: A list of objects.

        Returns:
            sorted_objects [dict]: A dictionary of sorted objects.
        """
        if len( objects ) != len( self ):
            raise ValueError
        sorted_objects = {}
        for key in set( self.tolist() ):
            sorted_objects[key] = [ o for k, o in zip( self.tolist(), objects ) if k is key ]
        return sorted_objects 
