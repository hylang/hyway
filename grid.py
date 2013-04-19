from collections import Mapping
from copy import deepcopy


class Grid(Mapping):
    """
    A Grid is a two-dimensional data-structure.

    >>> g = Grid(5, 5)
    >>> Grid.pprint(g)
    0 0 0 0 0
    0 0 0 0 0
    0 0 0 0 0
    0 0 0 0 0
    0 0 0 0 0
    >>> g[0, 0] = 1
    >>> g[4, 4] = 1
    >>> Grid.pprint(g)
    1 0 0 0 0
    0 0 0 0 0
    0 0 0 0 0
    0 0 0 0 0
    0 0 0 0 1

    The height and width of the grid are inclusive while the indexing
    begins at zero.  Access to elements of the grid are provided via
    the Mapping interface.  Internally the elements are stored in a
    flat array and can be any Python object.  The default element is
    the integer 0, but can be specified via the 'value' parameter to
    the Grid's constructor:

    >>> g = Grid(3, 3, value=".")
    >>> Grid.pprint(g)
    . . .
    . . .
    . . .

    There are helpful static methods available for copying grids,
    creating grids from arrays, and pretty printing grids.

    >>> w = h = 3
    >>> world = [0, 0, 0,
    ...          1, 0, 1,
    ...          0, 1, 0]
    >>> g = Grid.from_array(w, h, world)
    >>> Grid.pprint(g)
    0 0 0
    1 0 1
    0 1 0

    Care must be taken when creating Grids from arrays to ensure that
    the proper dimensions are passed in.  The only assertion this
    method makes is that the product of the width and height are the
    same as the length of the input array.

    Grids can be compared for equality:

    >>> g1 = Grid(3, 3)
    >>> g2 = Grid(3, 3)
    >>> g1[0, 0] = 1
    >>> g2[0, 0] = 1
    >>> g3 = Grid(3, 3)
    >>> g1 == g2
    True
    >>> g1 == g3
    False
    """

    def __init__(self, width, height, value=0):
        self.width = width
        self.height = height
        self._grid = [value for _ in range(width * height)]

    @classmethod
    def copy(cls, other):
        g = cls(other.width, other.height)
        g._grid = deepcopy(other._grid)
        return g

    @classmethod
    def from_array(cls, width, height, arr, copy=True):
        assert len(arr) == width * height, ("Array dimensions do not "
                                            "match length of array.")
        g = cls(width, height)
        a = deepcopy(arr) if copy else arr
        g._grid = a
        return g

    @staticmethod
    def pprint(grid):
        for y in range(grid.height):
            print(" ".join(str(grid[x, y]) for
                           x in range(grid.width)))

    def _is_valid_location(self, x, y):
        if x < 0 or x > self.width - 1:
            return False
        if y < 0 or y > self.height - 1:
            return False
        return True

    def __len__(self):
        return self.width * self.height

    def __eq__(self, other):
        assert isinstance(other, Grid)
        return self._grid == other._grid

    def __iter__(self):
        return iter(self._grid)

    def __contains__(self, value):
        return value in self._grid

    def __getitem__(self, *args):
        if not self._is_valid_location(*args[0]):
            raise KeyError("({0}, {1}) is an invalid co-ordinate".format(
                *args[0]))
        try:
            return self._grid[args[0][1] * self.height + args[0][0]]
        except IndexError:
            raise KeyError("({0}, {1}) is an invalid co-ordinate".format(
                *args[0]))

    def __setitem__(self, *args):
        if not self._is_valid_location(*args[0]):
            raise KeyError("({0}, {1}) is an invalid co-ordinate".format(
                *args[0]))
        try:
            self._grid[args[0][1] * self.height + args[0][0]] = args[1]
        except IndexError:
            raise KeyError("({0}, {1}) is an invalid co-ordinate".format(
                *args[0]))


class Torus(Grid):
    """
    A grid whose edges are connected.

    >>> w = h = 3
    >>> world = [0, 1, 0,
    ...          0, 0, 0,
    ...          0, 2, 0]
    >>> t = Torus.from_array(w, h, world)
    >>> Torus.pprint(t)
    0 1 0
    0 0 0
    0 2 0
    >>> t[1, 0]
    1
    >>> t[1, -1]
    2
    >>> t[4, 0]
    1
    """

    def __getitem__(self, *args):
        x = args[0][0] % self.width
        y = args[0][1] % self.height

        return self._grid[y * self.height + x]

    def __setitem__(self, *args):
        x = args[0][0] % self.width
        y = args[0][1] % self.height

        self._grid[y * self.height + x] = args[1]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
