# StudyGenie – AI-Powered Smart Study Assistant

StudyGenie is an **Agentic AI-based smart study assistant** designed to help students learn effectively from their study materials.

The system uses **RAG (Retrieval-Augmented Generation)** to retrieve relevant information from uploaded study materials and uses **Google Gemini** to generate useful and personalized learning resources.

## 🚀 Features

* 📄 Upload study materials in PDF format
* 💬 Ask questions from the uploaded study material
* 📝 Generate structured summaries
* ❓ Generate MCQs and quizzes
* 🗂️ Generate flashcards
* 📅 Generate personalized  study plans

## 🛠️ Technologies Used

* **Python**
* **Streamlit** – Frontend interface
* **Langflow** – AI workflow and agent development
* **Google Gemini** – Large Language Model
* **RAG** – Retrieval-Augmented Generation
* **ChromaDB** – Vector database
* **Gemini Embedding 2** – Document embeddings

## 🏗️ System Architecture


Student
   ↓
Streamlit
   ↓
Langflow API
   ↓
StudyGenie Agent
   ├── RAG
   ├── Quiz Generation
   ├── Flashcard Generation
   └── Study Plan Generation
   ↓
Google Gemini
   ↓
Response to Student

## 🎯 Objective

The objective of StudyGenie is to provide students with an **intelligent and personalized study assistant** that can transform study materials into useful learning resources and support effective exam preparation.

## 📌 Project Status

The current version supports **PDF-based study material upload, question answering, summaries, MCQs, flashcards, and 7-day study plans**.
