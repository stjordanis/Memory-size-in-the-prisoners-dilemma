import unittest

import axelrod as axl
import numpy as np

import opt_mo

turns, repetitions, params = 100, 5, [1, 1, 1]


def test_against_defector():
    opponent = [(0, 0, 0, 0)]
    pattern_1 = [0 for _ in range(9)]
    pattern_2 = [1 for _ in range(9)]

    obj_1 = opt_mo.objective_score(
        pattern=pattern_1,
        turns=turns,
        repetitions=repetitions,
        opponents=opponent,
        params=params,
    )
    obj_2 = opt_mo.objective_score(
        pattern=pattern_2,
        turns=turns,
        repetitions=repetitions,
        opponents=opponent,
        params=params,
    )
    assert np.isclose(abs(obj_1), 1.04)
    assert np.isclose(abs(obj_2), 0.03)


def test_against_cooperator():
    opponent = [(1, 1, 1, 1)]
    pattern_1 = [0 for _ in range(9)]
    pattern_2 = [1 for _ in range(9)]

    obj_1 = opt_mo.objective_score(
        pattern=pattern_1,
        turns=turns,
        repetitions=repetitions,
        opponents=opponent,
        params=params,
    )
    obj_2 = opt_mo.objective_score(
        pattern=pattern_2,
        turns=turns,
        repetitions=repetitions,
        opponents=opponent,
        params=params,
    )
    assert np.isclose(abs(obj_1), 5)
    assert np.isclose(abs(obj_2), 3)


def test_against_tit_for_tat():
    opponent = [(1, 0, 1, 0)]
    pattern_1 = [0 for _ in range(9)]
    pattern_2 = [1 for _ in range(9)]

    obj_1 = opt_mo.objective_score(
        pattern=pattern_1,
        turns=turns,
        repetitions=repetitions,
        opponents=opponent,
        params=params,
    )
    obj_2 = opt_mo.objective_score(
        pattern=pattern_2,
        turns=turns,
        repetitions=repetitions,
        opponents=opponent,
        params=params,
    )
    assert np.isclose(abs(obj_1), 1.04)
    assert np.isclose(abs(obj_2), 3)


def test_example_one():
    params = [1, 1, 1]
    assert opt_mo.pattern_size(params) == 8


def test_example_two():
    params = [1, 1, 2]
    assert opt_mo.pattern_size(params) == 16


def test_bayesian_gambler():
    opponents = [[0, 0, 0, 0], [1, 1, 1, 1]]
    turns, repetitions = 10, 2
    axl.seed(0)
    x, fun = opt_mo.train_gambler(
        method="bayesian",
        opponents=opponents,
        turns=turns,
        repetitions=repetitions,
        params=[1, 1, 2],
        method_params={"n_random_starts": 10, "n_calls": 15},
    )

    assert len(x) == opt_mo.pattern_size([1, 1, 2]) + 1
    assert np.isclose(fun, 2.9, atol=10 ** -1)


def test_differential_gambler():
    opponents = [[0, 0, 0, 0], [1, 1, 1, 1]]
    turns, repetitions = 10, 2
    axl.seed(0)
    x, fun = opt_mo.train_gambler(
        method="differential",
        opponents=opponents,
        turns=turns,
        repetitions=repetitions,
        params=[0, 0, 1],
        method_params={"popsize": 5},
    )

    assert len(x) == opt_mo.pattern_size([0, 0, 1]) + 1
    assert np.isclose(fun, 3.2, atol=10 ** -1)


def test_bayesian_mem_one():
    opponents = [[0, 0, 0, 0], [1, 1, 1, 1]]
    turns, repetitions = 200, 5
    axl.seed(0)
    x, theor, simul = opt_mo.optimal_memory_one(
        method="differential",
        opponents=opponents,
        turns=turns,
        repetitions=repetitions,
        method_params={"popsize": 100},
    )

    assert len(x) == 4
    assert np.isclose(theor, 3.0, atol=10 ** -2)
    assert np.isclose(simul, theor, atol=10 ** -2)


def test_differential_mem_one():
    opponents = [[0, 0, 0, 0], [1, 1, 1, 1]]
    turns, repetitions = 200, 5
    axl.seed(0)
    x, theor, simul = opt_mo.optimal_memory_one(
        method="bayesian",
        opponents=opponents,
        turns=turns,
        repetitions=repetitions,
        method_params={"n_random_starts": 20, "n_calls": 40},
    )

    assert len(x) == 4
    assert np.isclose(theor, 3.0, atol=10 ** -2)
    assert np.isclose(simul, theor, atol=10 ** -1)
