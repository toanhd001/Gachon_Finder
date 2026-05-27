# 🏫 Gachon Campus Path & Resource Finder Pro

An advanced Data Structures and Algorithms final project built with **Python** and **Streamlit Web UI**. Optimized for modular multi-member collaboration at Gachon University (2026).

[👉 Đọc bản Tiếng Việt tại đây](./README_VI.md)

---

## 🚀 1. Quick Start Guide (For Team Members)

Follow these exact steps to set up the project on your local machine:

### Prerequisites

Ensure you have Python 3 installed on your system.

### Installation & Execution

```bash
# Step 1: Clone the repository
git clone <YOUR_REPOSITORY_URL>
cd Gachon_Finder

# Step 2: Create a virtual environment (Mandatory for Mac/Linux PEP 668)
python3 -m venv .venv

# Step 3: Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows (Command Prompt):
# .venv\Scripts\activate.bat

# Step 4: Install required dependencies
pip install -r requirements.txt

# Step 5: Run the Streamlit Web Application
streamlit run main.py
```

---

## 🌿 2. Git Branching & Commit Standards

### Branching Strategy

Never push directly to the `main` branch. Every member must work on their dedicated feature branch:

- Member 1: `feat/member1-navigation`
- Member 2: `feat/member2-booking`
- Member 3: `feat/member3-traffic`

### How to Work Daily without Conflicts

```bash
# 1. Sync your local main branch with GitHub
git checkout main
git pull origin main

# 2. Switch to your feature branch (or create it if it doesn't exist)
git checkout -b feat/memberX-your-feature

# 3. Write your code and test via Streamlit. Once stable, stage and commit:
git add .
git commit -m "feat: description of what you added"

# 4. Push your branch to GitHub
git push origin feat/memberX-your-feature

# 5. Open a Pull Request (PR) on GitHub and tag the Leader for review.
```

### Commit Message Convention

We follow the **Conventional Commits** specification. Your commit messages must start with one of these prefixes:

- `feat:` A new feature or UI enhancement (e.g., `feat: add bar chart for emergency logs`)
- `fix:` A bug fix (e.g., `fix: resolve mid-point index error in binary search`)
- `docs:` Documentation changes only (e.g., `docs: update readme instructions`)
- `style:` Code style updates (formatting, missing semi-colons, no production code change)

---

## 👥 3. Roles and Responsibilities (R&R)

To maximize our score on **"Prototype Completeness"**, each member is responsible for maintaining their specific algorithm logic file and enhancing their corresponding UI tab in `main.py`:

| Member | Core Module File | Target Algorithms & Data Structures | UI Enhancement Task |
| --- | --- | --- | --- |
| **Member 1** | `modules/navigation.py` | Graph Topology, Dijkstra, A* Search | Dynamic GraphViz network visualization with path highlighting (Red lines). |
| **Member 2** | `modules/booking.py` | Chaining Hash Table, BST, Quick Sort, Binary Search | Interactive classroom data table view with dynamic capacity filtering via sliders. |
| **Member 3** | `modules/traffic.py` | Priority Queue (Max-Heap), Heap Sort, Kruskal's MST | Statistical data analytics (e.g., Bar Charts) comparing risk metrics of emergency logs. |

---

> **Note:** If you install any new third-party Python library via pip, you MUST run `pip freeze > requirements.txt` before committing your code.
