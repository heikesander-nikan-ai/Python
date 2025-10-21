# Hive Mind Prototype

This repository demonstrates a **Trust-Validated Enterprise Memory** system using Streamlit and PyVis.  
It enables ingestion, validation, and visualization of knowledge nodes, supporting collaborative workflows and provenance tracking.

---

## Repository Structure

- **interface_flow_SKA.py**  
  Main Streamlit app.  
  - Ingests knowledge files (Markdown, TXT, PDF).
  - Allows multiple file selection and batch submission for validation.
  - Tracks validation status and provenance.
  - Visualizes the knowledge graph interactively (PyVis).
  - All ingested nodes and their metadata are persisted as JSON files in the `ingested` folder.

- **graph visualization renderer.py**  
  Standalone script for generating and saving a knowledge graph visualization from mock data using PyVis.  
  - Produces an interactive HTML file (`knowledge_graph_view.html`) showing nodes and relationships.
  - Node popups display full content and metadata.

- **ingested/**  
  Folder where all ingested knowledge nodes are stored as JSON files.  
  - Each file represents a node with its content, status, author, validator, concepts, and relations.

---

## Usage

1. **Install dependencies:**
   ```bash
   pip install streamlit pyvis pandas
   ```

2. **Run the Streamlit app:**
   ```bash
   streamlit run interface_flow_SKA.py
   ```
   - Use the tabs to query, ingest, validate, and visualize knowledge.

3. **Generate standalone graph visualization (optional):**
   ```bash
   python graph\ visualization\ renderer.py
   ```
   - Open the generated HTML file in your browser.

---

## Features

- **Multi-file Ingestion:**  
  Upload and queue multiple files for review and validation.

- **Validation Workflow:**  
  Approve draft nodes, with persistent status updates.

- **Knowledge Graph Visualization:**  
  Interactive graph with node popups showing full content and metadata.

- **Provenance Tracking:**  
  Each node records author, validator, and validation status.

---

## Notes

- All ingested data is stored locally in the `ingested` folder.
- The graph visualization in the Streamlit app reflects the current state of all ingested and validated nodes.
- Markdown files are parsed for title, concepts, and relations to enrich the graph.

---

## License

This repository is for demonstration and prototyping purposes.
