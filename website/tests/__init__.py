import pytest
import os

def test_ceneo():
    test_dir_path = os.path.split(__file__)[0]
    ceneo_test_path = os.path.join(test_dir_path, 'test_ceneobrowser.py')
    pytest.main(['-qs', ceneo_test_path])