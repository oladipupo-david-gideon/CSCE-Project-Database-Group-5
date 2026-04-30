# 🚗 Auto Company Database System — Team 5

> **CSCE 4350 – Database Systems** | University of North Texas  
> A unified CLI application backed by a PostgreSQL database hosted on Supabase.

---

## 👥 Team Members & Responsibilities

| Name | Role | Folder | Responsibilities |
| :--- | :--- | :--- | :--- |
| **David Oladipupo** | Integration & Marketing Lead | `src/marketing/` & `sql/` | Repo setup, master DB connection script, Master Login Menu, Marketing OLAP CLI, complex defect/inventory queries, `.env` configuration |
| **Shegofa Ahmadi** | Customer Interface Developer | `src/customer/` | Online Customer CLI — inventory search & mock purchases, Project Presenation |
| **Snehitha Paruchi** | Dealer Interface Developer | `src/dealer/` | Vehicle Locator CLI — local/global stock & sales processing, Project Presenation|
| **Ronitkumar Sabhaya** | Project Manager & DBA | `src/dba` & `auto-company-db/tests` | DB management, DBA CLI Menu, unit tests & configuration, checkpoint submissions |

---

## ⚙️ Local Setup & Installation

### 1. Install Dependencies
Make sure your Python virtual environment is active, then run:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the `auto-company-db\src` folder with the following:
```env
DB_HOST=aws-1-us-east-2.pooler.supabase.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.yhatilhoqfnmmyictnyz
DB_PASS=your_actual_password_here
```
Or the `.env` file will come with the zip submitted to Canvas

### 3. Run the Application
```bash
python main.py
```

---

## 📅 Development Schedule

**Target Deadline: April 30**

### Phase 1 — Foundation & Initial Interfaces

| Date | Phase | Task | Assignee |
| :--- | :--- | :--- | :--- |
| Apr 8 | Setup | Repo setup, DB connection class, basic UI menus | David Oladipupo |
| Apr 9–13 | Dev Phase 1 | Build Marketing & Customer Interfaces | David & Shegofa |
| Apr 14–15 | CP2 Check-in | Test compiled interfaces for Checkpoint 2 | Ronitkumar Sabhaya |
| **Apr 17** | **Checkpoint 2** | **Submit relational schema, UI plans, and schedule** | **Ronitkumar Sabhaya** |

### Phase 2 — Architecture & SQL Implementation

| Date | Phase | Task | Assignee |
| :--- | :--- | :--- | :--- |
| Apr 18–19 | Architecture | Convert all menu code to standardized OOP class structure | Entire Team |
| Apr 20–24 | SQL Implementation | Add active SQL execution to Python class methods (replace print placeholders) | Entire Team |
| Apr 25–27 | Integration | Test Supabase connection pooler; verify concurrent DB transactions | David & Entire Team |

### Phase 3 — Final Delivery

| Date | Phase | Task | Assignee |
| :--- | :--- | :--- | :--- |
| Apr 26–29 | Bug Squashing | Fix broken queries, update E-R diagram, final tests | Entire Team |
| Apr 27–29 | Presentation Prep | Create project slides (Canva/PowerPoint) | Snehitha Paruchi |
| **Apr 30** | **Checkpoint 3 / Final Delivery** | **Submit `Project-Team5.zip` and presentation to Canvas** | **Ronitkumar Sabhaya** |

---

## 🌿 Git Workflow

> **Never push directly to `main`.** Follow the branch workflow below.

### Rules
1. **`main` is production-only** — only merge code that is 100% complete and reviewed.
2. **Pull from `dev` daily** — always sync before starting work to avoid conflicts.
3. **Branch off `dev`** — create a feature branch for every task:
```bash
   git checkout -b feature/your-feature-name
```
4. **Open a Pull Request into `dev`** — once your feature works, request a review before merging.

### Quick Reference
```bash
# Sync with the latest dev branch
git checkout dev
git pull origin dev

# Create your feature branch
git checkout -b feature/customer-menu

# After your work is done, push and open a PR
git push origin feature/customer-menu
```

---

*Check the `README.md` inside your assigned folder for feature-specific instructions.*
