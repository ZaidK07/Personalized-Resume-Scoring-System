# Personalized Resume Scoring System

## Overview
This project is a backend system designed to evaluate and score resumes against specific job descriptions using Generative AI. It differentiates itself from standard scoring systems by implementing a "Human-in-the-Loop" feedback mechanism. The system leverages a vector database to store user feedback and preferences, allowing the AI agent to learn and adapt its scoring criteria to specific user needs over time.

## Features
- **Automated Resume Scoring:** Parses resumes (PDF, DOCX, TXT) and evaluates them against a provided job description.
- **Personalized Adaptation:** Utilizes a vector database (Pinecone) to retrieve historical user feedback, enabling the AI to adjust scoring based on past preferences.
- **Feedback Loop:** Dedicated API endpoints for capturing user disagreement and reasoning to refine future model performance.
- **Multi-Format Support:** Handles common document formats including PDF and DOCX.

## Technical Architecture
- **Language:** Python
- **Web Framework:** Flask / Flask-RESTful
- **AI Engine:** Mistral AI (via LangChain)
- **Vector Database:** Pinecone
- **Document Processing:** pypdf, python-docx

## Prerequisites
- Python 3.8 or higher
- Mistral AI API Key
- Pinecone API Key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Personalized-Resume-Scoring-System
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the root directory.
2. Add the following environment variables:

   ```env
   API_KEY=<your_mistral_api_key>
   MODEL_ID=<mistral_model_id>
   PINECONE_API_KEY=<your_pinecone_api_key>
   ```

## Usage

To start the server, you can use the provided shell script or run the application directly.

**Using the script:**
```bash
sh run.sh
```

**Manual execution:**
```bash
source .venv/bin/activate
python app.py
```

The server runs by default on `http://0.0.0.0:9833`.

## API Reference

### 1. Health Check
**Endpoint:** `/home`
**Method:** `GET`
**Description:** Verifies that the API is running.

### 2. Get Resume Score
**Endpoint:** `/get-resume-score`
**Method:** `POST`
**Content-Type:** `multipart/form-data`
**Parameters:**
- `job_description`: File (Job Description document)
- `resume_files`: List of Files (Resume documents)
- `user_id`: String (Unique identifier for the user)

**Response:**
Returns a JSON object containing the AI score, pros, cons, and the extracted text content for potential feedback.

### 3. Submit Feedback
**Endpoint:** `/submit-feedback`
**Method:** `POST`
**Content-Type:** `application/json`
**Body:**
```json
{
  "user_id": "string",
  "job_description": "string (extracted text)",
  "resume_content": "string (extracted text)",
  "reason": "string (feedback on why the score was incorrect)"
}
```
**Description:** Stores user feedback in the vector database to influence future scoring logic for the specific user.

## Project Structure
- `app.py`: Entry point of the application.
- `views.py`: API resource definitions and logic.
- `routes.py`: Route registration.
- `config/`: Configuration for Pinecone and utility functions.
- `gen_ai/`: AI agent configuration, prompts, and LLM interaction logic.
