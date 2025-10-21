import streamlit as st
import os
import json
import streamlit.components.v1 as components
from pyvis.network import Network

# --- Disk Persistence Setup ---
INGESTED_FOLDER = os.path.join(os.path.dirname(__file__), "ingested")
os.makedirs(INGESTED_FOLDER, exist_ok=True)

def load_ingested_nodes():
    nodes = []
    for fname in os.listdir(INGESTED_FOLDER):
        if fname.endswith(".json"):
            with open(os.path.join(INGESTED_FOLDER, fname), "r") as f:
                nodes.append(json.load(f))
    return nodes

def save_node_to_disk(node):
    fname = f"node_{node['id']}.json"
    with open(os.path.join(INGESTED_FOLDER, fname), "w") as f:
        json.dump(node, f)

def update_node_on_disk(node):
    fname = f"node_{node['id']}.json"
    with open(os.path.join(INGESTED_FOLDER, fname), "w") as f:
        json.dump(node, f)

def extract_md_info(md_bytes, filename):
    """Extracts title, concepts, and relations from markdown file bytes."""
    text = md_bytes.decode("utf-8")
    lines = text.splitlines()
    title = lines[0] if lines else filename.split('.')[0]
    concepts = [line[2:].strip() for line in lines if line.startswith('- ')]
    relations = []
    for line in lines:
        if "relates to:" in line:
            parts = line.split("relates to:")
            if len(parts) == 2:
                target = parts[1].strip()
                relations.append({"target": target, "relation": "relates to"})
    return title, concepts, relations

# --- Data Simulation (Mock Backend) ---
if 'corporate_knowledge' not in st.session_state:
    st.session_state.corporate_knowledge = [
        {"id": 1, "content": "Liquid Neural Networks (LNNs) show superior time-series prediction accuracy compared to standard LSTMs for financial data.", "status": "Validated", "author": "User Master", "validator": "Igor", "title": "Liquid Neural Networks", "concepts": ["LNNs", "time-series prediction"], "relations": []},
        {"id": 2, "content": "The Q4 2024 exit strategy will prioritize an acquisition by a major cloud provider (e.g., Azure/GCP).", "status": "Draft", "author": "User Master", "validator": "None", "title": "Q4 Exit Strategy", "concepts": ["Azure", "GCP", "acquisition"], "relations": []},
        {"id": 3, "content": "Our primary RAG vector store utilizes a custom-trained BGE model on enterprise vocabulary.", "status": "Validated", "author": "Igor", "validator": "User Master", "title": "RAG Vector Store", "concepts": ["BGE model", "enterprise vocabulary"], "relations": []},
    ]
    # Load nodes from disk
    st.session_state.corporate_knowledge += load_ingested_nodes()

# --- UI Functions ---

