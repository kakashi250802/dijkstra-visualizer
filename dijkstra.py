import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox as messagebox
import re

def dijkstra(graph, source):
    distance = {node: float('inf') for node in graph}
    distance[source] = 0
    previous = {node: None for node in graph}

    unvisited = list(graph)

    while unvisited:
        current_node = min(unvisited, key=lambda node: distance[node])
        unvisited.remove(current_node)

        for neighbor in graph[current_node]:
            if neighbor not in graph:
                print(f"Lỗi: Đỉnh {neighbor} không tồn tại trong đồ thị.")
                return None, None

            temp_distance = distance[current_node] + graph[current_node][neighbor]['weight']
            if temp_distance < distance[neighbor]:
                distance[neighbor] = temp_distance
                previous[neighbor] = current_node

    return previous, distance

def display_shortest_distance(distance, end_node):
    if distance[end_node] == float('inf'):
        messagebox.showinfo("Khoảng cách Ngắn nhất", f"Không có đường từ đỉnh nguồn đến đỉnh cuối {end_node}.")
    else:
        messagebox.showinfo("Khoảng cách Ngắn nhất", f"Khoảng cách ngắn nhất từ đỉnh nguồn đến đỉnh cuối {end_node}: {distance[end_node]}")

def validate_vertex(vertex):
    # Sử dụng biểu thức chính quy để kiểm tra xem đỉnh có hợp lệ hay không
    # Cho phép chữ cái (in hoa hoặc in thường) và chữ số
    return re.match(r'^[a-zA-Z0-9]+$', vertex)

def validate_edge_weight(weight):
    # Kiểm tra xem trọng số có là một số không âm hay không
    try:
        weight = int(weight)
        return weight > 0
    except ValueError:
        return False

def draw_graph():
    global G, pos
    G = nx.DiGraph()

    try:
        V = int(entr_num_vertices.get())
        E = int(entr_num_edges.get())
    except ValueError:
        result_text.set("Lỗi: Số đỉnh hoặc số cạnh không hợp lệ.")
        return

    for _ in range(E):
        edge_input = entr_edges.get().strip()
        edge_data = edge_input.split(',')
        for edge_pair in edge_data:
            edge_components = edge_pair.split()
            if len(edge_components) != 3:
                result_text.set("Lỗi: Dữ liệu đầu vào không hợp lệ.")
                return

            u, v, weight = edge_components
            if not validate_vertex(u) or not validate_vertex(v) or not validate_edge_weight(weight):
                result_text.set("Lỗi: Đỉnh hoặc trọng số không hợp lệ.")
                return

            weight = int(weight)

            if u not in G:
                G.add_node(u)
            if v not in G:
                G.add_node(v)

            G.add_edge(u, v, weight=weight)

    pos = nx.spring_layout(G, seed=42)

    plt.clf()
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=12)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    canvas.draw()
    result_text.set("Đồ thị đã được vẽ.")

def compute_shortest_path():
    source_node = entr_source.get()
    end_node = entr_end.get()

    if source_node not in G.nodes:
        messagebox.showerror("Lỗi", f"Đỉnh nguồn '{source_node}' không tồn tại trong đồ thị.")
        return

    previous, distance = dijkstra(G, source_node)

    if previous is not None and distance is not None:
        if end_node not in G.nodes:
            messagebox.showerror("Lỗi", f"Đỉnh đích '{end_node}' không tồn tại trong đồ thị.")
            return

        path_edges = []
        current_node = end_node

        while previous[current_node] is not None:
            parent_node = previous[current_node]
            path_edges.append((parent_node, current_node))
            current_node = parent_node

        path_edges.reverse()

        edge_colors = ['r' if edge in path_edges else 'gray' for edge in G.edges]
        nx.draw_networkx_edges(G, pos, edgelist=list(G.edges), edge_color=edge_colors, width=2)

        canvas.draw()
        result_text.set("Tính toán hoàn tất.")
        display_shortest_distance(distance, end_node)

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

btn_compute = ttk.Button(frame_input, text="Tính Đường đi ngắn nhất", command=compute_shortest_path)
btn_compute.grid(row=5, column=1)

result_text = tk.StringVar()
lbl_result = ttk.Label(frame_input, textvariable=result_text)
lbl_result.grid(row=6, columnspan=2)

figure, ax = plt.subplots()
canvas = FigureCanvasTkAgg(figure, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
