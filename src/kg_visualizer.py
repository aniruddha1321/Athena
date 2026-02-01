# kg_visualizer.py - Interactive Knowledge Graph Visualization for Streamlit

import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from src.knowledge_graph import KnowledgeGraphBuilder
import json


def create_pyvis_graph(kg_builder: KnowledgeGraphBuilder):
    """Create interactive visualization using PyVis (if available)"""
    try:
        from pyvis.network import Network
        
        net = Network(
            height="400px",
            width="100%",
            bgcolor="#f8fafc",
            font_color="#1e293b",
            directed=True
        )
        
        # Configure physics
        net.set_options("""
        {
          "physics": {
            "enabled": true,
            "stabilization": {
              "enabled": true,
              "iterations": 100
            },
            "barnesHut": {
              "gravitationalConstant": -8000,
              "centralGravity": 0.3,
              "springLength": 200,
              "springConstant": 0.04
            }
          },
          "interaction": {
            "hover": true,
            "tooltipDelay": 100
          }
        }
        """)
        
        # Add nodes
        for node, data in kg_builder.graph.nodes(data=True):
            node_type = data.get('type', 'unknown')
            color = data.get('color', '#95E1D3')
            
            # Size based on degree
            degree = kg_builder.graph.degree(node)
            size = 10 + (degree * 3)
            
            title = f"{node}\nType: {node_type}\nConnections: {degree}"
            
            net.add_node(
                node,
                label=node,
                color=color,
                size=size,
                title=title,
                shape='dot'
            )
        
        # Add edges
        for source, target, data in kg_builder.graph.edges(data=True):
            relation = data.get('relation', 'related')
            context = data.get('context', '')
            
            title = f"{relation}\n{context[:100]}"
            
            net.add_edge(
                source,
                target,
                title=title,
                label=relation,
                arrows='to'
            )
        
        return net
        
    except ImportError:
        st.warning("⚠️ PyVis not installed. Install with: `pip install pyvis`")
        return None


