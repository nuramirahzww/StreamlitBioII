import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Function to retrieve PPI data from BioGRID
def retrieve_ppi_biogrid(target_protein):
    # Mocked data retrieval for example purposes
    ppi_data = pd.DataFrame({
        'Protein A': [target_protein, target_protein, 'Protein_X'],
        'Protein B': ['Protein_1', 'Protein_2', 'Protein_Y'],
        'Interaction Type': ['interaction', 'binding', 'association']
    })
    return ppi_data

# Function to retrieve PPI data from STRING
def retrieve_ppi_string(target_protein):
    # Mocked data retrieval for example purposes
    ppi_data = pd.DataFrame({
        'Protein A': [target_protein, target_protein, 'Protein_Z'],
        'Protein B': ['Protein_3', 'Protein_4', 'Protein_W'],
        'Interaction Type': ['interaction', 'binding', 'association']
    })
    return ppi_data

# Function to generate a network graph from PPI data
def generate_network(dataframe):
    G = nx.Graph()
    
    # Add edges to the graph based on the PPI data
    for _, row in dataframe.iterrows():
        G.add_edge(row['Protein A'], row['Protein B'])
        
    return G

# Function to calculate centrality measures
def get_centralities(network_graph):
    centrality_measures = {}
    
    # Degree centrality
    centrality_measures['degree'] = nx.degree_centrality(network_graph)
    
    # Betweenness centrality
    centrality_measures['betweenness'] = nx.betweenness_centrality(network_graph)
    
    # Closeness centrality
    centrality_measures['closeness'] = nx.closeness_centrality(network_graph)
    
    # Eigenvector centrality
    centrality_measures['eigenvector'] = nx.eigenvector_centrality(network_graph, max_iter=500)
    
    # PageRank centrality
    centrality_measures['pagerank'] = nx.pagerank(network_graph)
    
    return centrality_measures

# Streamlit App
def main():
    st.title("Protein-Protein Interaction (PPI) Network Analysis")

    # User input for protein ID and database selection
    target_protein = st.text_input("Enter Protein ID")
    database_choice = st.selectbox("Choose Database", ["BioGRID", "STRING"])
    
    if st.button("Retrieve PPI Data"):
        # Show loading spinner while fetching data
        with st.spinner('Retrieving PPI data...'):
            # Retrieve PPI data based on user selection
            if database_choice == "BioGRID":
                ppi_data = retrieve_ppi_biogrid(target_protein)
            else:
                ppi_data = retrieve_ppi_string(target_protein)
        
            # Generate network graph
            network_graph = generate_network(ppi_data)

            # Display PPI data and graph only after retrieval
            st.success("Data Retrieved Successfully!")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("PPI Data Information")
                st.write(f"Number of edges: {network_graph.number_of_edges()}")
                st.write(f"Number of nodes: {network_graph.number_of_nodes()}")
                st.write("PPI Data:")
                st.dataframe(ppi_data)
            
            with col2:
                st.subheader("Network Visualization")
                # Network Visualization
                st.graphviz_chart(nx.nx_pydot.to_pydot(network_graph).to_string())

            # Display centrality measures and their bar charts side by side
            centralities = get_centralities(network_graph)
            for measure, values in centralities.items():
                st.subheader(f"**{measure.capitalize()} Centrality**")

                # Sort and display top 5 nodes based on centrality values
                sorted_values = sorted(values.items(), key=lambda item: item[1], reverse=True)[:5]

                # Prepare for side-by-side display of the chart and the data
                col1, col2 = st.columns(2)
                with col1:
                    st.write(sorted_values)
                    st.write(f"Full {measure.capitalize()} Centrality List:")
                    st.json(values)

                with col2:
                    # Plotting a bar chart for the top 5 nodes
                    nodes, scores = zip(*sorted_values)
                    plt.figure(figsize=(8, 5))
                    plt.bar(nodes, scores, color='royalblue')
                    plt.xlabel('Node')
                    plt.ylabel(f'{measure.capitalize()} Centrality Score')
                    plt.title(f'Top 5 Nodes by {measure.capitalize()} Centrality')
                    st.pyplot(plt)

if __name__ == "__main__":
    main()
