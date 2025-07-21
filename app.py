import streamlit as st
from segment_tree import SegmentTree
import graphviz

st.set_page_config(layout="centered")
st.title("📊 Segment Tree Visualizer (Python + Streamlit)")

if 'data' not in st.session_state:
    st.session_state.data = []
if 'tree' not in st.session_state:
    st.session_state.tree = None


def draw_tree(node, l, r, depth=0):
    label = f"[{l},{r}]\\n{st.session_state.tree.tree[node]}"
    graph.node(str(node), label)
    if l == r:
        return
    mid = (l + r) // 2
    left = 2 * node + 1
    right = 2 * node + 2
    graph.edge(str(node), str(left))
    graph.edge(str(node), str(right))
    draw_tree(left, l, mid, depth + 1)
    draw_tree(right, mid + 1, r, depth + 1)


with st.form("build_form"):
    user_input = st.text_input("Enter array (comma-separated):", "1, 3, 5, 7, 9")
    build = st.form_submit_button("Build Tree")
    if build:
        try:
            st.session_state.data = list(map(int, user_input.split(",")))
            st.session_state.tree = SegmentTree(st.session_state.data)
            st.success("Segment Tree Built Successfully!")
        except:
            st.error("Invalid input! Use only integers separated by commas.")

if st.session_state.tree:
    st.subheader("Segment Tree Structure")
    graph = graphviz.Digraph(format='png')
    draw_tree(0, 0, len(st.session_state.data) - 1)
    st.graphviz_chart(graph)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Range Query")
        l = st.number_input("Left index", 0, len(st.session_state.data) - 1)
        r = st.number_input("Right index", 0, len(st.session_state.data) - 1, value=len(st.session_state.data) - 1)
        if st.button("Query Sum"):
            if l > r:
                st.error("Left index should be ≤ Right index.")
            else:
                res = st.session_state.tree.range_query(l, r)
                st.success(f"Sum in range [{l}, {r}] = {res}")

    with col2:
        st.subheader("Range Update (+val)")
        ul = st.number_input("Update Left", 0, len(st.session_state.data) - 1, key="ul")
        ur = st.number_input("Update Right", 0, len(st.session_state.data) - 1, value=len(st.session_state.data) - 1, key="ur")
        val = st.number_input("Value to add", value=1)
        if st.button("Update Range"):
            if ul > ur:
                st.error("Left index should be ≤ Right index.")
            else:
                st.session_state.tree.range_update(ul, ur, val)
                st.success(f"Added {val} to range [{ul}, {ur}]")

    st.divider()
    st.subheader("Modify Array")

    new_val = st.number_input("Append New Element")
    if st.button("Append"):
        st.session_state.data.append(int(new_val))
        st.session_state.tree = SegmentTree(st.session_state.data)
        st.success("Element added.")

    del_idx = st.number_input("Delete Index", 0, len(st.session_state.data) - 1, step=1)
    if st.button("Delete"):
        st.session_state.tree.delete_index(del_idx)
        st.success(f"Deleted element at index {del_idx}")
