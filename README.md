<div align="center">
  <a href="https://github.com/anshulsharma200817-svg">
    <img src="assets/header.svg" width="850" alt="Anshul Sharma - Full Stack &amp; Machine Learning Engineer" />
  </a>
</div>

<br />

## 🌌 Welcome, Programmer!
I am **Anshul Sharma**, a C-Rank software developer and machine learning practitioner. 
I specialize in building intelligent applications, starting from custom machine learning classification pipelines 
and metaheuristic optimizers to immersive, gamified discipline platforms and comprehensive Astro-based engineering applications.

*(Rank Progression: E ➔ D ➔ **[C]** ➔ B ➔ A ➔ S. Higher stats unlock higher ranks!)*

I thrive on taking complex engineering challenges (like building secure, compliant intelligence software for law enforcement) 
and distilling them into robust, clean, and highly user-friendly digital systems.

#### 🎯 Current Active Quests:
* 🛡️ **Threat Detection:** Advancing real-time NLP classification models for dark-social analysis.
* ⚡ **Performance Tuning:** Optimizing relational database architectures and background workers.
* 🎨 **Creative Interfaces:** Designing micro-animations and browser audio synthesizers (Web Audio API).

<br />

<div align="center">
  <h3>⚡ System Dashboard</h3>
  <table border="0" cellpadding="0" cellspacing="0">
    <tr>
      <!-- Column 1: Status Card -->
      <td align="center" valign="top" width="460">
        <img src="assets/stats.svg" width="450" alt="The System - Programmer Status Card" />
      </td>
      <!-- Column Spacing -->
      <td width="20"></td>
      <!-- Column 2: LeetCode Card -->
      <td align="center" valign="top" width="460">
        <a href="https://leetcode.com/u/anshulsharma200817-svg/" target="_blank">
          <img src="assets/leetcode.svg" width="450" alt="LeetCode Quest Progress Card" />
        </a>
      </td>
    </tr>
  </table>
</div>

<br />
<hr style="border: 1px solid #1f2937;" />
<br />

## 🚀 Highlighted Campaigns (Featured Projects)

### 🦅 NarcoScope AI — Dark Social Intelligence Platform
> **Client / Target:** Gwalior Police Cybercell (Hackathon Innovation)
* **Description:** An AI-powered threat detection platform built to monitor and flag illegal drug-trafficking activities across Telegram channels and uploaded Instagram/WhatsApp chat logs.
* **Core Technology:** React (Vite/Tailwind), Django REST Framework, SQLite, Python NLP Pipeline (SGD Classifier & Regex Rules), Telethon (live scraping), SHA-256 evidence hashing.
* **Key Achievement:** Achieved **0.97 Precision & 1.0 Recall** on held-out test sets. Correlates accounts across platforms using payment handles (UPI IDs) and compiles tamper-proof, legal evidence dossiers.
* **Architecture Diagram:**

