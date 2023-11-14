import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox as messagebox
import re

class EdgeNode:
    def __init__(self, dest, weight):
        self.dest = dest
        self.weight = weight
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_edge(self, dest, weight):
        new_edge = EdgeNode(dest, weight)
        new_edge.next = self.head
        self.head = new_edge

def dijkstra(graph, source):
    distance = {node: float('inf') for node in graph}
    distance[source] = 0
    previous = {node: None for node in graph}

    unvisited = list(graph)

    while unvisited:
        current_node = min(unvisited, key=lambda node: distance[node])
        unvisited.remove(current_node)

        if current_node in graph:
            for neighbor, weight in graph[current_node].items():
                temp_distance = distance[current_node] + weight.get('weight', 0)
                if temp_distance < distance[neighbor]:
                    distance[neighbor] = temp_distance
                    previous[neighbor] = current_node

    return previous, distance

def validate_vertex(vertex):
    return re.match(r'^[a-zA-Z0-9]+$', vertex)

def validate_edge_weight(weight):
    try:
        weight = int(weight)
        return weight > 0
    except ValueError:
        return False

def is_valid_graph():
    try:
        V = int(entr_num_vertices.get())
        E = int(entr_num_edges.get())
    except ValueError:
        return False

    if V <= 0 or E <= 0:
        return False

    return True

def draw_graph():
    global G, pos, graph_drawn
    graph_drawn = False
    btn_compute["state"] = "disable"
    shortest_path_entry.configure(state="normal")
    shortest_path_entry.delete(0, tk.END)
    shortest_path_entry.configure(state="readonly")

       # Xóa đồ thị hiện tại nếu có
    if graph_drawn:
        plt.clf()
    # Kiểm tra số lượng đỉnh và cạnh đã nhập có đúng không
    try:
        V = int(entr_num_vertices.get())
        E = int(entr_num_edges.get())
    except ValueError:
        result_text.set("Lỗi: Số đỉnh hoặc số cạnh không hợp lệ.")
        return

    # Kiểm tra xem số lượng đỉnh và cạnh có khớp với dữ liệu nhập vào hay không
    edges_input = entr_edges.get().strip().split(',')
    actual_edges = sum(len(edge.split()) == 3 for edge in edges_input)

    if not is_valid_graph() or len(edges_input) != E or actual_edges != E:
        result_text.set("Lỗi: Vui lòng kiểm tra số đỉnh, số cạnh và dữ liệu đồ thị.")
        return

    # Kiểm tra số đỉnh
    actual_vertices = set()
    for edge_input in edges_input:
        edge_components = edge_input.split()
        actual_vertices.update(edge_components[:2])

    if len(actual_vertices) != V:
        result_text.set("Lỗi: Số đỉnh không khớp với dữ liệu đồ thị.")
        return

    # Tiếp tục với việc vẽ đồ thị như bình thường
    graph_drawn = False  # Đặt lại trạng thái vẽ
    source_node = entr_source.get().strip()
    end_node = entr_end.get().strip()

    if not source_node or not end_node:
        result_text.set("Lỗi: Vui lòng nhập đỉnh nguồn và đỉnh đích.")
        return

    G = nx.Graph()

    for edge_input in edges_input:
        edge_components = edge_input.split()
        if len(edge_components) != 3:
            result_text.set("Lỗi: Dữ liệu đầu vào không hợp lệ.")
            return

        u, v, weight = edge_components
        if not validate_vertex(u) or not validate_vertex(v) or not validate_edge_weight(weight):
            result_text.set("Lỗi: Đỉnh hoặc trọng số không hợp lệ.")
            return

        weight = int(weight)

        G.add_edge(u, v, weight=weight)

    pos = nx.spring_layout(G, seed=42)

    plt.clf()
    ax.set_axis_off()  # Tắt trục toạ độ
    nx.draw(
        G,
        pos=pos,
        with_labels=True,
        node_size=800,
        node_color='skyblue',
        font_size=12,
        font_color='black',
        edge_color='gray',
        arrows=False,
        width=1,
        style='dashed'
    )
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    canvas.draw()
    result_text.set("Đồ thị đã được vẽ.")
    graph_drawn = True  # Cập nhật trạng thái vẽ

    # Kích hoạt nút tính toán sau khi đã vẽ xong đồ thị
    btn_compute["state"] = "normal"

