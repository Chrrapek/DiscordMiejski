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
    challenger = "a"
    target = "b"
    prize = 1

    def test_should_add_duel(self):
        arena = DuelArena(AlwaysFirstRandom())
        duel_result = arena.add_or_make_duel("1", challenger=self.challenger, prize=self.prize, target=self.target)
        self.assertEqual(duel_result.status, DuelStatus.DUEL_CREATED)

    def test_should_make_duel(self):
        arena = DuelArena(AlwaysFirstRandom())
        arena.add_or_make_duel("1", challenger=self.challenger, prize=self.prize, target=self.target)
        duel_result = arena.add_or_make_duel("1", challenger=self.target, prize=self.prize, target=self.challenger)
        self.assertEqual(duel_result.status, DuelStatus.CHALLENGER_WON)
        self.assertEqual(duel_result.prize, self.prize)

    def test_not_make_duel_twice(self):
        arena = DuelArena(AlwaysSecondRandom())
        arena.add_or_make_duel("1", challenger=self.challenger, prize=self.prize, target=self.target)
        duel_result = arena.add_or_make_duel("1", challenger=self.challenger, prize=self.prize, target=self.target)
        self.assertEqual(duel_result.status, DuelStatus.DUEL_ALREADY_CREATED)

    def test_should_add_duel_after_previous_id_resolved(self):
        arena = DuelArena(AlwaysSecondRandom())
        arena.add_or_make_duel("1", challenger=self.challenger, prize=self.prize, target=self.target)
        arena.add_or_make_duel("1", challenger=self.target, prize=self.prize, target=self.challenger)
        duel_result = arena.add_or_make_duel("1", challenger=self.challenger, prize=self.prize, target=self.target)
        self.assertEqual(duel_result.status, DuelStatus.DUEL_CREATED)

    def test_target_should_not_be_challenger(self):
        arena = DuelArena(AlwaysSecondRandom())
        duel_result = arena.add_or_make_duel("1", challenger=self.challenger, prize=self.prize, target=self.challenger)
        self.assertEqual(duel_result.status, DuelStatus.CANNOT_DUEL_WITH_YOURSELF)

    def test_should_take_prize_from_proposal(self):
        arena = DuelArena(AlwaysFirstRandom())
        arena.add_or_make_duel("1", challenger=self.challenger, prize=self.prize, target=self.target)
        duel_result = arena.add_or_make_duel("1", challenger=self.target, prize=self.prize + 1, target=self.challenger)
        self.assertEqual(duel_result.prize, self.prize)

    def test_should_list_user_duels(self):
        arena = DuelArena(AlwaysFirstRandom())
        arena.add_or_make_duel("1", challenger=self.challenger, prize=self.prize, target=self.target)
        self.assertEqual(arena.list_user_open_duels_rivals("1", self.challenger), [self.target])
        self.assertEqual(arena.list_user_waiting_duels_rivals("1", self.target), [self.challenger])


if __name__ == '__main__':
    unittest.main()