```mermaid
graph TD
    %% Node Definitions
    Telegram[📱 Telegram Live API]
    Instagram[📸 Instagram Import]
    WhatsApp[💬 WhatsApp Import]
    ReactDashboard[💻 React/Vite Dashboard]
    DjangoAPI[⚙️ Django REST API]
    SQLiteDB[(🗄️ SQLite Database)]
    LiveScraper[🕷️ Live Scraper - Telethon]
    Rules[🔍 Rule-Based Matcher]
    ML[🤖 SGD ML Classifier]
    LLM[🧠 LLM Validator]
    Correlation[🔗 UPI Payment Linker]
    SHA[🔒 SHA-256 Hashing]
    Dossier[📄 Legal Dossier Generator]

    %% Flow Layout
    Telegram -->|Live Feed| LiveScraper
    Instagram -->|Manual Upload| ReactDashboard
    WhatsApp -->|Manual Upload| ReactDashboard
    LiveScraper --> DjangoAPI
    ReactDashboard -->|API Calls| DjangoAPI
    DjangoAPI --> SQLiteDB
    
    %% Engine Pipeline
    DjangoAPI -->|Analyze Message| Rules
    Rules -->|Flagged / Confident| Correlation
    Rules -->|Ambiguous| ML
    ML -->|Flagged / Confident| Correlation
    ML -->|Still Ambiguous| LLM
    LLM --> Correlation
    
    %% Correlation and Dossier
    Correlation -->|Link Operators| SHA
    SHA -->|Hash Messages| Dossier

    %% Node Custom Styles (Matching GitHub Dark Mode)
    style Telegram fill:#1e293b,stroke:#0284c7,stroke-width:1px,color:#38bdf8
    style Instagram fill:#1e293b,stroke:#db2777,stroke-width:1px,color:#f472b6
    style WhatsApp fill:#1e293b,stroke:#059669,stroke-width:1px,color:#34d399
    style ReactDashboard fill:#1e293b,stroke:#3b82f6,stroke-width:1.5px,color:#38bdf8
    style DjangoAPI fill:#1e1b4b,stroke:#8b5cf6,stroke-width:1.5px,color:#c084fc
    style SQLiteDB fill:#0f172a,stroke:#334155,stroke-width:1px,color:#94a3b8
    style LiveScraper fill:#0f172a,stroke:#e11d48,stroke-width:1.5px,color:#fda4af
    style Rules fill:#1c1917,stroke:#ca8a04,stroke-width:1.2px,color:#fde047
    style ML fill:#1e1b4b,stroke:#4f46e5,stroke-width:1.5px,color:#a5b4fc
    style LLM fill:#311042,stroke:#d946ef,stroke-width:1.5px,color:#f472b6
    style Correlation fill:#1c1917,stroke:#b45309,stroke-width:1.5px,color:#fcd34d
    style SHA fill:#0f172a,stroke:#10b981,stroke-width:1.5px,color:#34d399
    style Dossier fill:#111827,stroke:#64748b,stroke-width:2px,color:#f8fafc
```

### ▓ THE SYSTEM — RPG Discipline Tracker
> **Theme:** Solo Leveling RPG Gamification Dashboard
* **Description:** A gamified habit and productivity engine designed to translate daily tasks into S-Rank quests, awarding XP, level ups, and medals.
* **Core Technology:** FastAPI backend, SQLite, Vanilla HTML/CSS/JS frontend, Web Audio API.
* **Key Achievement:** Synthesizes low-rumble audio overlays using browser sound oscillators on boot. Features streaks, bosses, character stats progression, and scheduled SQLite backups.

### 📊 AMO-HO (CardioInsight) — Feature Selection Optimization
> **Field:** Machine Learning Research & Healthcare
* **Description:** A research-grade machine learning platform introducing **Adaptive Multi-Objective Hybrid Optimization** for feature selection in clinical heart disease predictions.
* **Core Technology:** Python (Scikit-Learn), Streamlit frontend, SHAP Explainability.
* **Key Achievement:** Combines 7 bio-inspired metaheuristics (GA, HHO, SMA, AO) with contribution weights to produce feature subsets that are **2.15× more stable** than baseline feature selectors.

### 🧠 AI-Powered Study Planner & Architecture Pipeline
> **Field:** Intelligent Systems & Cloud Architecture
* **Description:** A full-stack AI-driven study planning platform that parses user syllabus and goals, executes RAG query retrieval from a vector store, and utilizes LLMs (Gemini/OpenAI API) to output dynamic study plans, charts, quizzes, and gamified progress tracking.
* **Core Technology:** Next.js (React), Django REST Framework (Python), PostgreSQL, Redis Cache, Celery Queue, Gemini/OpenAI API, RAG Vector Search.
* **Architecture Diagram:**

