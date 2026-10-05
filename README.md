<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/banner-dark.svg">
  <img src="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/banner-light.svg" width="100%" alt="Matvey Musatov — ML Engineer and Python Developer: demand forecasting, price optimization, LLM apps">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&duration=2800&pause=1400&color=38BDF8&center=true&vCenter=true&width=720&height=44&lines=Demand+forecasting+with+Temporal+Fusion+Transformers;Price+elasticity+%26+markdown+optimization;Text-to-SQL+assistants+over+ClickHouse;Speech+AI%3A+Whisper+%2B+speaker+diarization;FastAPI+%2F+Django+backends%2C+Polars+pipelines">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&duration=2800&pause=1400&color=0284C7&center=true&vCenter=true&width=720&height=44&lines=Demand+forecasting+with+Temporal+Fusion+Transformers;Price+elasticity+%26+markdown+optimization;Text-to-SQL+assistants+over+ClickHouse;Speech+AI%3A+Whisper+%2B+speaker+diarization;FastAPI+%2F+Django+backends%2C+Polars+pipelines" alt="Demand forecasting with Temporal Fusion Transformers · Price elasticity and markdown optimization · Text-to-SQL assistants over ClickHouse · Speech AI · FastAPI / Django backends">
</picture>

I build <b>production ML for retail pricing</b> — demand forecasting, price elasticity and markdown optimization —<br>
together with the analytical backends and LLM tools around them, owning components end to end:<br>
modelling and math, data pipelines, performance, tests and packaging.

</div>

## ⚡ Highlights

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/highlights-dark.svg">
  <img src="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/highlights-light.svg" width="100%" alt="6× faster markdown optimizer (882 s → 148 s); ~18× faster preprocessing after pandas → Polars; 229K demand curves per production run; 9 LLMs behind one Text-to-SQL assistant">
</picture>

## 🧭 What I do

- 🔮 **Forecasting & deep learning** — Temporal Fusion Transformers (PyTorch Lightning, pytorch-forecasting), GPU hyperparameter search with Optuna, fine-tuning of time-series foundation models (Chronos-T5), SARIMAX.
- 📐 **Applied math & optimization** — price-elasticity and promo-uplift curves (isotonic regression, PCHIP, non-linear least squares, LOWESS), greedy multiple-choice optimization under margin and turnover constraints, robust outlier handling.
- 🧠 **LLM & speech AI** — Text-to-SQL for ClickHouse with failure-driven guardrails, OpenAI-compatible APIs (Yandex Cloud AI Studio, Ollama), Faster-Whisper and pyannote speaker diarization.
- ⚙️ **Backend** — FastAPI, Django 5, Flask / Gunicorn, async SQLAlchemy 2, Pydantic v2, NDJSON / SSE streaming, multi-tenant API design.
- 🗄️ **Data engineering** — Polars (migrated a production pipeline from pandas), pandas, DuckDB, ClickHouse, PostgreSQL, SQLite star schemas, Parquet.
- 🚀 **MLOps & tooling** — Docker and Compose with NVIDIA GPUs, GitLab CI, `uv`, pytest (golden-output and equivalence tests), Ruff, mypy, PyInstaller.

## 💼 Experience

<sub>Client names are omitted. Each card shows the system as a whole; the section under it lists my own contribution.</sub>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/exp-pricing-dark.svg">
  <img src="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/exp-pricing-light.svg" width="100%" alt="Retail Markdown Pricing Pipeline (Jun 2026 – now): TFT demand forecasts → 21-scenario price curves → margin optimizer within turnover targets">
</picture>

<details>
<summary><b>My contribution</b> · calibration &amp; optimizer · 6× faster optimizer · pandas → Polars · Optuna on GPU</summary>
<br>

Production GPU pipeline that sets clearance (markdown) prices for a large retail chain. A Temporal Fusion Transformer forecasts weekly demand per SKU × store cluster, the model is re-run under 21 price scenarios to build demand-vs-price curves, and an optimizer assigns a discount to every SKU to maximize category margin within turnover (weeks-of-cover) targets. One production run covers ~284K stock rows in 222 categories and 229K demand curves (28.9M forecast rows).

