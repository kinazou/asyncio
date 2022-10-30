import unittest
import option

class OptionTest(unittest.TestCase):

    def test_get(self):
        args = option.get(5, 'input.csv', 'output.log', 'statistics.log')
        self.assertEqual(args.maxqueuesize, 5)

if __name__ == '__main__':
        unittest.main()
