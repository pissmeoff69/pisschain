from __future__ import annotations

from piss_rs import SpendBundle
from piss_rs.sized_ints import uint64

from piss._tests.util.get_name_puzzle_conditions import get_name_puzzle_conditions
from piss.consensus.cost_calculator import NPCResult
from piss.consensus.default_constants import DEFAULT_CONSTANTS
from piss.full_node.bundle_tools import simple_solution_generator
from piss.types.blockchain_format.program import INFINITE_COST
from piss.types.generator_types import BlockGenerator


def cost_of_spend_bundle(spend_bundle: SpendBundle) -> int:
    program: BlockGenerator = simple_solution_generator(spend_bundle)
    # always use the post soft-fork2 semantics
    npc_result: NPCResult = get_name_puzzle_conditions(
        program,
        INFINITE_COST,
        mempool_mode=True,
        height=DEFAULT_CONSTANTS.HARD_FORK_HEIGHT,
        constants=DEFAULT_CONSTANTS,
    )
    return uint64(0 if npc_result.conds is None else npc_result.conds.cost)
