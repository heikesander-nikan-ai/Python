import pandas as pd
from pyvis.network import Network

# --- Data Simulation (Mirrors the knowledge structure for visualization) ---

mock_knowledge = [
    {"id": "node-1", "content": "Liquid Neural Networks (LNNs) show superior time-series prediction.", "status": "Validated"},
    {"id": "node-2", "content": "Q4 Exit Strategy prioritizes Azure/GCP acquisition.", "status": "Draft"},
    {"id": "node-3", "content": "Primary RAG utilizes custom-trained BGE model.", "status": "Validated"},
    {"id": "node-4", "content": "New ISO 9001 compliance standards released.", "status": "Draft"},
    {"id": "node-5", "content": "Obsidian MD files used for initial KG ingestion.", "status": "Validated"},
]

# All edges must have a weight for DataFrame consistency
edges_data = [
    ('node-1', 'node-3', 'uses', 2),          # Validated to Validated
    ('node-3', 'node-5', 'processes', 2),     # Validated to Validated
    ('node-2', 'node-1', 'depends on', 1),    # Draft to Validated
    ('node-4', 'node-5', 'is related to', 1), # Draft to Validated
]
df_edges = pd.DataFrame(edges_data, columns=['source', 'target', 'relation', 'weight'])

def generate_knowledge_graph(nodes, df_edges, output_filename='knowledge_graph_view.html'):
    """Generates an interactive pyvis network visualization."""
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", notebook=False)
    net.toggle_physics(True)
    
    # Add Nodes
    for node in nodes:
        node_id = node['id']
        color = '#00CC66' if node['status'] == 'Validated' else '#FFCC00'
        title = f"Status: {node['status'].upper()}\nContent: {node['content']}"
        net.add_node(
            node_id, 
            label=node_id, 
            title=title, 
            color=color,
            size=15 if node['status'] == 'Validated' else 10
        )
        
    # Add Edges
    for _, row in df_edges.iterrows():
        net.add_edge(
            row['source'],
            row['target'],
            title=row['relation'],
            label=row['relation'],
            color='#AAAAAA',
            width=row['weight']
        )
        
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
    
    net.save_graph(output_filename)
    print(f"Interactive graph saved to {output_filename}")

if __name__ == '__main__':
    generate_knowledge_graph(mock_knowledge, df_edges)

    # Note: To view this, you would typically open the generated HTML file in a browser.
    # We will not generate the HTML file block here, as it requires the python script to run first.
