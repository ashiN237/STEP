import sys
import math
import random
from common import print_tour, read_input
from typing import List

# 2つの都市の座標から距離を計算する関数
def distance(city1: List[float], city2: List[float]) -> float:
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# 都市のリストを受け取り、ランダムな初期巡回路を生成する関数
def generate_initial_tour(cities: List[List[float]]) -> List[int]:
    tour = list(range(len(cities)))
    random.shuffle(tour)
    return tour

# 都市のリストと初期巡回路を受け取り、巡回路を改善する関数
def improve_tour(cities: List[List[float]], tour: List[int]) -> List[int]:
    N = len(cities)
    improved = True
    while improved:
        improved = False
        for i in range(N - 2):
            for j in range(i + 2, N):
                # 2つの隣接した辺を交換した場合の巡回路の距離を計算
                dist_current = (
                    distance(cities[tour[i]], cities[tour[i + 1]]) +
                    distance(cities[tour[j]], cities[tour[(j + 1) % N]])
                )
                dist_new = (
                    distance(cities[tour[i]], cities[tour[j]]) +
                    distance(cities[tour[i + 1]], cities[tour[(j + 1) % N]])
                )
                # 新しい巡回路の方が短い場合、辺を交換して巡回路を改善
                if dist_new < dist_current:
                    tour[i + 1: j + 1] = reversed(tour[i + 1: j + 1])
                    improved = True
    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])  # 入力ファイルから都市の座標を読み込む
    tour = generate_initial_tour(cities)  # 初期巡回路を生成
    improved_tour = improve_tour(cities, tour)  # 巡回路を改善
    print_tour(improved_tour)  # 改善された巡回路を出力
