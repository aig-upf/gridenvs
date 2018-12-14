"""
Here is the zone where we test all the functions
"""
import unittest
import numpy as np
from gridenvs.hero_gridworld import StrMapHeroGridEnv

class TestStringMethods(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()
