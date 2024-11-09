

from unittest import TestCase

from pynocchio.utility import (convert_string_to_boolean, file_exist,
                               get_base_name, get_dir_name, get_file_extension,
                               get_parent_path, is_dir, join_path, path_exist)


class TestUtility(TestCase):

    def setUp(self):
        TestCase.setUp(self)

    def test_get_file_extension(self):
        self.assertEqual(get_file_extension('myfile.zip'), '.zip')
        self.assertEqual(get_file_extension('myfile'), '')

    def test_get_dir_name(self):
        self.assertEqual(get_dir_name('/home/user/myfile.zip'), '/home/user')
        self.assertEqual(get_dir_name('myfile'), '')

    def test_get_base_name(self):
        self.assertEqual(get_base_name('/home/user/myfile.zip'), 'myfile.zip')
        self.assertEqual(get_base_name('/home/user/myfile'), 'myfile')

    def test_get_parent_path(self):
        self.assertEqual(get_parent_path('/home/user/myfile.zip'), '/home')
        self.assertEqual(get_parent_path('/home/user/myfile'), '/home')

    def test_join_path(self):
        self.assertEqual(join_path('/home', 'user', 'myfile.zip'),
                         '/home/user/myfile.zip')
        self.assertEqual(join_path('/home', 'user', 'myfile'),
                         '/home/user/myfile')

    def test_path_exist(self):
        self.assertTrue(path_exist('/home'))
        self.assertFalse(path_exist('/foo'))

    def test_file_exist(self):
        self.assertTrue(file_exist('LICENSE'))
        self.assertFalse(file_exist('foo.py'))

    def test_is_dir(self):
        self.assertTrue(is_dir('/home'))
        self.assertFalse(is_dir('LICENSE'))

    def test_convert_string_to_boolean(self):
        self.assertTrue(convert_string_to_boolean('True'))
        self.assertFalse(convert_string_to_boolean('False'))
        self.assertRaises(ValueError, convert_string_to_boolean, 'true')
