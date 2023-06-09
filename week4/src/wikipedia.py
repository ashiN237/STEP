import sys
import collections
from typing import Dict

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file: str, links_file: str) -> None:

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self) -> None:
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start: str, goal: str) -> None:
        # ページタイトルからページIDを取得
        for page_id, title in self.titles.items():
            if title == start:
                start_page_id = page_id
            if title == goal:
                goal_page_id = page_id

        # 幅優先探索で最短経路を見つける
        shortest_path = self.bfs(start_page_id, goal_page_id)
        if shortest_path:
            # ページIDからページタイトルに変換
            shortest_path_titles = [self.titles[page_id] for page_id in shortest_path]
            print("Shortest path found:", shortest_path_titles)
        else:
            print("No path found.")
        print()


    # BFSをdequeを用いて実装
    def bfs(self, start: int, goal: int) -> collections.deque:
        visited = set()  # 訪れたノードを記録する集合
        queue = collections.deque([[start]])  # キューを用いて探索するためのデータ構造を準備

        while queue:
            path = queue.popleft()  # キューから現在のパスを取り出す
            current_node = path[-1]  # パスの最後のノードが現在のノード

            if current_node == goal:  # 目標ノードに到達したらパスを返す
                return path

            if current_node not in visited:
                visited.add(current_node)
                neighbors = self.links[current_node]
                for neighbor in neighbors:  # 隣接ノードを順に探索
                    new_path = collections.deque(path)  # 現在のパスをコピー
                    new_path.append(neighbor)  # 隣接ノードをパスに追加
                    queue.append(new_path)  # キューに新しいパスを追加

                    if neighbor == goal:
                        return new_path

        return None


    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self) -> None:
        page_rank = {page_id: 1.0 for page_id in self.titles.keys()}
        page_rank = self.calculate_page_ranks(page_rank)

        # ページランクの収束の確認
        threshold = 0.0001  # 収束判定の閾値
        max_iterations = 100  # 最大繰り返し回数
        for i in range(max_iterations):
            new_page_rank = self.calculate_page_ranks(page_rank)
            diff = sum(abs(new_page_rank[page_id] - page_rank[page_id]) for page_id in self.titles.keys())
            if diff < threshold:
                page_rank = new_page_rank
                break
            page_rank = new_page_rank
        else:
            print("Page rank did not converge within the maximum number of iterations.")

        # 重要度の高いページトップ10を求める
        most_popular_pages = sorted(page_rank, key=page_rank.get, reverse=True)[:10]

        # 結果を表示
        print("The most popular pages are:")
        for page_id in most_popular_pages:
            print(self.titles[page_id], page_rank[page_id])
        print()


    # Calculate the page ranks
    def calculate_page_ranks(self, page_rank) -> Dict[int, float]:
        damping_factor = 0.85
        random_surfer_probability = 0.15

        new_page_rank = {page_id: 0.0 for page_id in self.titles.keys()}
        for page_id, links in self.links.items():
            if links:
                for link in links:
                    new_page_rank[link] += damping_factor * page_rank[page_id] / len(links)
                random_surfer_page_rank = random_surfer_probability * page_rank[page_id] / len(self.titles)
                for page_id_2 in self.titles.keys():
                    new_page_rank[page_id_2] += random_surfer_page_rank         
            else:
                for page_id_2 in self.titles.keys():
                    new_page_rank[page_id_2] += page_rank[page_id] / len(self.titles)
        return new_page_rank


    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # wikipedia.find_longest_titles()
    # wikipedia.find_most_linked_pages()
    # wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()