- **Elasticity & optimization stages (primary author):** rewrote demand-curve calibration (base-demand normalization, isotonic regression, product/category gradient blending, uplift caps, PCHIP interpolators) and the greedy multiple-choice optimizer (moves ranked by Δturnover / Δmargin, snapshot backtracking, per-category parallelism with joblib); added a mode that optimizes directly on raw TFT curves.
- **Performance:** vectorized the optimizer's candidate scan in NumPy with pick-for-pick identical decisions — the largest category (22K rows) went from 882 s to 148 s, mid-size ones ~13× faster, with outputs unchanged on all 222 production categories; batched PCHIP calibration made the correction step 10× faster (13.6 s → 1.3 s on 13.6K curves).
- **pandas → Polars migration** of the pipeline package (78 files), verified bit-identical on 1.5M real sales rows (preprocessing ~18× faster), trained weights, forecasts, interpolators and optimizer output.
- **GPU hyperparameter search for TFT:** Optuna TPE + median pruning through a custom PyTorch Lightning callback, bf16 on NVIDIA H200, resumable studies and per-trial TensorBoard logs; shipped as a GPU Docker Compose service launched from GitLab CI.
- **Data quality & incidents:** built a DuckDB reconciliation tool that validated moving the sales source from PostgreSQL to ClickHouse; root-caused and fixed a silent demand-filter mismatch that cut optimizable SKU × cluster pairs from 28,077 to 922, and a 50× revenue gap between actuals and forecasts in the pricing UI.
- **Testing & docs:** golden-output and reference-equivalence tests (243 passing; a mutation check caught 10 of 10 planted bugs), system documentation and a pipeline review with measured bottlenecks and a prioritized fix plan.

**Stack:** Python 3.12, PyTorch Lightning, pytorch-forecasting, Optuna, Polars, NumPy, SciPy, scikit-learn, DuckDB, PostgreSQL, ClickHouse, Nexus, Docker (NVIDIA GPU), GitLab CI.

</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/exp-text2sql-dark.svg">
  <img src="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/exp-text2sql-light.svg" width="100%" alt="LLM Text-to-SQL Assistant (Apr – Jun 2026): business questions in plain Russian → ClickHouse SQL → a table, a chart and a commentary">
</picture>

<details>
<summary><b>My contribution</b> · SQL-generation prompt · 9 switchable LLMs · result post-processing · streaming</summary>
<br>

Russian-language assistant for a retailer's pricing team: questions in plain language become ClickHouse SQL, and answers come back as a table, a chart and a short commentary (sales, stock, dead stock, markdowns, margin, turnover). It started as a fixed streaming pipeline (question → SQL → database → chart) and later evolved into a tool-calling agent.

- **SQL-generation prompt (main contributor):** schema and join-key documentation, business glossary and metric formulas (revenue, margin, turnover, stock value), few-shot query templates, and guardrails derived from real failures — ClickHouse errors 184 / 215 / 352, alias shadowing, duplicate-safe joins, an anti-join pattern for "no sales" questions, dates anchored to the latest loaded data, explicit lists of non-existent columns against hallucinations.
- **LLM provider integration:** connected Yandex Cloud AI Studio through the OpenAI-compatible SDK with per-request switching between 9 hosted models (GPT-OSS 120B / 20B, YandexGPT 5, DeepSeek, Alice AI); wrote a smoke-evaluation harness that logs generated SQL, token usage, LLM latency and DB time on a set of domain questions.
- **Result post-processing:** LLM-generated localized column labels with display types, and multi-series chart planning validated against the actual result columns — both reused by the team's later tool-calling agent.
- **Streaming & serving:** step-level progress events in the NDJSON stream with a ClickHouse → demo-data fallback and keep-alive pings for long queries; moved serving from the Flask dev server to Gunicorn; added token-usage and raw-output steps to the per-request JSON traces.
- **Multi-turn dialogue:** conversation history injected into the SQL prompt with pronoun-resolution rules, so follow-up questions resolve to concrete filters.

**Stack:** Python, OpenAI SDK, Yandex Cloud AI Studio, ClickHouse, Flask, Gunicorn, Docker, GitLab CI.

</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/exp-reliability-dark.svg">
  <img src="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/exp-reliability-light.svg" width="100%" alt="Equipment Reliability & PM Planning (Jan – Feb 2026): censored Weibull fits, Monte Carlo life cycles and budget-cut maintenance plans in one offline executable">
</picture>

<details>
<summary><b>My contribution</b> · backend owner · reliability-core integration · Excel in/out · single-file .exe</summary>
<br>

Tool for planning preventive maintenance (PM) of industrial equipment fleets: it fits right-censored Weibull models to failure and maintenance history, simulates equipment life cycles with Monte Carlo, compares Base vs Optimized PM plans under a budget cut, and reports availability, failure costs and production losses. Ships as a single Windows executable that works offline.