```mermaid
graph TD
    %% Node Definitions
    User([👤 User])
    Frontend[💻 Next.js Frontend]
    Auth{🔑 REST / JWT}
    API[⚙️ Django REST API]
    DB[(🗄️ PostgreSQL)]
    Cache[(⚡ Redis Cache)]
    Celery[(⏱️ Celery Queue)]
    UserData[📊 User Data and Progress]
    AIService[🧠 AI Service Layer]
    Gemini[🤖 Gemini / OpenAI]
    RAG[📚 RAG Vector Store]
    Plan[📝 Study Plan Generation]
    Analytics[📈 Charts • Quizzes • Analytics]

    %% Flow Layout
    User -->|Interacts| Frontend
    Frontend --> Auth
    Auth --> API
    API --> DB
    API --> Cache
    API --> Celery
    DB --> UserData
    UserData --> AIService
    AIService --> Gemini
    AIService --> RAG
    Gemini --> Plan
    RAG --> Plan
    Plan --> Analytics

    %% Node Custom Styles (Matching GitHub Dark Mode)
    style User fill:#3b82f6,stroke:#2563eb,stroke-width:1.5px,color:#fff
    style Frontend fill:#1e293b,stroke:#3b82f6,stroke-width:1.5px,color:#38bdf8
    style Auth fill:#0f172a,stroke:#10b981,stroke-width:1.5px,color:#34d399
    style API fill:#1e1b4b,stroke:#8b5cf6,stroke-width:1.5px,color:#c084fc
    style DB fill:#0f172a,stroke:#334155,stroke-width:1px,color:#94a3b8
    style Cache fill:#0f172a,stroke:#ef4444,stroke-width:1px,color:#f87171
    style Celery fill:#0f172a,stroke:#f97316,stroke-width:1px,color:#fb923c
    style UserData fill:#0f172a,stroke:#06b6d4,stroke-width:1.5px,color:#22d3ee
    style AIService fill:#311042,stroke:#d946ef,stroke-width:2px,color:#f472b6
    style Gemini fill:#0f172a,stroke:#e879f9,stroke-width:1px,color:#f472b6
    style RAG fill:#0f172a,stroke:#a78bfa,stroke-width:1px,color:#c084fc
    style Plan fill:#1e1b4b,stroke:#8b5cf6,stroke-width:1.5px,color:#c084fc
    style Analytics fill:#111827,stroke:#10b981,stroke-width:2px,color:#34d399
```

<br />
<hr style="border: 1px solid #1f2937;" />
<br />

## 🛠️ The Technical Armory (Skills)

<table width="100%" border="0" style="border-collapse: collapse; border: none; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">
  <tr>
    <td width="50%" valign="top" style="border: none; padding-right: 10px;">
      <h4>💻 Languages &amp; Frameworks</h4>
      <ul>
        <li><strong>Languages:</strong> Python, TypeScript, JavaScript, SQL, Java (DSA), HTML5/CSS3</li>
        <li><strong>Web Frameworks:</strong> Next.js, React, Astro, FastAPI, Django REST Framework</li>
        <li><strong>Styling:</strong> Vanilla CSS, Tailwind CSS, PostCSS</li>
      </ul>
    </td>
    <td width="50%" valign="top" style="border: none; padding-left: 10px;">
      <h4>🧠 AI/ML &amp; Systems</h4>
      <ul>
        <li><strong>Machine Learning:</strong> Solved 70+ algorithmic coding trials on LeetCode; NLP, Classification Pipelines, Scikit-Learn, PyTorch, SHAP, Metaheuristics (GA, SMA, HHO)</li>
        <li><strong>Database &amp; Tools:</strong> PostgreSQL, SQLite, Drizzle ORM, Docker, Nginx, Git, Bash</li>
      </ul>
    </td>
  </tr>
</table>

<br />
<hr style="border: 1px solid #1f2937;" />
<br />

## 📊 Programmer Statistics (GitHub Metrics)

<div align="center">
  <table border="0" cellpadding="0" cellspacing="0">
    <tr>
      <td align="center" valign="middle">
        <img src="https://github-readme-stats.vercel.app/api?username=anshulsharma200817-svg&show_icons=true&theme=tokyonight&hide_border=true&bg_color=0D1117" alt="Anshul's GitHub Stats" height="150" />
      </td>
      <td width="20"></td>
      <td align="center" valign="middle">
        <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=anshulsharma200817-svg&layout=compact&theme=tokyonight&hide_border=true&bg_color=0D1117" alt="Anshul's Top Languages" height="150" />
      </td>
    </tr>
  </table>
</div>

<br />

<div align="center" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">
  <p>📬 Let's connect! Reach out via <a href="https://github.com/anshulsharma200817-svg">GitHub Issues</a> or explore my projects linked in the repositories.</p>
  <sub>"Once you step into the gate, the only way is forward." — The System</sub>
</div>
