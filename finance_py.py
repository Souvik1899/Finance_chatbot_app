import pandas as pd
import streamlit as st

# Load the cleaned financial data
try:
    df = pd.read_excel("BCGX project.xlsx")
    df["Year"] = df["Year"].astype(str)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Streamlit UI
st.set_page_config(page_title="Financial Chatbot", page_icon="💬")
st.title("💬 Financial Chatbot")
st.write("Ask predefined financial questions about Microsoft, Tesla, and Apple.")

# Sidebar for additional options
with st.sidebar:
    st.header("Options")
    show_charts = st.checkbox("Show charts", value=True)

query = st.selectbox("Choose a query:", [
    "Select a query",
    "What is the total revenue?",
    "How has net income changed?",
    "What are the total assets?",
    "What are the total liabilities?",
    "What is the cash flow from operating activities?"
])

if query != "Select a query":
    company = st.selectbox("Choose a company:", sorted(df["Company"].unique()))
    years = sorted(df["Year"].unique())
    
    if query == "How has net income changed?":
        year1 = st.selectbox("From year:", years, index=0)
        year2 = st.selectbox("To year:", years, index=1)
    else:
        year = st.selectbox("Year:", years)
    
    if st.button("Submit"):
        try:
            if query == "What is the total revenue?":
                value = df.loc[(df["Company"] == company) & (df["Year"] == year), "Total Revenue"].values[0]
                st.success(f"The total revenue for {company} in {year} was ${value:,}.")
                
                if show_charts:
                    st.subheader(f"Revenue Trend for {company}")
                    chart_data = df[df["Company"] == company].sort_values("Year")
                    st.bar_chart(chart_data.set_index("Year")["Total Revenue"])
                
            elif query == "How has net income changed?":
                ni1 = df.loc[(df["Company"] == company) & (df["Year"] == year1), "Net Income"].values[0]
                ni2 = df.loc[(df["Company"] == company) & (df["Year"] == year2), "Net Income"].values[0]
                
                if ni1 == 0:
                    if ni2 > 0:
                        st.success(f"Net income for {company} increased from $0 in {year1} to ${ni2:,} in {year2}.")
                    elif ni2 < 0:
                        st.success(f"Net income for {company} decreased from $0 in {year1} to -${abs(ni2):,} in {year2}.")
                    else:
                        st.success(f"Net income for {company} remained at $0 from {year1} to {year2}.")
                else:
                    change = ((ni2 - ni1) / abs(ni1)) * 100
                    direction = "increased" if change > 0 else "decreased"
                    st.success(f"Net income for {company} has {direction} by {abs(change):.2f}% from {year1} to {year2}.")
                    st.write(f"• {year1}: ${ni1:,}")
                    st.write(f"• {year2}: ${ni2:,}")
                
                if show_charts:
                    st.subheader(f"Net Income Trend for {company}")
                    chart_data = df[df["Company"] == company].sort_values("Year")
                    st.line_chart(chart_data.set_index("Year")["Net Income"])
                
            elif query == "What are the total assets?":
                value = df.loc[(df["Company"] == company) & (df["Year"] == year), "Total Assets"].values[0]
                st.success(f"The total assets of {company} in {year} were ${value:,}.")
                
                if show_charts:
                    st.subheader(f"Assets Trend for {company}")
                    chart_data = df[df["Company"] == company].sort_values("Year")
                    st.bar_chart(chart_data.set_index("Year")["Total Assets"])
                
            elif query == "What are the total liabilities?":
                value = df.loc[(df["Company"] == company) & (df["Year"] == year), "Total Liabilities"].values[0]
                st.success(f"The total liabilities of {company} in {year} were ${value:,}.")
                
                if show_charts:
                    st.subheader(f"Liabilities Trend for {company}")
                    chart_data = df[df["Company"] == company].sort_values("Year")
                    st.bar_chart(chart_data.set_index("Year")["Total Liabilities"])
                
            elif query == "What is the cash flow from operating activities?":
                value = df.loc[(df["Company"] == company) & (df["Year"] == year), "Cash Flow from Operating Activities"].values[0]
                st.success(f"The cash flow from operating activities for {company} in {year} was ${value:,}.")
                
                if show_charts:
                    st.subheader(f"Operating Cash Flow Trend for {company}")
                    chart_data = df[df["Company"] == company].sort_values("Year")
                    st.line_chart(chart_data.set_index("Year")["Cash Flow from Operating Activities"])
                
        except Exception as e:
            st.error(f"Error: {e}")
            st.error("Data not found. Please check the selected inputs.")

# Footer
st.markdown("---")
st.caption("Financial Chatbot - Data Analysis Tool")