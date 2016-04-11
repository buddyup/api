from django.test import TestCase


class SampleTest(TestCase):
    # def test_addition(self):
    #     self.assertEquals(1 + 1, 3)

    def test_addition_right(self):
        self.assertEquals(1 + 1, 2)

    # def test_addition_raise(self):
    #     raise Exception
    #     self.assertEquals(1 + 1 ,2)
