```markdown
# Dietitian AI Agent

A lightweight **AI-powered diet plan generator** built with **LangGraph** and **LangChain**, using **Gemini 2.5 Flash** as the language model.  
The backend collects basic user information (age, gender, goals, preferences) and produces a **personalized daily or weekly diet plan** in PDF format.  
API endpoints will be connected to a frontend in future updates.

---

## 🗂 Repository Structure
```

Dietetian-agent/
│
├── main.py          # Entry point to start the backend agent
├── graph.py         # LangGraph workflow and node definitions
├── methods.py       # Core functions for diet planning & PDF generation
├── requirements.txt # Python dependencies
└── README.md

````

---

## ✨ Features
- **Personalized meal plans** based on user input  
- **Gemini 2.5 Flash** LLM for fast, high-quality responses  
- **LangGraph** for clean, modular conversation flow  
- Generates **print-ready PDF diet plans**  
- Ready for integration with a **frontend/API layer** for web or mobile use

---

## 🚀 Quick Start (Backend Only)

1. **Clone the repository**
   ```bash
   git clone https://github.com/hassan3208/Dietetian-agent.git
   cd Dietetian-agent
````

2. **Create & activate a virtual environment**

   ```bash
   python -m venv venv
   # Linux/macOS
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   Create a `.env` file and add:

   ```
   GEMINI_API_KEY=your_gemini_key_here
   ```

5. **Run the backend**

   ```bash
   python main.py
   ```

---

## 🧩 Usage

* The backend script collects user details via console or future API calls.
* It generates a complete diet plan and saves it as a PDF.
* A separate frontend will call this backend API for a web or mobile interface.

---

## 📌 Next Steps

* Build a **frontend** (e.g., React, Next.js, or Flutter) to capture user inputs.
* Connect the frontend to the backend API endpoints for real-time diet plan generation.

---

## 🤝 Contributing

Pull requests and feature suggestions are welcome:

1. Fork the repo
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push and open a Pull Request

---

## 🛡 License

This project is licensed under the **MIT License**.

```

Copy everything between the triple backticks into your `README.md` file—it’s already in proper Markdown format and will render cleanly on GitHub.
```
