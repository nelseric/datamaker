from pathlib import Path

import datamaker.db as db

import pstats, cProfile

import pandas as pd

import datamaker.heuristic.should_buy as sb



def no_bm(path=Path(".")):
    historical = pd.HDFStore("fix.h5").fix
    sb.apply(historical, 0.0050, 0.0050, 14400)

def benchmark(path=Path(".")):
    historical = pd.HDFStore("fix.h5").fix

    cProfile.runctx("sb.apply(historical, 0.0050, 0.0050, 14400)", globals(), locals(), "Profile.prof")

    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("time").print_stats()




if __name__ == '__main__':
    # no_bm()
    benchmark()