def create_plotly_graph(kg_builder: KnowledgeGraphBuilder):
    """Create visualization using Plotly (fallback)"""
    try:
        import plotly.graph_objects as go
        
        # Get positions using spring layout
        pos = nx.spring_layout(kg_builder.graph, k=2, iterations=50)
        
        # Create edge traces
        edge_traces = []
        
        for source, target, data in kg_builder.graph.edges(data=True):
            x0, y0 = pos[source]
            x1, y1 = pos[target]
            
            relation = data.get('relation', 'related')
            
            edge_trace = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=1, color='#888'),
                hoverinfo='text',
                text=f"{source} → {target}\n{relation}",
                showlegend=False
            )
            edge_traces.append(edge_trace)
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_size = []
        
        for node, data in kg_builder.graph.nodes(data=True):
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            node_type = data.get('type', 'unknown')
            color = data.get('color', '#95E1D3')
            degree = kg_builder.graph.degree(node)
            
            node_text.append(f"{node}<br>Type: {node_type}<br>Connections: {degree}")
            node_color.append(color)
            node_size.append(10 + degree * 2)
        
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[node for node in kg_builder.graph.nodes()],
            hovertext=node_text,
            textposition="top center",
            marker=dict(
                color=node_color,
                size=node_size,
                line=dict(width=2, color='white')
            )
        )
        
        # Create figure
        fig = go.Figure(
            data=edge_traces + [node_trace],
            layout=go.Layout(
                title="Knowledge Graph",
                showlegend=False,
                hovermode='closest',
                margin=dict(b=0, l=0, r=0, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='#0e1117',
                paper_bgcolor='#0e1117',
                font=dict(color='white'),
                height=400
            )
        )
        
        return fig
        
    except ImportError:
        st.error("❌ Plotly not installed. Install with: `pip install plotly`")
        return None


def render_graph_statistics(kg_builder: KnowledgeGraphBuilder):
    """Render graph statistics in sidebar"""
    summary = kg_builder.get_graph_summary()
    
    st.sidebar.markdown("### 📊 Graph Statistics")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        st.metric("Nodes", summary['total_nodes'])
        st.metric("Density", f"{summary['density']:.2%}")
    
    with col2:
        st.metric("Edges", summary['total_edges'])
    
    # Node types
    st.sidebar.markdown("#### 📦 Node Types")
    for node_type, count in summary['node_types'].items():
        st.sidebar.write(f"- **{node_type}**: {count}")
    
    # Relations
    st.sidebar.markdown("#### 🔗 Relations")
    for rel_type, count in summary['relation_types'].items():
        st.sidebar.write(f"- *{rel_type}*: {count}")
    
    # Central nodes
    if summary['central_nodes']:
        st.sidebar.markdown("#### 🌟 Most Connected")
        for node, degree in summary['central_nodes'][:5]:
            st.sidebar.write(f"- {node[:30]}: {degree}")


def render_knowledge_graph_tab(pdf_text: str, title: str = "Research Paper"):
    """Main function to render knowledge graph tab"""
    
    st.markdown("### 🕸️ Knowledge Graph Analysis")
    st.info("💡 Visualize entities, methods, datasets, and their relationships extracted from your document")
    
    # Build graph button
    if 'kg_builder' not in st.session_state or st.button("Build Knowledge Graph", type="primary"):
        with st.spinner("Extracting knowledge and building graph..."):
            kg_builder = KnowledgeGraphBuilder()
            graph = kg_builder.build_graph(pdf_text, title)
            st.session_state.kg_builder = kg_builder
            st.success("Knowledge graph built successfully!")
    
    if 'kg_builder' not in st.session_state:
        st.warning("Click 'Build Knowledge Graph' to start")
        return
    
    kg_builder = st.session_state.kg_builder
    
    # Statistics in sidebar
    render_graph_statistics(kg_builder)
    
    # Initialize session state
    if 'viz_method' not in st.session_state:
        st.session_state.viz_method = "PyVis"
    if 'active_kg_tab' not in st.session_state:
        st.session_state.active_kg_tab = "Visualization"
    
    # CSS to reduce spacing and style labels
    st.markdown("""
    <style>
    /* Reduce spacing after button row */
    .stHorizontalBlock { margin-bottom: -10px; }
    /* Reduce hr margins */
    hr { margin: 0.5rem 0 !important; }
    /* Reduce heading margins */
    h4 { margin-top: 0.5rem !important; margin-bottom: 0.5rem !important; }
    /* Increase widget label font size */
    .stTextInput label, .stSelectbox label { font-size:25px !important; font-weight: 600 !important; }
    </style>
    """, unsafe_allow_html=True)
    
    # All buttons on same row: Visualization, Query, Analysis | PyVis, Plotly
    col1, col2, col3, spacer, col4, col5 = st.columns([1, 1, 1, 3, 1, 1])
    
    with col1:
        if st.button("Visualization", use_container_width=True,
                    type="primary" if st.session_state.active_kg_tab == "Visualization" else "secondary"):
            st.session_state.active_kg_tab = "Visualization"
            st.rerun()
    with col2:
        if st.button("Query", use_container_width=True,
                    type="primary" if st.session_state.active_kg_tab == "Query" else "secondary"):
            st.session_state.active_kg_tab = "Query"
            st.rerun()
    with col3:
        if st.button("Analysis", use_container_width=True,
                    type="primary" if st.session_state.active_kg_tab == "Analysis" else "secondary"):
            st.session_state.active_kg_tab = "Analysis"
            st.rerun()
    with col4:
        if st.button("PyVis", use_container_width=True,
                    type="primary" if st.session_state.viz_method == "PyVis" else "secondary"):
            st.session_state.viz_method = "PyVis"
            st.rerun()
    with col5:
        if st.button("Plotly", use_container_width=True,
                    type="primary" if st.session_state.viz_method == "Plotly" else "secondary"):
            st.session_state.viz_method = "Plotly"
            st.rerun()
    
    st.markdown("---")
    
    # CONTENT: Visualization
    if st.session_state.active_kg_tab == "Visualization":
        # Show graph based on selection
        if st.session_state.viz_method == "PyVis":
            net = create_pyvis_graph(kg_builder)
            
            if net:
                html_file = "knowledge_graph.html"
                net.save_graph(html_file)
                
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                components.html(html_content, height=420, scrolling=False)
            else:
                st.info("PyVis not available, using Plotly...")
                fig = create_plotly_graph(kg_builder)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        else:
            fig = create_plotly_graph(kg_builder)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # Legend
        with st.expander("🎨 Color Legend"):
            legend_data = {
                "🔴 Paper": "Central research paper",
                "🔵 Methods": "Techniques and algorithms",
                "🟡 Datasets": "Training/evaluation data",
                "🟢 Metrics": "Performance measurements",
                "🟣 Models": "Neural network architectures",
                "🟠 Results": "Performance numbers"
            }
            
            for emoji_color, description in legend_data.items():
                st.write(f"{emoji_color}: {description}")
    
    # CONTENT: Query
    elif st.session_state.active_kg_tab == "Query":
        st.markdown("#### Query Knowledge Graph")
        
        query = st.text_input(
            "Search for entities or concepts",
            placeholder="e.g., transformer, BLEU, dataset"
        )
        
        if query:
            results = kg_builder.query_graph(query, k=10)
            
            if results:
                st.success(f"✅ Found {len(results)} results")
                
                for i, result in enumerate(results, 1):
                    with st.expander(f"Result {i}", expanded=(i <= 3)):
                        if result.get('type') == 'relationship':
                            st.markdown(f"**Relationship:**")
                            st.write(f"{result['source']} --[{result['relation']}]--> {result['target']}")
                            if result.get('context'):
                                st.caption(f"Context: {result['context']}")
                        else:
                            st.markdown(f"**Entity:** {result['node']}")
                            st.write(f"Type: {result['type']}")
                            st.write(f"Connections: {result['degree']}")
                            
                            if result.get('neighbors'):
                                st.write(f"Connected to: {', '.join(result['neighbors'][:3])}")
            else:
                st.warning("No results found for this query")
        
        # Path finding
        st.markdown("---")
        st.markdown("#### Find Path Between Entities")
        
        col1, col2 = st.columns(2)
        
        with col1:
            source_node = st.selectbox(
                "Source",
                options=list(kg_builder.graph.nodes()),
                key="source_path"
            )
        
        with col2:
            target_node = st.selectbox(
                "Target",
                options=list(kg_builder.graph.nodes()),
                key="target_path"
            )
        
        if st.button("🔍 Find Paths"):
            paths = kg_builder.find_paths(source_node, target_node, max_length=4)
            
            if paths:
                st.success(f"✅ Found {len(paths)} path(s)")
                
                for i, path in enumerate(paths[:5], 1):  # Show top 5
                    st.write(f"**Path {i}:** {' → '.join(path)}")
            else:
                st.info("No paths found between these entities")
    
    # CONTENT: Analysis
    elif st.session_state.active_kg_tab == "Analysis":
        st.markdown("#### Graph Analysis (Export)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export as JSON"):
                export_data = kg_builder.export_to_cytoscape()
                
                json_str = json.dumps(export_data, indent=2)
                st.download_button(
                    "Download JSON",
                    data=json_str,
                    file_name="knowledge_graph.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📥 Export as GraphML"):
                import tempfile
                
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix='.graphml',
                    mode='w'
                )
                
                nx.write_graphml(kg_builder.graph, temp_file.name)
                
                with open(temp_file.name, 'r') as f:
                    graphml_content = f.read()
                
                st.download_button(
                    "Download GraphML",
                    data=graphml_content,
                    file_name="knowledge_graph.graphml",
                    mime="application/xml"
                )
        
        # Subgraph extraction
        st.markdown("---")
        
        col_controls, col_help = st.columns([1, 1])
        
        with col_controls:
            st.markdown("##### 🔬 Extract Subgraph")
            center_node = st.selectbox(
                "Center node",
                options=list(kg_builder.graph.nodes()),
                key="center_subgraph"
            )
            
            depth = st.slider("Depth (hops)", min_value=1, max_value=3, value=1)
            
            if st.button("Extract Subgraph"):
                subgraph = kg_builder.get_subgraph(center_node, depth=depth)
                
                st.success(f"✅ Subgraph: {subgraph.number_of_nodes()} nodes, {subgraph.number_of_edges()} edges")
                
                # Show subgraph details
                st.markdown("**Nodes in subgraph:**")
                for node in list(subgraph.nodes())[:10]:
                    node_type = subgraph.nodes[node].get('type', 'unknown')
                    st.write(f"- {node} ({node_type})")
                
                if subgraph.number_of_nodes() > 10:
                    st.write(f"... and {subgraph.number_of_nodes() - 10} more")
        
        with col_help:
            st.markdown("""
            ##### How to use:

            1. **Select a center node** - Choose the entity you want to explore from the dropdown
            
            2. **Set depth (hops)** - Controls how far to expand:
               - `1 hop`: Direct connections only
               - `2 hops`: Connections of connections
               - `3 hops`: Extended network
            
            3. **Click Extract** - View the subgraph containing all nodes within the specified distance
            
            💡 *Useful for focusing on specific parts of large knowledge graphs*
            """)


# =====================================================================
# 🧪 STANDALONE TEST
# =====================================================================

if __name__ == "__main__":
    st.set_page_config(
        page_title="Knowledge Graph Visualizer",
        page_icon="🕸️",
        layout="wide"
    )
    
    st.title("🕸️ Knowledge Graph Visualizer Test")
    
    sample_text = """
    Title: Attention Is All You Need
    
    We propose the Transformer architecture based on self-attention mechanisms.
    The model uses multi-head attention and is evaluated on WMT 2014 dataset.
    We achieve 28.4 BLEU score on English-German translation task.
    The Transformer outperforms LSTM and CNN models on machine translation.
    We use Adam optimizer with learning rate scheduling for training.
    Results show 92% accuracy on SQUAD question answering benchmark.
    """
    
    render_knowledge_graph_tab(sample_text, "Test Paper")