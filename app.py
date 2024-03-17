import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def trim_label(label, max_length=10):
    if len(label) > max_length:
        return label[:max_length] + '...'
    else:
        return label

# Set page configuration
st.set_page_config(page_title="DataDash", layout="wide")


st.markdown("<h1 style='text-align: center; color: #1f77b4;'>DataDash</h1>", unsafe_allow_html=True)

# Get user input
data = st.file_uploader("Upload a file for data visualization", type=['csv', 'xlsx', 'json'])

if data is not None:
    try:
        if data.type == 'text/csv':
            df = pd.read_csv(data)
        elif data.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':  # Excel file
            df = pd.read_excel(data)
        elif data.type == 'application/json':  # JSON file
            df = pd.read_json(data)
        else:
            st.error("Unsupported file type. Please upload a CSV, Excel, or JSON file")

        # Display the DataFrame
        st.write(df)

        # Divide the app into two columns
        col1, col2 = st.columns([1, 3])

        with col1:
            # Get the column for the x-axis
            x_col = st.selectbox("Select x-axis column", df.columns)

            # Get the columns for the y-axis (multiselect)
            y_cols = st.multiselect("Select y-axis columns", df.columns, default=df.columns[1])

            # Get the option to select all rows
            select_all_rows = st.checkbox("Select all rows")

            # If select_all_rows is True, use all rows, otherwise allow selection
            if select_all_rows:
                selected_rows = df[x_col].astype(str).tolist()  # Convert integers to strings
            else:
                # Get the rows to include (multiselect)
                selected_rows = st.multiselect("Select rows to include", df[x_col].astype(str).tolist(), default=df[x_col].astype(str).tolist()[:10])

        with col2:
            # Filter the DataFrame based on selected rows
            filtered_df = df[df[x_col].astype(str).isin(selected_rows)]  # Convert integers to strings

            # Create the line plot
            fig, ax = plt.subplots(figsize=(12, 6))  # Increase the figure size further
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Custom colors
            markers = ['o', 's', '^', 'x', '+']
            for i, y_col in enumerate(y_cols):
                line_style = '-' if i == 0 else '--'  # Use solid line for the first line, dashed lines for others
                ax.plot(filtered_df[x_col], filtered_df[y_col], label=y_col, color=colors[i % len(colors)], marker=markers[i % len(markers)], linestyle=line_style, linewidth=2, markersize=8)

            ax.set_xlabel(x_col, fontsize=14, fontweight='bold')
            ax.set_ylabel("Values", fontsize=14, fontweight='bold')
            ax.set_title("Line Plot", fontsize=16, fontweight='bold')
            ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', ncol=1, frameon=True, fancybox=True, shadow=True)  # Move the legend outside the plot and add styling

            # Customize grid lines
            ax.grid(True, linestyle='--', alpha=0.8, color='gray')

            # Set the x-ticks and x-tick labels to the selected rows
            ax.set_xticks(range(len(selected_rows)))
            ax.set_xticklabels([trim_label(label) for label in selected_rows], rotation=45, ha='right', fontsize=10)  # Apply trim_label to all labels
            ax.margins(x=0.05)  # Add some margin to the x-axis

            # Adjust the layout and spacing to prevent overlapping labels
            plt.subplots_adjust(bottom=0.2, left=0.1, right=0.8, top=0.9)  # Adjust margins and spacing

            # Set background color and spines
            ax.set_facecolor('whitesmoke')
            ax.spines['bottom'].set_color('gray')
            ax.spines['top'].set_color('gray')
            ax.spines['right'].set_color('gray')
            ax.spines['left'].set_color('gray')

            # Format y-axis tick labels
            ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.2f}'))

            # Display the plot in Streamlit
            st.pyplot(fig)

    except TypeError as e:
        st.warning(f"An error occurred while processing the file: {e}. Please try to use other columns")














