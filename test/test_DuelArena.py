import unittest
from random import Random
from typing import Sequence
from unittest import TestCase

from cogs.duel.DuelArena import DuelArena, DuelResult, DuelStatus


class AlwaysFirstRandom(Random):
    def choice(self, seq: Sequence):
        return seq[0]


class AlwaysSecondRandom(Random):
    def choice(self, seq: Sequence):
        return seq[1]


class TestDuelArena(TestCase):

    def test_should_add_duel(self):
        arena = DuelArena(AlwaysFirstRandom())
        duel_result = arena.add_or_make_duel(server_id="1", challenger="a", prise=1, target="b")
        self.assertEqual(duel_result.status, DuelStatus.DUEL_CREATED)

    def test_should_make_duel(self):
        arena = DuelArena(AlwaysFirstRandom())
        challenger = "a"
        target = "b"
        prise = 1
        arena.add_or_make_duel(server_id="1", challenger=challenger, prise=prise, target=target)
        duel_result = arena.add_or_make_duel(server_id="1", challenger=target, prise=prise, target=challenger)
        self.assertEqual(duel_result.status, DuelStatus.CHALLENGER_WON)
        self.assertEqual(duel_result.prise, prise)

    def test_not_make_duel_twice(self):
        arena = DuelArena(AlwaysSecondRandom())
        challenger = "c"
        target = "d"
        prise = 1
        arena.add_or_make_duel(server_id="1", challenger=challenger, prise=prise, target=target)
        duel_result = arena.add_or_make_duel(server_id="1", challenger=challenger, prise=prise, target=target)
        self.assertEqual(duel_result.status, DuelStatus.DUEL_ALREADY_CREATED)


if __name__ == '__main__':
    unittest.main()
