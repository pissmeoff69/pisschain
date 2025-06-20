from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar, Optional, cast

import pytest
from piss_rs import BlockRecord, FullBlock
from piss_rs.sized_bytes import bytes32
from piss_rs.sized_ints import uint32

from piss._tests.blockchain.blockchain_test_utils import _validate_and_add_block
from piss._tests.util.blockchain import create_blockchain
from piss.consensus.augmented_chain import AugmentedBlockchain
from piss.simulator.block_tools import BlockTools
from piss.util.errors import Err


@dataclass
class NullBlockchain:
    if TYPE_CHECKING:
        from piss.consensus.blockchain_interface import BlocksProtocol

        _protocol_check: ClassVar[BlocksProtocol] = cast("NullBlockchain", None)

    added_blocks: set[bytes32] = field(default_factory=set)
    heights: dict[uint32, bytes32] = field(default_factory=dict)

    # BlocksProtocol
    async def lookup_block_generators(self, header_hash: bytes32, generator_refs: set[uint32]) -> dict[uint32, bytes]:
        raise ValueError(Err.GENERATOR_REF_HAS_NO_GENERATOR)  # pragma: no cover

    async def get_block_record_from_db(self, header_hash: bytes32) -> Optional[BlockRecord]:
        return None  # pragma: no cover

    def add_block_record(self, block_record: BlockRecord) -> None:
        self.added_blocks.add(block_record.header_hash)

    # BlockRecordsProtocol
    def try_block_record(self, header_hash: bytes32) -> Optional[BlockRecord]:
        return None  # pragma: no cover

    def block_record(self, header_hash: bytes32) -> BlockRecord:
        raise KeyError("no block records in NullBlockchain")  # pragma: no cover

    def height_to_block_record(self, height: uint32) -> BlockRecord:
        raise ValueError("Height is not in blockchain")

    def height_to_hash(self, height: uint32) -> Optional[bytes32]:
        return self.heights.get(height)

    def contains_block(self, header_hash: bytes32, height: uint32) -> bool:
        return False  # pragma: no cover

    def contains_height(self, height: uint32) -> bool:
        return height in self.heights.keys()

    async def prev_block_hash(self, header_hashes: list[bytes32]) -> list[bytes32]:
        raise KeyError("no block records in NullBlockchain")  # pragma: no cover


@dataclass
class FakeBlockRecord:
    height: uint32
    header_hash: bytes32
    prev_hash: bytes32


def BR(b: FullBlock) -> BlockRecord:
    ret = FakeBlockRecord(b.height, b.header_hash, b.prev_header_hash)
    return ret  # type: ignore[return-value]


