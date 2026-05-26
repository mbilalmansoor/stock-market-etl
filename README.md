# 📈 Automated Stock Market ETL Pipeline

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![DuckDB](https://img.shields.io/badge/Database-DuckDB-orange?style=for-the-badge)
![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub_Actions-black?style=for-the-badge&logo=githubactions)
![uv](https://img.shields.io/badge/Package_Manager-uv-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

### Fully Automated • Serverless • Zero-Cost Data Engineering Pipeline

*A production-style ETL system that autonomously collects, transforms, and stores daily stock market data using modern cloud-native tooling.*

</div>

---

# ✨ Overview

This project demonstrates how a modern data pipeline can be built entirely on free-tier infrastructure while still following real-world engineering practices.

The system automatically:

- Extracts fresh stock market data every weekday
- Cleans and transforms incoming records
- Stores historical datasets inside DuckDB
- Commits updated datasets back to the repository
- Runs autonomously using GitHub Actions

The entire workflow executes without maintaining servers, containers, or cloud infrastructure.

---

# 🏗️ System Architecture

```text
        ┌─────────────────────────────┐
        │  GitHub Actions Scheduler  │
        │   Runs Weekdays @ 11 PM    │
        └─────────────┬──────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │     Python ETL Pipeline     │
        │  Extract • Transform • Load │
        └─────────────┬──────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │        DuckDB Storage       │
        │  Embedded Analytical Engine │
        └─────────────┬──────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │      GitHub Automation      │
        │  Commit + Persist Changes   │
        └─────────────────────────────┘
```

---

# ⚙️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Orchestration | GitHub Actions | Scheduled serverless execution |
| Runtime Management | uv | Fast dependency synchronization |
| Data Processing | Python 3.10 | ETL logic |
| Storage Engine | DuckDB | Embedded analytical database |
| Version Control | Git + GitHub | Dataset persistence |
| Scheduling | Cron Jobs | Automated execution |

---

# 🚀 Key Engineering Highlights

## ✅ Fully Serverless Architecture

The pipeline operates entirely on ephemeral GitHub-hosted runners.

No:
- VPS
- Docker server
- Cloud VM
- Kubernetes cluster
- Paid infrastructure

---

## ⚡ Fast Environment Provisioning with `uv`

Traditional Python CI environments are often slowed by dependency installation.

This project uses:

```bash
uv sync
```

to provision isolated environments significantly faster than conventional `pip` workflows.

---

## 🔒 Automated GitHub Persistence

The workflow safely writes transformed datasets back into the repository using GitHub Actions bot permissions.

### Challenges Solved

- GitHub token permission failures
- Repository write authorization
- Safe automated commits
- CI recursion prevention

---

## 🔄 Infinite Workflow Loop Protection

Automated commits can recursively retrigger workflows.

This was mitigated using:

```text
[skip ci]
```

which prevents unnecessary execution cycles after bot-generated commits.

---

# 📂 Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── etl.yml
│
├── cron_job.py
├── stock_data.duckdb
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# 🧠 ETL Workflow

## Extract

- Pulls fresh stock market data from external sources
- Runs automatically every trading day

## Transform

- Cleans incoming records
- Prevents duplicate inserts
- Standardizes schema formatting

## Load

- Persists datasets into DuckDB
- Commits updated database snapshots into GitHub

---

# 🚀 Local Development

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

---

## Install Dependencies

```bash
uv sync
```

---

## Execute Pipeline

```bash
uv run python cron_job.py
```

---

# 📊 Why DuckDB?

This project intentionally uses DuckDB because it provides:

- Extremely fast analytical queries
- Zero external database infrastructure
- Portable single-file storage
- Efficient columnar execution
- Perfect fit for lightweight ETL systems

---

# 📈 Future Enhancements

Planned improvements include:

- Data quality validation layer
- Automated anomaly detection
- Financial dashboards
- Historical trend visualization
- Parquet export support
- CI-based testing suite
- Partitioned historical datasets

---

# 🎯 What This Project Demonstrates

This repository showcases practical experience with:

- Data Engineering
- ETL Pipeline Design
- CI/CD Automation
- Cloud-Native Workflows
- Serverless Infrastructure
- Workflow Orchestration
- Analytical Databases
- Production Automation

---

# 📜 License

MIT License

---

<div align="center">

### Built with Python, DuckDB, and GitHub Actions

⭐ If you found this project interesting, consider starring the repository.

</div>