def display_rag_tool():
    st.header("1. RAG Query Tool (The Corporate Memory)", divider='blue')
    query = st.text_input("Ask the Hive Mind:", placeholder="What are the key benefits of Liquid Neural Networks?")
    if query:
        st.subheader("Hive Mind Response (Simulated):")
        if "LNN" in query or "Liquid Neural Network" in query:
            result = st.session_state.corporate_knowledge[0]
            st.success(result['content'])
            st.markdown(f"""
            <div style="border-left: 5px solid #007bff; padding: 10px; margin-top: 15px; background-color: #f7f9fc;">
                **🔍 Provenance & Trust Check**
                - **Status:** **{result['status']}**
                - **Source Node ID:** `{result['id']}` (Directly from Vector Store/KG)
                - **Author:** `{result['author']}`
                - **Validated By:** `{result['validator']}`
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("I found this unvalidated content that might be relevant: 'The best deployment environment is Replit for low-cost PoC hosting.'")
            st.caption("Status: **Unvalidated Draft** (Not included in Corporate Trust layer)")

def display_ingestion_tool():
    st.header("2. Data Ingestion & Contribution", divider='green')
    st.markdown("**Action:** Upload one or more documents (e.g., Obsidian markdown notes) to create new knowledge nodes for review.")

    # Initialize pending_files in session state
    if 'pending_files' not in st.session_state:
        st.session_state.pending_files = []

    # Multiple file upload
    uploaded_files = st.file_uploader("Upload Documents for Review", type=['txt', 'md', 'pdf'], accept_multiple_files=True)
    if uploaded_files:
        # Add new files to pending_files, avoiding duplicates by filename
        existing_names = {f.name for f in st.session_state.pending_files}
        for f in uploaded_files:
            if f.name not in existing_names:
                st.session_state.pending_files.append(f)

    # Show pending files
    if st.session_state.pending_files:
        st.subheader("Files Awaiting Submission for Validation")
        for idx, f in enumerate(st.session_state.pending_files):
            st.write(f"- {f.name}")
        # Option to submit all files
        if st.button("Submit ALL for Validation"):
            for f in st.session_state.pending_files:
                new_id = len(st.session_state.corporate_knowledge) + 1
                if f.name.endswith('.md'):
                    title, concepts, relations = extract_md_info(f.read(), f.name)
                else:
                    title, concepts, relations = (f.name.split('.')[0], [], [])
                node = {
                    "id": new_id,
                    "content": f"New Draft: {f.name} uploaded for review. Key concepts extracted: {', '.join(concepts) if concepts else f.name.split('.')[0]}.",
                    "status": "Draft",
                    "author": "User Master",
                    "validator": "None",
                    "title": title,
                    "concepts": concepts,
                    "relations": relations
                }
                st.session_state.corporate_knowledge.append(node)
                save_node_to_disk(node)
            st.success(f"{len(st.session_state.pending_files)} files submitted. Draft nodes are awaiting validation.")
            st.session_state.pending_files = []
            st.rerun()
        # Option to remove individual files before submission
        for idx, f in enumerate(st.session_state.pending_files):
            if st.button(f"Remove {f.name}", key=f"remove_{f.name}"):
                st.session_state.pending_files.pop(idx)
                st.rerun()
    else:
        st.info("No files awaiting submission.")

def display_validation_tool():
    st.header("3. Knowledge Validation Workflow", divider='red')
    st.markdown("**Action:** Review, edit, and validate knowledge nodes created by the team.")
    draft_nodes = [node for node in st.session_state.corporate_knowledge if node['status'] == 'Draft']
    if not draft_nodes:
        st.info("All knowledge is currently **Validated** or awaiting contribution. The queue is clear.")
        return
    for node in draft_nodes:
        with st.expander(f"Draft Node ID {node['id']} - From: {node['author']}"):
            st.write(f"Content Snippet: *{node['content'][:100]}...*")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"✅ Validate & Approve (ID {node['id']})", key=f"validate_{node['id']}", use_container_width=True):
                    for n in st.session_state.corporate_knowledge:
                        if n['id'] == node['id']:
                            n['status'] = "Validated"
                            n['validator'] = "Igor"
                            update_node_on_disk(n)
                            break
                    st.toast(f"Node ID {node['id']} has been successfully **Validated** and is now included in the corporate truth layer.")
                    st.rerun()

def display_graph_visualization():
    st.header("4. Knowledge Graph Visualization", divider='violet')
    nodes = st.session_state.corporate_knowledge
    edges_data = []
    for node in nodes:
        for rel in node.get("relations", []):
            edges_data.append((f"node-{node['id']}", rel["target"], rel["relation"], 1))
    if not edges_data and len(nodes) > 1:
        for i in range(len(nodes)-1):
            edges_data.append((f"node-{nodes[i]['id']}", f"node-{nodes[i+1]['id']}", "related", 1))
    import pandas as pd
    df_edges = pd.DataFrame(edges_data, columns=['source', 'target', 'relation', 'weight'])
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white", notebook=False)
    net.toggle_physics(True)
    for node in nodes:
        node_id = f"node-{node['id']}"
        color = '#00CC66' if node['status'] == 'Validated' else '#FFCC00'
        # Use HTML for the popup content
        title = f"""
        <b>Title:</b> {node.get('title','')}<br>
        <b>Status:</b> {node['status'].upper()}<br>
        <b>Author:</b> {node.get('author','')}<br>
        <b>Validator:</b> {node.get('validator','')}<br>
        <b>Concepts:</b> {', '.join(node.get('concepts', []))}<br>
        <b>Content:</b> {node.get('content','')}
        """
        net.add_node(node_id, label=node.get('title', node_id), title=title, color=color, size=15 if node['status'] == 'Validated' else 10)
    for _, row in df_edges.iterrows():
        net.add_edge(row['source'], row['target'], title=row['relation'], label=row['relation'], color='#AAAAAA', width=row['weight'])
    net.set_options("""
    var options = {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 150,
          "springConstant": 0.08
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)
    graph_html = "graph.html"
    net.save_graph(graph_html)
    with open(graph_html, "r") as f:
        html = f.read()
    components.html(html, height=650, scrolling=True)

# --- Main App Logic ---

st.set_page_config(layout="centered", page_title="Hive Mind Demonstrator", initial_sidebar_state="expanded")

st.title(" Hive Mind Prototype (Step 1)")
st.caption("Demonstrating the **Trust-Validated Enterprise Memory** USP.")

tab1, tab2, tab3, tab4 = st.tabs(["💬 Query Tool", "📥 Ingestion", "✅ Validation Queue", "🕸️ Knowledge Graph"])

with tab1:
    display_rag_tool()
with tab2:
    display_ingestion_tool()
with tab3:
    display_validation_tool()
with tab4:
    display_graph_visualization()

st.sidebar.markdown("---")
validated_count = len([n for n in st.session_state.corporate_knowledge if n['status'] == 'Validated'])
draft_count = len([n for n in st.session_state.corporate_knowledge if n['status'] == 'Draft'])
st.sidebar.metric(label="Validated Nodes", value=validated_count)
st.sidebar.metric(label="Draft Nodes", value=draft_count)
st.sidebar.markdown("*The demonstrator is running locally on your Ollama setup.*")