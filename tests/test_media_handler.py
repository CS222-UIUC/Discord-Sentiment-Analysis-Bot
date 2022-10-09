"""Test File for Media Handler"""

#using sys to allow us to import our media_handler file for testing
import sys
sys.path.append("/home/afif/course-project-group-38/media_handler")

import media_handler as mh #pylint: disable=C0413

#Tests

def test_atsign_removed():
    """Tests whether we remove the @ symbol from passed in messages"""
    test_string = "Testing whether @ symbol is removed@ multiple places@"
    correct_output = "Testing whether  symbol is removed multiple places "
    assert mh.remove_irrelevant(test_string) == correct_output
