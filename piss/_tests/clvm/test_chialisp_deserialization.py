from __future__ import annotations

import pytest
from piss_puzzles_py.programs import pissLISP_DESERIALISATION

from piss.types.blockchain_format.program import INFINITE_COST, Program
from piss.util.byte_types import hexstr_to_bytes

DESERIALIZE_MOD = Program.from_bytes(pissLISP_DESERIALISATION)


def serialized_atom_overflow(size):
    if size == 0:
        size_blob = b"\x80"
    elif size < 0x40:
        size_blob = bytes([0x80 | size])
    elif size < 0x2000:
        size_blob = bytes([0xC0 | (size >> 8), (size >> 0) & 0xFF])
    elif size < 0x100000:
        size_blob = bytes([0xE0 | (size >> 16), (size >> 8) & 0xFF, (size >> 0) & 0xFF])
    elif size < 0x8000000:
        size_blob = bytes(
            [
                0xF0 | (size >> 24),
                (size >> 16) & 0xFF,
                (size >> 8) & 0xFF,
                (size >> 0) & 0xFF,
            ]
        )
    elif size < 0x400000000:
        size_blob = bytes(
            [
                0xF8 | (size >> 32),
                (size >> 24) & 0xFF,
                (size >> 16) & 0xFF,
                (size >> 8) & 0xFF,
                (size >> 0) & 0xFF,
            ]
        )
    else:
        size_blob = bytes(
            [
                0xFC | ((size >> 40) & 0xFF),
                (size >> 32) & 0xFF,
                (size >> 24) & 0xFF,
                (size >> 16) & 0xFF,
                (size >> 8) & 0xFF,
                (size >> 0) & 0xFF,
            ]
        )
    extra_str = "01" * 1000
    return size_blob.hex() + extra_str


def test_deserialization_simple_list():
    # ("hello" "friend")
    b = hexstr_to_bytes("ff8568656c6c6fff86667269656e6480")
    cost, output = DESERIALIZE_MOD.run_with_cost(INFINITE_COST, [b])
    print(cost, output)
    prog = Program.to(output)
    assert prog == Program.from_bytes(b)


def test_deserialization_password_coin():
    # (i (= (sha256 2) (q 0x2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824)) (c (q 51) (c 5 (c (q 100) (q ())))) (q "wrong password"))  # noqa
    b = hexstr_to_bytes(
        "ff04ffff0affff0bff0280ffff01ffa02cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b98248080ffff05ffff01ff3380ffff05ff05ffff05ffff01ff6480ffff01ff8080808080ffff01ff8e77726f6e672070617373776f72648080"
    )
    cost, output = DESERIALIZE_MOD.run_with_cost(INFINITE_COST, [b])
    print(cost, output)
    prog = Program.to(output)
    assert prog == Program.from_bytes(b)


def test_deserialization_large_numbers():
    # '(99999999999999999999999999999999999999999999999999999999999999999 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF -99999999999999999999999999999999999999999999999999999999999999999999999999999)'  # noqa
    b = hexstr_to_bytes(
        "ff9c00f316271c7fc3908a8bef464e3945ef7a253609ffffffffffffffffffb00fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa1ff22ea0179500526edb610f148ec0c614155678491902d6000000000000000000180"
    )
    cost, output = DESERIALIZE_MOD.run_with_cost(INFINITE_COST, [b])
    print(cost, output)
    prog = Program.to(output)
    assert prog == Program.from_bytes(b)


def test_overflow_atoms():
    b = hexstr_to_bytes(serialized_atom_overflow(0xFFFFFFFF))
    with pytest.raises(Exception):
        _cost, _output = DESERIALIZE_MOD.run_with_cost(INFINITE_COST, [b])

    b = hexstr_to_bytes(serialized_atom_overflow(0x3FFFFFFFF))
    with pytest.raises(Exception):
        _cost, _output = DESERIALIZE_MOD.run_with_cost(INFINITE_COST, [b])

    b = hexstr_to_bytes(serialized_atom_overflow(0xFFFFFFFFFF))
    with pytest.raises(Exception):
        _cost, _output = DESERIALIZE_MOD.run_with_cost(INFINITE_COST, [b])

    b = hexstr_to_bytes(serialized_atom_overflow(0x1FFFFFFFFFF))
    with pytest.raises(Exception):
        _cost, _output = DESERIALIZE_MOD.run_with_cost(INFINITE_COST, [b])
