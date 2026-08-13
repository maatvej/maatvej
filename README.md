<div align="center">

  [![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&pause=1000&color=36BCF7&center=true&vCenter=true&width=750&lines=Senior+ML+%26+MLOps+Engineer;Data+Scientist+%7C+Applied+Mathematician;Backend+Developer+(Python+%2F+FastAPI);LLM+Agents+%26+Optimization+Specialist)](https://git.io/typing-svg)

  <p align="center">
    <b>Specializing in production MLOps systems, mathematical optimization, LLM agents, and high-performance analytical backends.</b>
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
    <img src="https://img.shields.io/badge/ClickHouse-FFCC00?style=for-the-badge&logo=clickhouse&logoColor=black" />
    <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  </p>
</div>

---

## Overview

Senior Engineer with expertise in designing, building, and deploying production-grade Machine Learning pipelines, mathematical optimization algorithms, LLM-driven autonomous agents, and high-performance backend services.

* **Machine Learning & Deep Learning:** Time-series demand forecasting (Temporal Fusion Transformers / PyTorch Lightning), hyperparameter tuning (Optuna with GPU trial pruning), classical machine learning (Scikit-Learn).
* **Applied Mathematics & Optimization:** Demand elasticity modeling, mathematical monotonic smoothing (Isotonic Regression, PCHIP Interpolation), multi-criteria optimization solvers (Multi-Choice Knapsack Problem / MCKP), reliability engineering (Weibull distributions, MLE parameter fitting via SciPy/Autograd/Lifelines), Monte Carlo life-cycle simulations.
* **LLM & Generative AI:** Autonomous Text-to-SQL agents (Anthropic Claude 3.5 Sonnet / OpenRouter), dynamic LLM Chart Planners for adaptive data visualization, step-by-step trace-based model observability.
* **Backend & API Architecture:** Clean Architecture, FastAPI, Async Python (`asyncio`, `aiosqlite`), SQLAlchemy ORM, Pydantic v2, Streaming API (Server-Sent Events).
* **Data Engineering & Databases:** PostgreSQL (bulk operations, transactional partition rotation), ClickHouse (Native & HTTPS interfaces), Parquet ETL pipelines, SQLite, Nexus Artifact Management.
* **MLOps & Engineering Infrastructure:** Docker & NVIDIA Container Toolkit (GPU execution inside containers), package management (`uv`, `poetry`), static analysis (Ruff, Mypy), testing (Pytest), standalone desktop packaging (PyInstaller).


## Technical Stack

| Domain | Tools & Technologies |
| :--- | :--- |
| **Languages & Core** | Python 3.10+, SQL, Shell/Bash, Makefile |
| **ML / AI / Optimization** | PyTorch, PyTorch Lightning, Temporal Fusion Transformer (TFT), Optuna, Scikit-Learn, SciPy, Autograd, Lifelines, Anthropic API, OpenRouter |
| **Backend & Web Frameworks** | FastAPI, Uvicorn, Pydantic v2, SQLAlchemy, Asyncio, REST API, Streaming API (SSE) |
| **Databases & Storage** | ClickHouse, PostgreSQL, SQLite, Parquet, Nexus Repository |
| **MLOps, CI/CD & Tooling** | Docker, NVIDIA Container Toolkit (GPU), `uv`, Poetry, PyInstaller, Pytest, Ruff, Mypy |
| **Data Processing & Analytics** | Pandas, NumPy, Matplotlib, Seaborn, OpenPyXL, XlsxWriter |

---

## Featured Projects & Experience

### 1. NeuroSpros B1 - Industrial Dynamic Pricing & Demand Forecasting System
*An end-to-end industrial MLOps system for demand forecasting, price elasticity curve fitting, and retail price optimization.*

* **Architecture:** Implemented using Clean Architecture principles, strict layer separation (DAL, features, models, business logic, and optimization layers).
* **Demand Forecasting:** Built on PyTorch Lightning using **Temporal Fusion Transformers (TFT)** with GPU-accelerated **Optuna** hyperparameter tuning and trial pruning.
* **Elasticity & Optimization Engine:** Applied **Isotonic Regression** and **PCHIP Interpolation** for demand curve monotonicity calibration, followed by a greedy multi-choice solver for the **Multi-Choice Knapsack Problem (MCKP)** to maximize margin under business constraints.
* **Data Pipelines & Storage:** High-performance ETL pipeline processing Parquet files via Nexus, automated PostgreSQL partition replacement, and atomic transactional database sessions.
* **Containerization:** Containerized pipeline deployment using Docker Compose with full NVIDIA GPU runtime support.

### 2. Retail Analytics Assistant (b-pn-agent)
*An intelligent analytics assistant converting natural language queries into optimized ClickHouse SQL with dynamic chart generation.*

* **Text-to-SQL Agent:** Powered by Anthropic Claude 3.5 Sonnet / OpenRouter to translate complex domain-specific questions into executable ClickHouse SQL queries.
* **Streaming API:** Built a Server-Sent Events (SSE) endpoint (`/api/query/stream`) providing real-time query progress feedback (Initialization, SQL Generation, DB Execution, Chart Planning, Final Result).
* **LLM Chart Planner:** Implemented an LLM decision module that evaluates SQL outputs and automatically selects appropriate chart types (`bar`, `line`, `doughnut`), axis mappings, and optimal orientations.
* **Observability:** Structured execution logging (`logs/model_traces/`) capturing prompts, model outputs, generated SQL queries, and database execution metadata.

### 3. WeibullTool - Equipment Reliability & Maintenance Optimization Platform
*A reliability engineering backend providing failure probability estimation, lifecycle Monte Carlo simulation, and preventive maintenance schedule optimization.*

* **Mathematical Estimation:** Estimated Weibull distribution parameters ($\alpha, \beta$) via Maximum Likelihood Estimation (MLE) using **SciPy**, **Autograd**, and **Lifelines**.
* **Monte Carlo Lifecycle Engine:** Simulated equipment lifecycle trajectories to estimate failure frequency, downtime, production losses, and monetary risk.
* **Backend Architecture:** Developed with **FastAPI**, **SQLite** (`aiosqlite`), **SQLAlchemy**, and strict **Pydantic** data schemas.
* **Desktop Distribution:** Packaged the application into a standalone client executable (`.exe`) using **PyInstaller** and **PyStray** for offline execution without requiring a local Python installation.
