import pytest
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from devp2p.rlp import (
    encode_rlp,
    decode_rlp,
)

@pytest.mark.parametrize(
    'value, expected',
    (
        ('b', 'b'),
        ('dog', ['\x83', 'd', 'o', 'g']), 
        (['cat', 'dog'], ['\xc8', '\x83', 'c', 'a', 't', '\x83', 'd', 'o', 'g']),
        ('', ['\x80']),
        ([], ['\xc0']),
        ('\x00', '\x00'),
        ('\x0f', '\x0f'),
        ('\x04\x00', ['\x82', '\x04', '\x00']),
        ([[], [[]], [ [], [[]] ] ], [ '\xc7', '\xc0', '\xc1', '\xc0', '\xc3', '\xc0', '\xc1', '\xc0' ]),
	# ("Lorem ipsum dolor sit amet, consectetur adipisicing elit", 
		# ['\xc7', '\x38', 'L', 'o', 'r', 'e', 'm'. ]),
    )
)
def test_encode_rlp(value, expected):
    encode_result = encode_rlp(value)
    assert encode_result == expected 


@pytest.mark.parametrize(
    'value, expected',
    (
	('b','b'),
        (['\x83', 'd', 'o', 'g'], 'dog'), 
        (['\xc8', '\x83', 'c', 'a', 't', '\x83', 'd', 'o', 'g'], ['cat', 'dog']),
	(['\x82', '\x04', '\x00'], '\x04\x00'),
        (['\x80'], ''),
	(['\xc0'], []),
        ('\x00', '\x00'),
        ('\x0f', '\x0f'),
    )
)
def test_decode_rlp(value, expected):
    decode_result = decode_rlp(value)
    assert decode_result == expected

## exception raising tests