@pytest.mark.anyio
@pytest.mark.limit_consensus_modes(reason="save time")
async def test_augmented_chain(default_10000_blocks: list[FullBlock]) -> None:
    blocks = default_10000_blocks
    # this test blockchain is expected to have block generators at these
    # heights:
    # 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
    # 24, 25, 26, 28

    null = NullBlockchain()
    abc = AugmentedBlockchain(null)

    # before adding anything to the augmented blockchain, make sure we just pass
    # through all requests
    with pytest.raises(ValueError, match="Height is not in blockchain"):
        abc.height_to_block_record(uint32(1))

    with pytest.raises(KeyError):
        abc.block_record(blocks[2].header_hash)

    with pytest.raises(KeyError):
        await abc.prev_block_hash([blocks[2].header_hash])

    with pytest.raises(ValueError, match="Err.GENERATOR_REF_HAS_NO_GENERATOR"):
        await abc.lookup_block_generators(blocks[3].header_hash, {uint32(3)})

    block_records = []

    # now add some blocks
    for b in blocks[:5]:
        block_records.append(BR(b))
        abc.add_extra_block(b, BR(b))

    assert abc.height_to_block_record(uint32(1)) == block_records[1]

    with pytest.raises(ValueError, match="Err.GENERATOR_REF_HAS_NO_GENERATOR"):
        await abc.lookup_block_generators(blocks[10].header_hash, {uint32(3), uint32(10)})

    # block 1 exists in the chain, but it doesn't have a generator
    with pytest.raises(ValueError, match="Err.GENERATOR_REF_HAS_NO_GENERATOR"):
        await abc.lookup_block_generators(blocks[1].header_hash, {uint32(1)})

    expect_gen = blocks[2].transactions_generator
    assert expect_gen is not None
    assert await abc.lookup_block_generators(blocks[5].prev_header_hash, {uint32(2)}) == {uint32(2): bytes(expect_gen)}

    for i in range(1, 5):
        assert await abc.prev_block_hash([blocks[i].header_hash]) == [blocks[i - 1].header_hash]

    for i in range(5):
        assert abc.block_record(blocks[i].header_hash) == block_records[i]
        assert abc.try_block_record(blocks[i].header_hash) == block_records[i]
        assert abc.height_to_hash(uint32(i)) == blocks[i].header_hash
        assert await abc.prev_block_hash([blocks[i].header_hash]) == [blocks[i].prev_header_hash]
        assert abc.try_block_record(blocks[i].header_hash) is not None
        assert await abc.get_block_record_from_db(blocks[i].header_hash) == block_records[i]
        assert abc.contains_height(uint32(i))

    for i in range(5, 10):
        assert abc.height_to_hash(uint32(i)) is None
        assert abc.try_block_record(blocks[i].header_hash) is None
        assert not await abc.get_block_record_from_db(blocks[i].header_hash)
        assert not abc.contains_height(uint32(i))

    assert abc.height_to_hash(uint32(5)) is None
    null.heights = {uint32(5): blocks[5].header_hash}
    assert abc.height_to_hash(uint32(5)) == blocks[5].header_hash

    # if we add blocks to cache that are already augmented into the chain, the
    # augmented blocks should be removed
    assert len(abc._extra_blocks) == 5
    for b in blocks[:5]:
        abc.add_block_record(BR(b))
    assert len(abc._extra_blocks) == 0
    assert null.added_blocks == {br.header_hash for br in blocks[:5]}


@pytest.mark.anyio
@pytest.mark.limit_consensus_modes(reason="save time")
async def test_augmented_chain_contains_block(default_10000_blocks: list[FullBlock], bt: BlockTools) -> None:
    blocks = default_10000_blocks[:50]
    async with create_blockchain(bt.constants, 2) as (b1, _):
        async with create_blockchain(bt.constants, 2) as (b2, _):
            for block in blocks:
                await _validate_and_add_block(b1, block)
                await _validate_and_add_block(b2, block)

            new_blocks = bt.get_consecutive_blocks(10, block_list_input=blocks)[50:]
            abc = AugmentedBlockchain(b1)
            for block in new_blocks:
                await _validate_and_add_block(b2, block)
                block_rec = b2.block_record(block.header_hash)
                abc.add_extra_block(block, block_rec)

            for block in blocks:
                # check underlying contains block but augmented does not
                assert abc.contains_block(block.header_hash, block.height) is True
                assert block.height not in abc._height_to_hash

            for block in new_blocks:
                # check augmented contains block but augmented does not
                assert abc.contains_block(block.header_hash, block.height) is True
                assert not abc._underlying.contains_height(block.height)

            for block in new_blocks:
                await _validate_and_add_block(b1, block)

            for block in new_blocks:
                # check underlying contains block
                assert abc._underlying.height_to_hash(block.height) == block.header_hash
                # check augmented contains block
                assert abc._height_to_hash[block.height] == block.header_hash

            abc.remove_extra_block(new_blocks[-1].header_hash)

            # check blocks removed from augmented
            for block in new_blocks:
                # check underlying contains block
                assert abc._underlying.height_to_hash(block.height) == block.header_hash
                # check augmented contains block
                assert block.height not in abc._height_to_hash