- **Backend owner:** bootstrapped the FastAPI REST API (6 of 8 router modules), the async SQLAlchemy + aiosqlite persistence layer and Pydantic v2 schemas with field-level constraints.
- **Math integration:** wired the team's reliability core — Weibull MLE (SciPy + Autograd Hessian for confidence bands), Kaplan–Meier curves (lifelines), Monte Carlo life-cycle simulator, PM-schedule optimizer — into the service layer, with per-group α / β persistence and Base vs Optimized scenario runs.
- **Data in, reports out:** Excel ingestion and validation (required columns, types, date logic, per-column statistics), cross-checks of user parameters against the uploaded data, and multi-sheet Excel reports with a Base / Optimized / Delta comparison.
- **Desktop distribution:** packaged the backend and the Vite-built SPA into a single-file executable (PyInstaller) with a PyStray tray launcher — no Python or Node.js needed on the target machine.
- **Quality:** end-to-end API tests (pytest-asyncio, httpx ASGITransport, in-memory SQLite) and the API contract docs used by the frontend team.

**Stack:** Python, FastAPI, SQLAlchemy (async), aiosqlite, Pydantic v2, pandas, SciPy, lifelines, openpyxl / XlsxWriter, PyInstaller, PyStray.

</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/exp-elasticity-dark.svg">
  <img src="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/exp-elasticity-light.svg" width="100%" alt="Promo Elasticity & Pricing Simulator (Oct 2025 – Jan 2026): uplift-vs-discount curves, what-if price simulations and profit-optimal discounts for FMCG">
</picture>

<details>
<summary><b>My contribution</b> · main backend developer · uplift model · multi-tenancy · performance</summary>
<br>

Platform for an FMCG manufacturer's pricing team: promo elasticity (sales uplift vs discount depth) by segment, a target brand vs its competitors, what-if discount and price-index simulations with a search for the profit-optimal discount, EDA, and demand forecasts (SARIMAX, TFT, PatchTST). FastAPI + React, Docker Compose; ~1.4M weekly sales records across 11.5K SKUs. Authored ~70% of the project's commits, including 7 of its 17 REST endpoints.

- **Promo-uplift model:** sales-weighted uplift curves fitted by bounded non-linear least squares (log curve, SciPy `curve_fit`) and made monotonic with isotonic regression; a 5-level hierarchical fallback for sparse segments; two-stage outlier filtering (99.5th-percentile cap + per-segment IQR).
- **Multi-tenancy:** turned a single-client prototype into a multi-company service — normalized SQLite star schema (company-scoped dimensions, foreign keys, indexes), tenant scoping across all data endpoints, repository / config / logging layers and chunked ETL CLIs; onboarded 3 company datasets.
- **Performance:** targeted SQL aggregations instead of full-table loads, a shared `ProcessPoolExecutor` with `asyncio.gather` fan-out instead of a new process pool per request, and 5 analytics endpoints merged into one that loads the data once.
- **Analytics & forecasting features:** revenue and margin dynamics, historical promo profitability by discount bucket, a price-index response curve vs competitors, a scenario simulator on TFT forecasts, PatchTST forecast loading and a tenant-scoped SARIMAX batch job.

**Stack:** Python, FastAPI, pandas, NumPy, SciPy, scikit-learn, statsmodels, SQLAlchemy, SQLite, Docker Compose.

</details>

## 🧪 Personal projects

<p>
<a href="https://github.com/maatvej/Eidos"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/proj-eidos-dark.svg">
  <img src="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/proj-eidos-light.svg" width="100%" alt="Eidos — Offline-First Meeting AI: recordings → speaker-attributed transcripts, summaries, decisions and action items, fully local">
</picture></a>
</p>

<p>
<a href="https://github.com/maatvej/tg-sticker-bot"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/proj-stickers-dark.svg">
  <img src="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/proj-stickers-light.svg" width="49%" alt="Sticker Converter Bot: Telegram bot converting static, Lottie and video stickers to PNG, GIF, APNG, WebP or WebM">
</picture></a>
<a href="https://github.com/maatvej/chronos-fine-tune"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/proj-chronos-dark.svg">
  <img src="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/proj-chronos-light.svg" width="49%" alt="Chronos-T5 Fine-Tuning: full fine-tuning of Chronos-T5-Large for retail sales forecasting">
</picture></a>
</p>

<details>
<summary><b>Project details</b> · speech pipeline &amp; voice memory · local LLMs · sticker media pipeline · Chronos fine-tuning</summary>
<br>

