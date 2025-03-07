
import streamlit as st
import pandas as pd
import os
# import plotly.express as px
from io import BytesIO

# st.set_page_config(page_title="Data Sweeper", layout='wide')
# st.title("🚀 Data Sweeper and Converter")

# Custom Page Config & Title
st.set_page_config(page_title="Data Sweeper", layout='wide', initial_sidebar_state='expanded')

# Add Background Style
st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f4;
        }
        .main-title {
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
            color: #4CAF50;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
        .coder-name {
            text-align: center;
            font-size: 1.2em;
            color: #555;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

#  Add Banner Image
st.image("./farazpic.png", width=150)
st.markdown("<div class='coder-name'>👨‍💻 Developed by: Muhammad Faraz GIAIC </div>", unsafe_allow_html=True)



# Display Title and Coder Name
st.markdown("<div class='main-title'>🚀 Data Sweeper & Converter</div>", unsafe_allow_html=True)



st.write("Transform your files between CSV and Excel formats with built-in data cleaning, visualization, and insights!")

uploaded_files = st.file_uploader("📂Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue
        
        st.write(f"**📂File Name:** {file.name}")
        st.write(f"**📏File Size:** {file.size / 1024:.2f} KB")
        
        st.subheader("📊 Data Preview")
        st.dataframe(df.head())
        
        st.subheader("🧹 Smart Data Cleaning")
        if st.checkbox(f"Clean Data for {file.name}"):
            if st.button(f"🗑️ Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("✅ Duplicates Removed!")
            
            if st.button(f"Fill Missing Values for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("✅ Missing Values Filled!")
        
        st.subheader("Select columns to convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default = df.columns)
        df = df[columns]


        st.subheader("📈 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])


        # chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Scatter Chart", "Pie Chart"])
        # numeric_cols = df.select_dtypes(include='number').columns
        
        # if len(numeric_cols) >= 2:
        #     x_col = st.selectbox("X-axis Column", numeric_cols)
        #     y_col = st.selectbox("Y-axis Column", numeric_cols)
            
        #     if chart_type == "Bar Chart":
        #         fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Chart of {x_col} vs {y_col}")
        #     elif chart_type == "Scatter Chart":
        #         fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Chart of {x_col} vs {y_col}")
        #     elif chart_type == "Pie Chart":
        #         fig = px.pie(df, names=x_col, values=y_col, title=f"Pie Chart of {x_col}")
            
        #     st.plotly_chart(fig)
        
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)
            st.download_button(label=f"Download {file.name} as {conversion_type}", data=buffer, filename=file_name, mime=mime_type)

    st.success("✅ All files processed successfully!")