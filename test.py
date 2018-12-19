"""
Here is the zone where we test all the functions
"""
import unittest
import cv2
import numpy as np
class TestStringMethods(unittest.TestCase):
    """
        The following methods are examples to implement tests. It is possible
    to make a function which is not a test but which can be used for the test.
    To do that, just make the function private by adding the character '_' at
    the begining at the name of the function.
    More info her: https://docs.python.org/3/library/unittest.html
    """
    def _example_function_which_is_not_a_test_function(a):
        return a+1

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_blurred_image(self):
        """
        A test to check if cv2.resize(...,interpolation=cv2.INTER_AREA) make an average of the colors of the cells
        """
        n = 9
        grid_colors = []
        #        grid_colors = np.zeros([self.grid_size.y, self.grid_size.x, 3], dtype=np.uint8)
        for _ in range(n):
            column = []
            for _ in range(n):
                colors = []
                for k in range(3):
                    colors.append(np.random.randint(256))
                column.append(colors)
            grid_colors.append(column)

        moy = []
        for a in range(3):
            col = []
            for b in range(3):
                colors = []
                colors.append(round(sum([grid_colors[i+3*a][j+3*b][0] for i in range(3) for j in range(3)]) / 9))
                colors.append(round(sum([grid_colors[i+3*a][j+3*b][1] for i in range(3) for j in range(3)]) / 9))
                colors.append(round(sum([grid_colors[i+3*a][j+3*b][2] for i in range(3) for j in range(3)]) / 9))
                col.append(colors)
            moy.append(col)
        image_blurred =  cv2.resize(np.array(grid_colors, dtype = np.uint8), (len(grid_colors[0]) // 3, len(grid_colors) // 3), interpolation=cv2.INTER_AREA)
        self.assertListEqual(image_blurred.tolist(), moy)

if __name__ == "__main__":
    unittest.main()


import numpy as np
import cv2
n = 9
grid_colors = []
for _ in range(n):
    column = []
    for _ in range(n):
        colors = []
        for k in range(3):
            colors.append(np.random.randint(256))
        column.append(colors)
    grid_colors.append(column)

moy = []
for a in range(3):
    col = []
    for b in range(3):
        colors = []
        colors.append(round(sum([grid_colors[i+3*a][j+3*b][0] for i in range(3) for j in range(3)]) / 9))
        colors.append(round(sum([grid_colors[i+3*a][j+3*b][1] for i in range(3) for j in range(3)]) / 9))
        colors.append(round(sum([grid_colors[i+3*a][j+3*b][2] for i in range(3) for j in range(3)]) / 9))
        col.append(colors)
    moy.append(col)

image_blurred =  cv2.resize(np.array(grid_colors, dtype = np.uint8), (len(grid_colors[0]) // 3, len(grid_colors) // 3), interpolation=cv2.INTER_AREA)
print(image_blurred)
print(grid_colors)
