# src/symbolic_engine.py
# Corrected symbolic regression engine using DEAP to rediscover Friedmann-like relations.

import math
import operator
import random
from functools import partial

import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM
from deap import base, creator, gp, tools, algorithms

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# -------------------------
# 1) Prepare dataset
# -------------------------
def prepare_dataset():
    df = pd.read_csv("data/processed/cosmology_data.csv")
    try:
        consts = pd.read_csv("data/processed/constants.csv").to_dict(orient="records")[0]
        H0_val = float(consts.get("H0_current", 70.0))
        Om0_val = float(consts.get("Omega_matter", 0.3))
        Omega_lambda = float(consts.get("Omega_lambda", 0.7))
    except Exception:
        H0_val = 70.0
        Om0_val = 0.3
        Omega_lambda = 0.7

    cosmo = FlatLambdaCDM(H0=H0_val, Om0=Om0_val)

    z = df["redshift_z"].values
    Hvals = np.array([cosmo.H(zz).value for zz in z])
    H2 = Hvals ** 2

    rho0_proxy = Om0_val
    rho_proxy = rho0_proxy * (1 + z) ** 3
    Lambda_proxy = np.full_like(z, Omega_lambda)

    X = np.vstack([rho_proxy, Lambda_proxy]).T
    y = H2
    return X, y, z


# -------------------------
# 2) Protected operations
# -------------------------
def protectedDiv(a, b):
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.where(np.abs(b) > 1e-12, a / b, 1.0)
    return c


def protectedLog(a):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(a > 0, np.log(a), 0.0)


def protectedSqrt(a):
    with np.errstate(invalid='ignore'):
        return np.where(a >= 0, np.sqrt(a), 0.0)


# -------------------------
# 3) Setup DEAP GP toolbox
# -------------------------
def setup_gp():
    pset = gp.PrimitiveSet("MAIN", 2)
    pset.renameArguments(ARG0="rho")
    pset.renameArguments(ARG1="Lambda")

    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addPrimitive(protectedDiv, 2)
    pset.addPrimitive(operator.neg, 1)

    pset.addPrimitive(protectedLog, 1)
    pset.addPrimitive(protectedSqrt, 1)
    pset.addPrimitive(np.sin, 1)
    pset.addPrimitive(np.cos, 1)
    pset.addPrimitive(np.exp, 1)

    pset.addEphemeralConstant("rand101", partial(random.uniform, -10, 10))

    if not hasattr(creator, "FitnessMin"):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    if not hasattr(creator, "Individual"):
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("expr_init", gp.genHalfAndHalf, pset=pset, min_=1, max_=3)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)

    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

    return toolbox, pset


# -------------------------
# 4) Run symbolic regression
# -------------------------
def run_symbolic_regression(generations=20, pop_size=200):
    X, y, z = prepare_dataset()
    toolbox, pset = setup_gp()

    # Define evaluator that uses toolbox.compile (no recursion)
    def evaluate_individual(individual):
        func = toolbox.compile(expr=individual)
        try:
            y_pred = func(X[:, 0], X[:, 1])
            y_pred = np.array(y_pred, dtype=float).reshape(-1)
            rmse = np.sqrt(np.mean((y - y_pred) ** 2))
            if np.isnan(rmse) or np.isinf(rmse):
                return (1e6,)
            return (rmse,)
        except Exception:
            return (1e6,)

    toolbox.register("evaluate", evaluate_individual)

    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(5)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("std", np.std)

    pop, log = algorithms.eaSimple(
        pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=generations,
        stats=stats, halloffame=hof, verbose=True
    )
    return pop, log, hof, toolbox, pset, X, y, z


# -------------------------
# 5) Display results
# -------------------------
def print_results(hof, toolbox, X, y):
    print("\n=== Top discovered expressions ===")
    for i, ind in enumerate(hof):
        expr = gp.PrimitiveTree(ind)
        print(f"\nRank {i+1}:")
        print(expr)
        func = toolbox.compile(expr=ind)
        try:
            y_pred = func(X[:, 0], X[:, 1])
            y_pred = np.array(y_pred, dtype=float).reshape(-1)
            rmse = math.sqrt(np.mean((y - y_pred) ** 2))
            print(f"RMSE: {rmse:.6e}")
        except Exception as e:
            print("Evaluation error:", e)

    best = hof[0]
    best_func = toolbox.compile(expr=best)
    y_pred = np.array(best_func(X[:, 0], X[:, 1]), dtype=float).reshape(-1)
    print("\nSample comparison (first 10 rows):")
    print(" idx    target(H^2)       pred(H^2)")
    for i in range(min(10, len(y))):
        print(f"{i:3d} {y[i]:16.6e} {y_pred[i]:16.6e}")


# -------------------------
# 6) Main
# -------------------------
if __name__ == "__main__":
    print("Preparing data and running symbolic regression (this may take a few minutes)...")
    pop, log, hof, toolbox, pset, X, y, z = run_symbolic_regression(generations=18, pop_size=120)

    print_results(hof, toolbox, X, y)
    print("\nDone. Best expression above. You can now simplify it with SymPy if you wish.")
