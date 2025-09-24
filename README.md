Dietitian AI Agent

A lightweight AI-powered diet plan generator built with LangGraph and LangChain, using Gemini 2.5 Flash as the language model.
The backend collects basic user information (age, gender, goals, preferences) and produces a personalized daily/weekly diet plan in PDF format.
The API endpoints will be exposed and connected to a frontend application in future updates.

🗂 Repository Structure
Dietetian-agent/
│
├── main.py          # Entry point to start the backend agent
├── graph.py         # LangGraph workflow and node definitions
├── methods.py       # Core functions for diet planning & PDF generation
├── requirements.txt # Python dependencies
└── README.md

✨ Features

Personalized meal plans based on user input

Gemini 2.5 Flash LLM for fast, high-quality responses

LangGraph for clean, modular conversation flow

Generates print-ready PDF diet plans

Designed to be connected to a frontend/API layer for web or mobile use

🚀 Quick Start (Backend Only)

Clone the repository

git clone https://github.com/hassan3208/Dietetian-agent.git
cd Dietetian-agent


Create & activate a virtual environment

python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate


Install dependencies

pip install -r requirements.txt


Set up environment variables
Create a .env file (or export variables) with:

GEMINI_API_KEY=your_gemini_key_here


Run the backend

python main.py

🧩 Usage

The backend script collects user details via console or future API calls.

It generates a complete diet plan and saves it as a PDF.

A separate frontend will call this backend API for a web/mobile interface.

📌 Next Steps

Build a frontend (e.g., React, Next.js, or Flutter) to capture user inputs.

Connect the frontend to the backend API endpoints for real-time diet plan generation.

🤝 Contributing

Pull requests and feature suggestions are welcome:

Fork the repo

Create a new branch (git checkout -b feature-name)

Commit your changes (git commit -m "Add feature")

Push and open a Pull Request

🛡 License

This project is licensed under the MIT License.