def compute_shortest_path():
    global G, pos

    source_node = entr_source.get()
    end_node = entr_end.get()

    if not source_node or not end_node:
        result_text.set("Lỗi: Vui lòng nhập đỉnh nguồn và đỉnh đích.")
        return

    if not graph_drawn:
        result_text.set("Lỗi: Vui lòng vẽ đồ thị trước khi tính toán.")
        return

    if source_node not in G:
        messagebox.showerror("Lỗi", f"Đỉnh nguồn '{source_node}' không tồn tại trong đồ thị.")
        return

    previous, distance = dijkstra(G, source_node)

    if end_node not in G:
        messagebox.showerror("Lỗi", f"Đỉnh đích '{end_node}' không tồn tại trong đồ thị.")
        return

    path_edges = []
    current_node = end_node

    while previous[current_node] is not None:
        parent_node = previous[current_node]
        path_edges.append((parent_node, current_node))
        current_node = parent_node

    path_edges.reverse()

    # Highlight the shortest path in red
    edge_colors = ['r' if (u, v) in path_edges or (v, u) in path_edges else 'gray' for u, v in G.edges()]

    nx.draw_networkx_edges(G, pos, edgelist=list(G.edges()), edge_color=edge_colors, width=2)

    canvas.draw()
    result_text.set("Tính toán hoàn tất.")
    display_shortest_distance(distance, end_node)

    # Update the shortest path Entry widget
    shortest_path = " -> ".join(path[0] for path in path_edges) + f" -> {end_node}"
    shortest_path_entry.configure(state="normal")
    shortest_path_entry.delete(0, tk.END)
    shortest_path_entry.insert(0, shortest_path)
    shortest_path_entry.configure(state="readonly")

def display_shortest_distance(distance, end_node):
    result_text.set(f"Khoảng cách ngắn nhất tới {end_node}: {distance[end_node]}")

# Tạo giao diện đồ thị
root = tk.Tk()
root.title("Ứng dụng Dijkstra")

frame_input = ttk.Frame(root)
frame_input.pack(padx=10, pady=10)

lbl_num_vertices = ttk.Label(frame_input, text="Số đỉnh của đồ thị:")
lbl_num_vertices.grid(row=0, column=0)

entr_num_vertices = ttk.Entry(frame_input)
entr_num_vertices.grid(row=0, column=1)

lbl_num_edges = ttk.Label(frame_input, text="Số cạnh của đồ thị:")
lbl_num_edges.grid(row=1, column=0)

entr_num_edges = ttk.Entry(frame_input)
entr_num_edges.grid(row=1, column=1)

lbl_edges = ttk.Label(frame_input, text="Cạnh và trọng số (đỉnh 1 đỉnh 2 trọng số, cách nhau bằng dấu phẩy):")
lbl_edges.grid(row=2, column=0)

entr_edges = ttk.Entry(frame_input)
entr_edges.grid(row=2, column=1)

lbl_source = ttk.Label(frame_input, text="Đỉnh nguồn:")
lbl_source.grid(row=3, column=0)

entr_source = ttk.Entry(frame_input)
entr_source.grid(row=3, column=1)

lbl_end = ttk.Label(frame_input, text="Đỉnh đích:")
lbl_end.grid(row=4, column=0)

entr_end = ttk.Entry(frame_input)
entr_end.grid(row=4, column=1)

btn_draw = ttk.Button(frame_input, text="Vẽ Đồ thị", command=draw_graph)
btn_draw.grid(row=5, column=0)

btn_compute = ttk.Button(frame_input, text="Tính Đường đi ngắn nhất", command=compute_shortest_path, state="disabled")
btn_compute.grid(row=5, column=1)

# Add a new Entry widget for displaying the shortest path
shortest_path_entry = ttk.Entry(frame_input, state="readonly", width=30)
shortest_path_entry.grid(row=5, column=2, padx=10)

result_text = tk.StringVar()
lbl_result = ttk.Label(frame_input, textvariable=result_text)
lbl_result.grid(row=6, columnspan=3)

figure, ax = plt.subplots()
ax.set_axis_off()
canvas = FigureCanvasTkAgg(figure, master=root)
canvas.get_tk_widget().pack()

graph_drawn = False

root.mainloop()
