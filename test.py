"""
Here is the zone where we test all the functions
"""
import unittest
import numpy as np
from gridenvs.hero_gridworld import StrMapHeroGridEnv

class TestStringMethods(unittest.TestCase):
    """
        The following methods test the function average_colors_zone in gridworld.py
    """
    def _test_average_colors_zone(self, matrix, average_rgb):
        """
        A private method used to create tests
        """
        m_average = StrMapHeroGridEnv.average_colors_zone(matrix)
        matrix_average_rgb = np.zeros((len(m_average), len(m_average[0])), dtype = object)
        matrix_average_rgb.fill(average_rgb)
        self.assertTrue((m_average==matrix_average_rgb).all())

    def test_average_colors_zone_good_matrix(self):
        matrix = [[ [1,2,3], [0,0,0], [1,1,1] ],
                  [ [1,2,3], [0,2,0], [1,3,1] ],
                  [ [1,2,3], [0,0,3], [3,2,1] ]
                  ]
        average_rgb = [8 / 9, 14 / 9, 15 / 9]
        self._test_average_colors_zone(matrix, average_rgb)


    def test_average_colors_zone_bad_shape_matrix(self):
        matrix = [[ [1,2,3], [0,0,0], [1,1,1] ],
                  [ [1,2,3], [0,2,0], [1,3,1] ],
                  [ [1,2,3], [0,0,3], [3,2,1], [0,0,0] ],
                  ]
        average_rgb = [8 / 9, 14 / 9, 15 / 9]
        with self.assertRaises(Exception):
            m_average = StrMapHeroGridEnv.average_colors_zone(matrix)

    def test_average_colors_zone_bad_shape_matrix_rgb(self):
        matrix = [[ [1,2,3], [0,0,0], [1,1,1, 0] ],
                  [ [1,2,3], [0,2,0], [1,3,1] ],
                  [ [1,2,3], [0,0,3], [3,2,1] ],
                  ]
        average_rgb = [8 / 9, 14 / 9, 15 / 9]
        with self.assertRaises(Exception):
            m_average = StrMapHeroGridEnv.average_colors_zone(matrix)

    """
        The following methods test the function average_colors in gridworld.py
    def _test_average_colors(self, matrix, averaged_matrix, zone_size_x, zone_size_y):

        #A private method used to create tests

        smaphero = StrMapHeroGridEnv()
        matrix = smaphero.average_colors(matrix, zone_size_x, zone_size_y)
        self.assertTrue((matrix==averaged_matrix).all())

    def test_average_colors_good_matrix(self):
        matrix = np.zeros((10,10), dtype = object)
        matrix.fill([1, 1, 1])
        average_rgb = [1 / 3, 1 / 3, 1 / 3]
        averaged_matrix = np.ones((10,10), dtype = object)
        averaged_matrix.fill(1 / 3)
        self._test_average_colors(matrix, averaged_matrix, 2, 2)
    """
if __name__ == "__main__":
    unittest.main()
