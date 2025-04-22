import tkinter as tk
from tkinter import ttk
import time
import random
import threading
import heapq


def threaded(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper


class AlgorithmVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Visualizer")
        self.root.geometry("700x800")
        self.title_label = tk.Label(
            root, text="Select Algorithm to Visualize", font=("Arial", 16)
        )
        self.title_label.pack(pady=10)
        self.algo_type_label = tk.Label(
            root, text="Choose Algorithm Type:", font=("Arial", 12)
        )
        self.algo_type_label.pack()
        self.algo_type = ttk.Combobox(root, values=["Sorting", "Graph Traversal"])
        self.algo_type.pack(pady=5)
        self.algo_type.bind("<<ComboboxSelected>>", self.update_algorithm_list)
        self.algo_label = tk.Label(
            root, text="Choose Specific Algorithm:", font=("Arial", 12)
        )
        self.algo_label.pack()
        self.algorithm = ttk.Combobox(root, values=[])
        self.algorithm.pack(pady=5)
        self.run_button = tk.Button(
            root, text="Run Visualization", command=self.run_visualization
        )
        self.run_button.pack(pady=20)
        self.speed_scale = tk.Scale(
            root,
            from_=0.1,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            label="Visualization Speed",
        )
        self.speed_scale.set(1.0)
        self.speed_scale.pack(pady=10)

        self.canvas = tk.Canvas(root, width=600, height=350, bg="white")
        self.canvas.pack(pady=10)

        self.status_label = tk.Label(root, text="", font=("Arial", 10), fg="blue")
        self.status_label.pack()

    def update_algorithm_list(self, event):
        self.algorithm.set("")
        algo_type = self.algo_type.get()
        if algo_type == "Sorting":
            self.algorithm["values"] = [
                "Bubble Sort",
                "Selection Sort",
                "Quick Sort",
            ]
        elif algo_type == "Graph Traversal":
            self.algorithm["values"] = [
                "Breadth-First Search (BFS)",
                "Dijkstra's Algorithm",
                "Prim's Algorithm",
            ]
        else:
            self.algorithm["values"] = []

    @threaded
    def run_visualization(self):
        algo_type = self.algo_type.get()
        algo_name = self.algorithm.get()

        if algo_type == "Sorting":
            if algo_name == "Bubble Sort":
                self.visualize_bubble_sort()
            elif algo_name == "Selection Sort":
                self.visualize_selection_sort()
            elif algo_name == "Quick Sort":
                self.visualize_quick_sort()
            else:
                self.status_label.config(
                    text="Please select a valid sorting algorithm."
                )
        elif algo_type == "Graph Traversal":
            if algo_name == "Breadth-First Search (BFS)":
                self.visualize_bfs()
            elif algo_name == "Dijkstra's Algorithm":
                self.visualize_dijkstra()
            elif algo_name == "Prim's Algorithm":
                self.visualize_prim()
            else:
                self.status_label.config(
                    text="Please select a valid graph traversal algorithm."
                )
        else:
            self.status_label.config(text="Please select a valid algorithm type.")

    def visualize_bubble_sort(self):
        self.status_label.config(text="Running Bubble Sort Visualization...")
        array = [random.randint(10, 100) for _ in range(20)]
        self.run_sort_algorithm(array, self.bubble_sort)

    def bubble_sort(self, array, draw_array):
        n = len(array)
        for i in range(n):
            for j in range(0, n - i - 1):
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    draw_array(array, j, j + 1)
            self.status_label.config(text=f"Completed pass {i + 1} of {n - 1}")

    def visualize_selection_sort(self):
        self.status_label.config(text="Running Selection Sort Visualization...")
        array = [random.randint(10, 100) for _ in range(20)]
        self.run_sort_algorithm(array, self.selection_sort)

    def selection_sort(self, array, draw_array):
        for i in range(len(array)):
            min_idx = i
            for j in range(i + 1, len(array)):
                if array[j] < array[min_idx]:
                    min_idx = j
            array[i], array[min_idx] = array[min_idx], array[i]
            draw_array(array, i, min_idx)

    def visualize_quick_sort(self):
        self.status_label.config(text="Running Quick Sort Visualization...")
        array = [random.randint(10, 100) for _ in range(20)]
        self.run_sort_algorithm(array, self.quick_sort)

    def quick_sort(self, array, draw_array, low=0, high=None):
        if high is None:
            high = len(array) - 1

        if low < high:
            # Partition the array
            pivot_index = self.partition(array, low, high, draw_array)

            self.quick_sort(array, draw_array, low, pivot_index - 1)
            self.quick_sort(array, draw_array, pivot_index + 1, high)

    def partition(self, array, low, high, draw_array):
        pivot = array[high]
        i = low - 1

        self.status_label.config(text=f"Pivot selected: {pivot}")
        draw_array(array, pivot_index=high)

        for j in range(low, high):
            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
                draw_array(
                    array, highlighted_index1=i, highlighted_index2=j, pivot_index=high
                )

        array[i + 1], array[high] = array[high], array[i + 1]
        draw_array(
            array, highlighted_index1=i + 1, highlighted_index2=high, pivot_index=i + 1
        )

        self.status_label.config(text=f"Pivot {pivot} placed at position {i + 1}")
        time.sleep(self.speed_scale.get())
        return i + 1

    def run_sort_algorithm(self, array, sort_function):
        self.canvas.delete("all")

        def draw_array(
            array, highlighted_index1=None, highlighted_index2=None, pivot_index=None
        ):
            self.canvas.delete("all")
            bar_width = 20
            max_height = max(array) if array else 1

            for i, value in enumerate(array):
                x0 = i * bar_width
                y0 = 350 - (value / max_height) * 300
                x1 = x0 + bar_width
                y1 = 350

                if i == highlighted_index1 or i == highlighted_index2:
                    color = "red"
                elif i == pivot_index:
                    color = "purple"
                else:
                    color = "blue"

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
                self.canvas.create_text(
                    (x0 + x1) / 2, y0 - 10, text=str(value), font=("Arial", 10)
                )

            self.root.update_idletasks()
            time.sleep(self.speed_scale.get())

        sort_function(array, draw_array)
        self.status_label.config(text="Sorting Completed!")

    def visualize_bfs(self):
        self.status_label.config(text="Running BFS Visualization...")
        self.canvas.delete("all")
        grid_size = 5
        cell_size = 70
        grid = [[0] * grid_size for _ in range(grid_size)]
        start = (0, 0)
        goal = (grid_size - 1, grid_size - 1)
        grid[goal[0]][goal[1]] = 2

        def bfs(start):
            queue = [start]
            visited = set()
            while queue:
                x, y = queue.pop(0)
                if (x, y) == goal:
                    self.status_label.config(text="Goal reached!")
                    return
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < grid_size
                        and 0 <= ny < grid_size
                        and (nx, ny) not in visited
                    ):
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                        grid[nx][ny] = 1
                        draw_grid(visited, queue)

        def draw_grid(visited, queue):
            self.canvas.delete("all")
            for i in range(grid_size):
                for j in range(grid_size):
                    x0, y0 = j * cell_size, i * cell_size
                    x1, y1 = x0 + cell_size, y0 + cell_size
                    color = "white"
                    if (i, j) in visited:
                        color = "lightblue"
                    elif (i, j) in queue:
                        color = "orange"
                    if (i, j) == goal:
                        color = "green"
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill=color, outline="black"
                    )
            self.root.update_idletasks()
            time.sleep(self.speed_scale.get())

        bfs(start)
        self.status_label.config(text="BFS Completed")

    def visualize_dijkstra(self):
        self.status_label.config(text="Running Dijkstra's Algorithm...")
        self.canvas.delete("all")
        grid_size = 10
        cell_size = 35
        grid = [
            [random.randint(1, 10) for _ in range(grid_size)] for _ in range(grid_size)
        ]
        start = (0, 0)
        goal = (grid_size - 1, grid_size - 1)

        def dijkstra(start, goal):
            distances = {
                node: float("infinity")
                for row in range(grid_size)
                for node in [(row, col) for col in range(grid_size)]
            }
            distances[start] = 0
            visited = set()
            pq = [(0, start)]
            parents = {start: None}

            while pq:
                current_distance, current_node = heapq.heappop(pq)
                if current_node in visited:
                    continue

                visited.add(current_node)
                if current_node == goal:
                    reconstruct_path(parents, goal)
                    self.status_label.config(text="Dijkstra's Algorithm Completed!")
                    return

                x, y = current_node
                for dx, dy in [
                    (-1, 0),
                    (1, 0),
                    (0, -1),
                    (0, 1),
                ]:
                    neighbor = (x + dx, y + dy)
                    if 0 <= neighbor[0] < grid_size and 0 <= neighbor[1] < grid_size:
                        distance = current_distance + grid[neighbor[0]][neighbor[1]]
                        if distance < distances[neighbor]:
                            distances[neighbor] = distance
                            parents[neighbor] = current_node
                            heapq.heappush(pq, (distance, neighbor))
                draw_grid(visited, current_node, goal)

        def draw_grid(visited, current_node, goal):
            self.canvas.delete("all")
            for i in range(grid_size):
                for j in range(grid_size):
                    x0, y0 = j * cell_size, i * cell_size
                    x1, y1 = x0 + cell_size, y0 + cell_size
                    color = "white"
                    if (i, j) == start:
                        color = "yellow"
                    elif (i, j) == goal:
                        color = "green"
                    elif (i, j) in visited:
                        color = "lightblue"
                    elif (i, j) == current_node:
                        color = "orange"
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill=color, outline="black"
                    )
                    self.canvas.create_text(
                        x0 + cell_size // 2,
                        y0 + cell_size // 2,
                        text=str(grid[i][j]),
                        font=("Arial", 8),
                    )
            self.root.update_idletasks()
            time.sleep(self.speed_scale.get())

        def reconstruct_path(parents, goal):
            current = goal
            while current:
                x0, y0 = current[1] * cell_size, current[0] * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill="blue", outline="black"
                )
                current = parents.get(current)
                self.root.update_idletasks()
                time.sleep(self.speed_scale.get() / 2)

        dijkstra(start, goal)

    def visualize_prim(self):
        self.status_label.config(text="Running Prim's Algorithm...")
        self.canvas.delete("all")
        graph = {
            0: {1: 2, 2: 3},
            1: {0: 2, 3: 1, 4: 4},
            2: {0: 3, 4: 5},
            3: {1: 1, 4: 6},
            4: {1: 4, 2: 5, 3: 6},
        }
        node_positions = {
            0: (100, 100),
            1: (200, 50),
            2: (300, 100),
            3: (200, 200),
            4: (300, 200),
        }

        def draw_graph(mst_edges, current_edge=None, visited_nodes=set()):
            self.canvas.delete("all")
            for node, (x, y) in node_positions.items():
                color = "green" if node in visited_nodes else "white"
                self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color)
                self.canvas.create_text(x, y, text=str(node), font=("Arial", 12))
            for node, neighbors in graph.items():
                for neighbor, weight in neighbors.items():
                    x0, y0 = node_positions[node]
                    x1, y1 = node_positions[neighbor]
                    edge_color = "lightgray"
                    if (node, neighbor) in mst_edges or (neighbor, node) in mst_edges:
                        edge_color = "blue"
                    elif (node, neighbor) == current_edge or (
                        neighbor,
                        node,
                    ) == current_edge:
                        edge_color = "orange"
                    self.canvas.create_line(x0, y0, x1, y1, fill=edge_color, width=2)
                    self.canvas.create_text(
                        (x0 + x1) / 2,
                        (y0 + y1) / 2,
                        text=str(weight),
                        font=("Arial", 10),
                        fill="black",
                    )

            self.root.update_idletasks()
            time.sleep(self.speed_scale.get())

        def prim(start):
            visited_nodes = {start}
            edges = [(weight, start, to) for to, weight in graph[start].items()]
            heapq.heapify(edges)
            mst_edges = []
            while edges:
                weight, frm, to = heapq.heappop(edges)
                if to not in visited_nodes:
                    visited_nodes.add(to)
                    mst_edges.append((frm, to))
                    draw_graph(
                        mst_edges, current_edge=(frm, to), visited_nodes=visited_nodes
                    )
                    for next_to, next_weight in graph[to].items():
                        if next_to not in visited_nodes:
                            heapq.heappush(edges, (next_weight, to, next_to))

            self.status_label.config(text="Prim's Algorithm Completed!")

        prim(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmVisualizerApp(root)
    root.mainloop()
