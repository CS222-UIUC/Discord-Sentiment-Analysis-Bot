"""Test File for Media Handler"""

#using sys to allow us to import our media_handler file for testing
import sys
sys.path.append("./course-project-group-38/media_handler")

import media_handler as mh #pylint: disable=C E

#Tests

def test_msg_to_lower():
    """Tests whether the message is correctly made into lowercase"""
    test_string = "Hello This TESTS if things get correctly ChAnGeD to @lowercase."
    correct_output = "hello this tests if things get correctly changed to @lowercase."
    test_string = mh.msg_to_lower(test_string)
    assert test_string == correct_output

def test_atsign_removed():
    """Tests whether we remove the @ symbol from passed in messages"""
    test_string = "Testing whether @ symbol is removed@ multiple places@"
    correct_output = "Testing whether   symbol is removed  multiple places "
    assert mh.remove_irrelevant_chars(test_string) == correct_output

def test_punctuation_removed():
    """Tests whether we remove punctutation & non relevant characters"""
    test_string = "Testing! whether, punctuation? and symbols &*(^ are removed."
    correct_output = "Testing  whether  punctuation  and symbols      are removed "
    assert mh.remove_irrelevant_chars(test_string) == correct_output

