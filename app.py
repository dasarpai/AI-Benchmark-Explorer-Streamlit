import streamlit as st
import pandas as pd
import plotly.express as px
import math

# Set page configuration
st.set_page_config(
    page_title="AI Benchmark Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved styling
st.markdown("""
<style>
    /* Enhanced Dark Theme */
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    
    /* Improved Table Styling */
    .stDataFrame {
        background-color: #1e2026;
        color: #f0f2f6;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Refined Typography */
    h1, h2, h3 {
        color: #f0f2f6;
        font-weight: 600;
    }
    
    /* Improved Sidebar */
    .stSidebar {
        background-color: #1e2026;
    }
    
    /* Enhanced Button Styles */
    .stButton>button {
        background-color: #3b5998;
        color: white;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #4a6cd4;
        transform: scale(1.05);
    }
    
    /* Refined Pagination */
    .pagination {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 15px 0;
        padding: 10px;
        background-color: #1e2026;
        border-radius: 8px;
    }
    
    .pagination-button {
        background-color: #3b5998;
        color: white;
        border: none;
        padding: 8px 15px;
        margin: 0 5px;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .pagination-button:hover {
        background-color: #4a6cd4;
    }
    
    .pagination-button.active {
        background-color: #4a6cd4;
    }
    
    /* Improved Row Spacing */
    .stDataFrame .row-container {
        margin-bottom: 5px;
    }
    
    /* Horizontal Chip Layout */
    .horizontal-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        align-items: center;
    }
    
    .chip {
        background-color: #2c3e50;
        color: #ecf0f1;
        padding: 3px 8px;
        border-radius: 15px;
        font-size: 0.8em;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Cached data loading function
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/datasets.csv')
        
        # Enhanced column calculations
        df['benchmark_cnt'] = df['benchmark_urls'].apply(
            lambda x: len([url for url in str(x).split(',') if url.strip()]) if pd.notna(x) else 0
        )
        df['associated_task_cnt'] = df['associated_tasks'].apply(
            lambda x: len([task for task in str(x).split(',') if task.strip()]) if pd.notna(x) else 0
        )
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Improved filtering function
def create_filter_panel(df):
    st.sidebar.title("🔍 Dataset Filters")
    
    # Task filter with count
    task_counts = df['task'].value_counts()
    tasks = ['All'] + list(task_counts.index)
    task_options = [f"{task} ({count})" for task, count in task_counts.items()]
    selected_task_with_count = st.sidebar.selectbox("Task", ['All'] + task_options)
    selected_task = selected_task_with_count.split(' (')[0] if selected_task_with_count != 'All' else 'All'
    
    # Area filter
    areas = ['All'] + sorted(df['area'].dropna().unique().tolist())
    selected_area = st.sidebar.selectbox("Research Area", areas)
    
    # Modalities multiselect
    all_modalities = []
    for mods in df['modalities'].dropna():
        all_modalities.extend([m.strip() for m in mods.split(',') if m.strip()])
    unique_modalities = sorted(set(all_modalities))
    selected_modalities = st.sidebar.multiselect("Modalities", unique_modalities)
    
    # Year range slider
    years = df['year_published'].dropna().astype(int)
    min_year, max_year = int(years.min()), int(years.max())
    year_range = st.sidebar.slider("Publication Year", min_year, max_year, (min_year, max_year))
    
    # Search input
    search_term = st.sidebar.text_input("Search Datasets", "")
    
    # Filtering logic
    filtered_df = df.copy()
    
    if selected_task != 'All':
        filtered_df = filtered_df[filtered_df['task'] == selected_task]
    
    if selected_area != 'All':
        filtered_df = filtered_df[filtered_df['area'] == selected_area]
    
    if selected_modalities:
        filtered_df = filtered_df[filtered_df['modalities'].apply(
            lambda x: any(mod.strip() in str(x).split(',') for mod in selected_modalities) if pd.notna(x) else False
        )]
    
    filtered_df = filtered_df[
        (filtered_df['year_published'] >= year_range[0]) & 
        (filtered_df['year_published'] <= year_range[1])
    ]
    
    if search_term:
        filtered_df = filtered_df[filtered_df['dataset_id'].str.contains(search_term, case=False)]
    
    return filtered_df

# Detailed view of dataset
def show_dataset_details(dataset):
    st.markdown("## 📊 Dataset Details")
    
    # Create two-column layout for key information
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {dataset['dataset_id']}")
        st.markdown(f"**Description:** {dataset['description'] if pd.notna(dataset['description']) else 'No description available'}")
    
    with col2:
        st.markdown("#### Quick Stats")
        st.metric("Total Benchmarks", dataset['benchmark_cnt'])
        st.metric("Associated Tasks", dataset['associated_task_cnt'])
    
    # Horizontal layout for metadata
    st.markdown("### Dataset Metadata")
    
    # Use columns to create horizontal layout
    cols = st.columns(5)
    
    metadata_items = [
        ("Task", dataset['task']),
        ("Area", dataset['area']),
        ("Year", dataset['year_published']),
        ("License", dataset['license']),
        ("Languages", dataset['languages'])
    ]
    
    for i, (label, value) in enumerate(metadata_items):
        with cols[i]:
            st.markdown(f"**{label}**")
            st.markdown(f"<div class='chip'>{value if pd.notna(value) else 'N/A'}</div>", unsafe_allow_html=True)
    
    # Modalities and Associated Tasks
    st.markdown("### Additional Information")
    
    cols = st.columns(2)
    
    with cols[0]:
        st.markdown("**Modalities**")
        if pd.notna(dataset['modalities']):
            modalities = [mod.strip() for mod in dataset['modalities'].split(',') if mod.strip()]
            st.markdown(
                "<div class='horizontal-chips'>" + 
                "".join([f"<span class='chip'>{mod}</span>" for mod in modalities]) + 
                "</div>", 
                unsafe_allow_html=True
            )
        else:
            st.markdown("No modalities available")
    
    with cols[1]:
        st.markdown("**Associated Tasks**")
        if pd.notna(dataset['associated_tasks']):
            tasks = [task.strip() for task in dataset['associated_tasks'].split(',') if task.strip()]
            st.markdown(
                "<div class='horizontal-chips'>" + 
                "".join([f"<span class='chip'>{task}</span>" for task in tasks]) + 
                "</div>", 
                unsafe_allow_html=True
            )
        else:
            st.markdown("No associated tasks available")

# Main application
def main():
    st.title("🌐 AI Benchmark Explorer")
    
    # Load data
    df = load_data()
    
    if df.empty:
        st.warning("Please place your dataset CSV file in the 'data' directory.")
        return
    
    # Apply filters
    filtered_df = create_filter_panel(df)
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["Dataset Explorer", "Dataset Statistics"])
    
    with tab1:
        # Improved pagination setup
        st.sidebar.markdown("### Pagination Settings")
        page_size_options = [10, 20, 50, 100]
        page_size = st.sidebar.selectbox("Entries per page", page_size_options, index=1)
        
        total_pages = math.ceil(len(filtered_df) / page_size)
        
        # Store current page in session state to maintain state between interactions
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
        
        # Ensure current page is valid (in case filtering reduces available pages)
        if st.session_state.current_page > total_pages:
            st.session_state.current_page = 1
        
        # Slice data for current page
        start_idx = (st.session_state.current_page - 1) * page_size
        end_idx = start_idx + page_size
        page_data = filtered_df.iloc[start_idx:end_idx].reset_index(drop=True)
        
        # Display dataset count and page info
        st.markdown(f"**Showing {min(page_size, len(page_data))} of {len(filtered_df)} datasets (Page {st.session_state.current_page} of {total_pages})**")
        
        # Create a clickable dataframe
        # We'll use a unique key for each row based on dataset_id
        if 'selected_dataset_id' not in st.session_state:
            st.session_state.selected_dataset_id = None
        
        # Column headers (displayed BEFORE the data rows)
        col_headers = st.columns([3, 1, 1, 1, 1, 1])
        with col_headers[0]:
            st.markdown("<div style='font-weight: bold;'>Dataset ID</div>", unsafe_allow_html=True)
        with col_headers[1]:
            st.markdown("<div style='font-weight: bold;'>Task</div>", unsafe_allow_html=True)
        with col_headers[2]:
            st.markdown("<div style='font-weight: bold;'>Area</div>", unsafe_allow_html=True)
        with col_headers[3]:
            st.markdown("<div style='font-weight: bold;'>Year</div>", unsafe_allow_html=True)
        with col_headers[4]:
            st.markdown("<div style='font-weight: bold;'>Benchmarks</div>", unsafe_allow_html=True)
        with col_headers[5]:
            st.markdown("<div style='font-weight: bold;'>Tasks</div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 0; padding: 0; height: 1px; background-color: #4a6cd4; border: none;'>", unsafe_allow_html=True)
        
        # Display table with key columns and make it interactive
        for idx, row in page_data.iterrows():
            dataset_id = row['dataset_id']
            # Create a container for the entire row to make it visually cohesive
            row_container = st.container()
            with row_container:
                # Add hover effect with CSS
                st.markdown(f"""
                <style>
                    div[data-testid="stHorizontalBlock"]:has(button#btn_{dataset_id}) {{
                        background-color: {('#2c3e50' if st.session_state.selected_dataset_id == dataset_id else '#1e2026')};
                        border-radius: 5px;
                        padding: 5px;
                        margin-bottom: 5px;
                        transition: background-color 0.3s;
                    }}
                    div[data-testid="stHorizontalBlock"]:has(button#btn_{dataset_id}):hover {{
                        background-color: #2c3e50;
                    }}
                    /* Control button height to keep rows compact */
                    button#btn_{dataset_id} {{
                        padding: 0px 8px;
                        min-height: 0px;
                        height: auto;
                        line-height: normal;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        width: 100%;
                        text-align: left;
                    }}
                </style>
                """, unsafe_allow_html=True)
                
                # Create columns with the same widths as the headers
                cols = st.columns([3, 1, 1, 1, 1, 1])
                
                # Dataset ID as a button in the first column
                with cols[0]:
                    if st.button(f"{dataset_id}", key=f"btn_{dataset_id}"):
                        st.session_state.selected_dataset_id = dataset_id
                        st.experimental_rerun()
                
                # Other data in the remaining columns
                with cols[1]:
                    st.write(row['task'])
                with cols[2]:
                    st.write(row['area'] if pd.notna(row['area']) else 'N/A')
                with cols[3]:
                    st.write(int(row['year_published']) if pd.notna(row['year_published']) else 'N/A')
                with cols[4]:
                    st.write(row['benchmark_cnt'])
                with cols[5]:
                    st.write(row['associated_task_cnt'])
        
        # Pagination controls
        st.markdown("---")
        col_prev, col_pages, col_next = st.columns([1, 3, 1])
        
        with col_prev:
            if st.button('← Previous', disabled=(st.session_state.current_page == 1)):
                st.session_state.current_page -= 1
                st.experimental_rerun()
        
        with col_pages:
            # Display page numbers (show up to 7 page numbers with ellipsis for others)
            page_cols = st.columns(min(7, total_pages))
            displayed_pages = []
            
            if total_pages <= 7:
                displayed_pages = list(range(1, total_pages + 1))
            else:
                # Always include first, last, current and some surrounding pages
                current = st.session_state.current_page
                displayed_pages = [1]
                
                if current > 3:
                    displayed_pages.append('...')
                
                start_page = max(2, current - 1)
                end_page = min(total_pages - 1, current + 1)
                
                displayed_pages.extend(list(range(start_page, end_page + 1)))
                
                if current < total_pages - 2:
                    displayed_pages.append('...')
                
                if total_pages > 1:
                    displayed_pages.append(total_pages)
            
            # Create the page number buttons
            for i, page_col in enumerate(page_cols):
                if i < len(displayed_pages):
                    page = displayed_pages[i]
                    with page_col:
                        if page == '...':
                            st.write('...')
                        else:
                            if st.button(str(page), key=f"page_{page}", 
                                        disabled=(page == st.session_state.current_page)):
                                st.session_state.current_page = page
                                st.experimental_rerun()
        
        with col_next:
            if st.button('Next →', disabled=(st.session_state.current_page == total_pages)):
                st.session_state.current_page += 1
                st.experimental_rerun()
        
        # Show selected dataset details if any
        if st.session_state.selected_dataset_id:
            selected_row = df[df['dataset_id'] == st.session_state.selected_dataset_id].iloc[0]
            st.markdown("---")
            show_dataset_details(selected_row)
    
    with tab2:
        # Statistics plots
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Tasks Distribution")
            task_counts = filtered_df['task'].value_counts()
            fig_tasks = px.pie(task_counts, values=task_counts.values, names=task_counts.index, 
                               title="Tasks Overview")
            st.plotly_chart(fig_tasks, use_container_width=True)
        
        with col2:
            st.markdown("### Yearly Trends")
            year_counts = filtered_df['year_published'].value_counts().sort_index()
            fig_years = px.line(x=year_counts.index, y=year_counts.values, 
                                labels={'x': 'Year', 'y': 'Number of Datasets'},
                                title="Datasets by Year")
            st.plotly_chart(fig_years, use_container_width=True)

if __name__ == "__main__":
    main()