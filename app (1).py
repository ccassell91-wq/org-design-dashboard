
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
employees = pd.read_excel("synthetic_org_100.xlsx", sheet_name="Employees", engine="openpyxl")
teams = pd.read_excel("synthetic_org_100.xlsx", sheet_name="Teams", engine="openpyxl")
org_edges = pd.read_excel("synthetic_org_100.xlsx", sheet_name="OrgEdges", engine="openpyxl")
employee_skills = pd.read_excel("synthetic_org_100.xlsx", sheet_name="EmployeeSkills", engine="openpyxl")
principles = pd.read_excel("synthetic_org_100.xlsx", sheet_name="Principles", engine="openpyxl")

# Set page config
st.set_page_config(page_title="Org Design Dashboard", layout="wide")

st.title("📊 Strategic HR Org Design Dashboard")

# Sidebar navigation
tab = st.sidebar.radio("Select View", ["Org Chart", "Team Metrics", "Skill Alignment", "Diversity Analysis", "Org Design Principles"])

if tab == "Org Chart":
    st.header("🧭 Org Chart")
    G = nx.DiGraph()
    for _, row in org_edges.iterrows():
        G.add_edge(row["ManagerID"], row["EmployeeID"])
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=8)
    st.pyplot(plt)

elif tab == "Team Metrics":
    st.header("📐 Team Size by Function")
    team_sizes = employees.groupby("ManagerID").size().reset_index(name="DirectReports")
    team_sizes = team_sizes.merge(employees[["EmployeeID", "FullName", "JobRole"]], left_on="ManagerID", right_on="EmployeeID")
    fig = px.bar(team_sizes, x="FullName", y="DirectReports", color="JobRole", title="Direct Reports per Manager")
    st.plotly_chart(fig, use_container_width=True)

elif tab == "Skill Alignment":
    st.header("🛠️ Skill Proficiency by Role")
    merged = employee_skills.merge(employees[["EmployeeID", "JobRole"]], on="EmployeeID")
    avg_skills = merged.groupby(["JobRole", "Skill"]).Proficiency.mean().reset_index()
    fig = px.bar(avg_skills, x="Skill", y="Proficiency", color="JobRole", barmode="group", title="Average Skill Proficiency by Role")
    st.plotly_chart(fig, use_container_width=True)

elif tab == "Diversity Analysis":
    st.header("🌍 Diversity Distribution")
    diversity = employees.groupby(["Ethnicity", "Gender"]).size().reset_index(name="Count")
    fig = px.sunburst(diversity, path=["Ethnicity", "Gender"], values="Count", title="Ethnicity & Gender Distribution")
    st.plotly_chart(fig, use_container_width=True)

elif tab == "Org Design Principles":
    st.header("📜 Org Design Principles")
    st.dataframe(principles)

