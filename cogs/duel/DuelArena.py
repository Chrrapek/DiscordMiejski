from enum import Enum
from random import Random
from typing import Dict


class DuelStatus(Enum):
    DUEL_CREATED = 1
    CHALLENGER_WON = 2
    TARGET_WON = 3
    DUEL_ALREADY_CREATED = 4
    CANNOT_DUEL_WITH_YOURSELF = 5


class DuelResult:
    def __init__(self, status: DuelStatus, prise: int = None):
        self.status: DuelStatus = status
        self.prise: int = prise


class DuelProposal:
    def __init__(self, target: str, prise: int):
        self.target: str = target
        self.prise: int = prise


class ServerDuels:
    def __init__(self):
        self.open_duels: Dict[str, Dict[str, DuelProposal]] = {}

    def add_proposal(self, challenger: str, proposal: DuelProposal):
        if challenger not in self.open_duels:
            self.open_duels[challenger] = {}
        self.open_duels[challenger][proposal.target] = proposal


class DuelArena:

    def __init__(self, random: Random):
        self.random = random
        self.open_duels: Dict[str, ServerDuels] = {}

    def add_or_make_duel(self, server_id: str, challenger: str, prise: int, target: str) -> DuelResult:
        if challenger == target:
            return DuelResult(DuelStatus.CANNOT_DUEL_WITH_YOURSELF)
        if self.proposal_exists(server_id, challenger, target):
            return DuelResult(status=DuelStatus.DUEL_ALREADY_CREATED, prise=prise)
        if self.reverse_proposal_exists(server_id, challenger, target):
            proposal = self.open_duels[server_id].open_duels[target][challenger]
            self.open_duels[server_id].open_duels[target].pop(challenger)
            winner = self.random.choice([challenger, target])
            if winner == challenger:
                return DuelResult(status=DuelStatus.CHALLENGER_WON, prise=proposal.prise)
            else:
                return DuelResult(status=DuelStatus.TARGET_WON, prise=proposal.prise)
        if server_id not in self.open_duels:
            self.open_duels[server_id] = ServerDuels()
        self.open_duels[server_id].add_proposal(challenger=challenger,
                                                proposal=DuelProposal(target=target, prise=prise))
        return DuelResult(status=DuelStatus.DUEL_CREATED, prise=prise)

    def proposal_exists(self, server_id: str, challenger: str, target: str):
        if server_id in self.open_duels:
            server_duel_proposals: ServerDuels = self.open_duels[server_id]
            if challenger in server_duel_proposals.open_duels:
                if target in server_duel_proposals.open_duels[challenger]:
                    return True
        else:
            return False

    def reverse_proposal_exists(self, server_id, challenger, target) -> bool:
        return self.proposal_exists(server_id, challenger=target, target=challenger)
