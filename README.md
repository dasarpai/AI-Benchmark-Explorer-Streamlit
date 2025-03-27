# AI Benchmark Explorer - Streamlit Version

This is a Python Streamlit implementation of the AI Benchmark Explorer application. It provides an interactive interface to explore AI datasets, benchmarks, and tasks.

## Features

- **Dataset Explorer**: Browse through AI datasets with pagination
- **Detailed View**: View comprehensive details about each dataset
- **Benchmark Links**: Direct links to Papers With Code benchmarks
- **Filtering**: Filter datasets by task, area, modalities, and year
- **Statistics**: Visualize dataset distributions by task, year, and modality

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone this repository or download the files
2. Navigate to the project directory
3. Create a data directory and place your dataset CSV file in it:

```bash
mkdir -p data
# Copy your datasets.csv file to the data directory
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

Run the Streamlit application with:

```bash
streamlit run app.py
```

The application will start and open in your default web browser at `http://localhost:8501`.

## Data Format

The application expects a CSV file named `datasets.csv` in the `data` directory with the following columns:

- `sno`: Serial number
- `dataset_id`: Name of the dataset
- `description`: Description of the dataset
- `task`: Primary task
- `subtask`: Subtask (if applicable)
- `associated_tasks`: Comma-separated list of associated tasks
- `modalities`: Comma-separated list of modalities
- `homepage_url`: URL to the dataset homepage
- `pwc_url`: URL to the Papers With Code page
- `year_published`: Year the dataset was published
- `area`: Area of research
- `dataset_size`: Size of the dataset
- `license`: License information
- `languages`: Languages used in the dataset
- `paper_url`: URL to the research paper
- `benchmark_urls`: Comma-separated list of benchmark URLs

## Customization

You can customize the application by:

1. Modifying the styling in the CSS section at the top of `app.py`
2. Adding or removing filters in the `create_filter_panel` function
3. Changing the number of items displayed per page in the `items_per_page_options` list
4. Adding additional visualizations in the Statistics tab

## Comparison with React Version

This Streamlit implementation provides similar functionality to the React version but with:

- Simpler development workflow (Python-only)
- Built-in data visualization capabilities
- Automatic responsive design
- Slightly different UI aesthetics (Streamlit components vs. Material-UI)
- Integrated filtering and pagination controls
