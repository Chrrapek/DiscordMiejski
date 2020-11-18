from enum import Enum
from random import Random
from typing import List, Dict


class DuelStatus(Enum):
    DUEL_CREATED = 1
    CHALLENGER_WON = 2
    TARGET_WON = 3
    DUEL_ALREADY_CREATED = 4


class DuelResult:
    def __init__(self, status: DuelStatus, prise: int):
        self.status: DuelStatus = status
        self.prise: int = prise


class DuelProposal:
    def __init__(self, challenger: str, target: str, prise: int):
        self.challenger: str = target
        self.prise: int = prise


class ServerDuels:
    open_duels: Dict[str, List[DuelProposal]] = {}


class DuelArena:

    def __init__(self, random: Random):
        self.random = random

    open_duels: Dict[str, ServerDuels] = {}

    def add_or_make_duel(self, server_id: str, challenger: str, prise: int, target: str) -> DuelResult:
        if self.reverse_proposal_exists(server_id, challenger, target):
            pass
        return DuelResult(status=DuelStatus.DUEL_CREATED, prise=prise)

    def reverse_proposal_exists(self, server_id, challenger, target) -> bool:
        if server_id in self.open_duels:
            server_duel_proposals: ServerDuels = self.open_duels[server_id]
            # if

        pass
