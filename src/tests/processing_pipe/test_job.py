import unittest  # second tests
from src.core.processing_pipe.src.Job import Job


class JobTestCase(unittest.TestCase):

    def test_datetime_from_string(self):
        job = Job("", "", None, 0)
        iterator = job.fibonacci(14)
        fibonacci_lookup_table = [2, 3, 5, 8, 13]
        for i in range(5):
            try:
                self.assertEqual(fibonacci_lookup_table[i], next(iterator))
                continue
            except StopIteration:
                del iterator
                break

def suite():
    suite = unittest.TestSuite()
    suite.addTest(JobTestCase())

    return suite


if __name__ == '__main__':
    unittest.main()