**[Eidos](https://github.com/maatvej/Eidos)** — self-hosted platform that turns meeting recordings into speaker-attributed transcripts with word timestamps, summaries, decisions, action items and sentiment, with all ML running locally.

- **Speech pipeline:** FFmpeg cleanup (band-pass, FFT denoise, EBU R128 loudness) → Faster-Whisper large-v3-turbo (GPU fp16 / CPU int8, Silero VAD, word timestamps) → pyannote diarization with a Ward-clustering fallback → word-to-speaker alignment.
- **Voice memory:** speaker embeddings written from scratch in NumPy (32-dim: MFCC, pitch, formant ratios, spectral features) with cosine matching and running-average profiles — renamed speakers are recognized automatically in later recordings.
- **Privacy-first LLM layer:** JSON-mode client for local OpenAI-compatible LLMs (Ollama) that refuses non-private hosts, plus a dependency-free LexRank summarizer fallback for Russian and English.
- **Architecture:** custom ASGI dispatcher combining Django 5 (admin, allauth) and FastAPI (REST + SSE progress) with shared session / JWT auth; React 19 + TypeScript + Zustand SPA with an audio-synced transcript player; export to TXT, SRT, VTT, JSON, PDF and DOCX.
- **Quality:** 152 pytest and 85 Vitest tests, Ruff with 39 rule families (incl. Bandit security rules), and a custom cProfile toolkit with bottleneck diagnosis.

**[Telegram Sticker Converter Bot](https://github.com/maatvej/tg-sticker-bot)** — async aiogram 3 bot that converts static (WebP), animated (Lottie / TGS) and video (VP9 WebM) stickers to PNG, GIF, APNG, WebP or WebM with transparency preserved. Media pipeline on rlottie, ffmpeg and Pillow: disk-buffered frames, alpha-preserving VP9 decoding, flicker-free GIFs (global palette + ordered dithering), CPU work in worker threads under a concurrency limit; 58 pytest cases including network-free end-to-end tests.

**[Chronos-T5 Fine-Tuning](https://github.com/maatvej/chronos-fine-tune)** — full fine-tuning of the Chronos-T5-Large time-series foundation model (Hugging Face Trainer, AdamW, cosine schedule) for 8-step-ahead sales forecasting, with a streaming data pipeline that turns a 14.9M-row Parquet table into 182K continuous series, and probabilistic evaluation (20 sample paths, median forecast, zero-aware WAPE).

</details>

## 🧰 Tech stack

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/stack-dark.svg">
  <img src="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/stack-light.svg" width="100%" alt="Tech stack — ML & forecasting: PyTorch, Lightning, TFT, Optuna, scikit-learn, statsmodels, SciPy, Transformers. Data: Polars, pandas, NumPy, DuckDB, ClickHouse, PostgreSQL, SQLite, Parquet. LLM & speech: OpenAI-compatible APIs, Yandex AI Studio, Ollama, Faster-Whisper, pyannote.audio, FFmpeg. Backend: FastAPI, Django, Flask, Pydantic v2, SQLAlchemy, aiogram. MLOps: Docker, CUDA GPUs, GitLab CI, uv, Ruff, pytest, Git, Linux. Languages & frontend: Python, SQL, TypeScript, Bash, React, Vite, Tailwind CSS, Vitest">
</picture>

## 🎓 Coursework

- 🌀 **Diffusion models** ([generative-ai](https://github.com/maatvej/generative-ai)) — DDPM components in PyTorch: forward noising, posterior, ε-prediction loss, ancestral sampling, plus classifier-free guidance and respaced sampling; class-conditional U-Net on MNIST with sampling cut from 1,000 to 100 steps.
- 📚 **Recommender systems** ([RS-homework](https://github.com/maatvej/RS-homework)) — popularity, TF-IDF content, item-item CF, SVD (test RMSE 0.84) and a Keras neural CF model on Goodbooks-10k (~982K ratings), with Precision / Recall / nDCG@10 evaluation and a weighted hybrid ranker.
- 🕹️ **Reinforcement learning** ([RL-session](https://github.com/maatvej/RL-session)) — PPO vs A2C and a network-size study on Gymnasium LunarLander-v3 with Stable-Baselines3, with learning curves and rollout videos.

<sub>More study notebooks — math, statistics, classical ML — are in my <a href="https://github.com/maatvej?tab=repositories">repositories</a>.</sub>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/footer-dark.svg">
  <img src="https://raw.githubusercontent.com/maatvej/maatvej/main/assets/footer-light.svg" width="100%" alt="">
</picture>
