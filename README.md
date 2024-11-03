# GPT-Researcher Flask API

A Flask API wrapper for GPT-Researcher that allows you to conduct research through HTTP requests.

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key and other optional configurations

## Running the API

```bash
python app.py
```

The API will run on `http://localhost:5000`

## API Endpoints

### POST /research
Conducts research based on the provided query.

Request body:
```json
{
    "query": "Your research query here",
    "report_type": "research_report"  // optional
}
```

Example curl command:
```bash
curl -X POST http://localhost:5000/research \
-H "Content-Type: application/json" \
-d '{"query": "Research DaRose Vienna (darosevienna.at) and provide a comprehensive SWOT analysis."}'
```

### GET /health
Health check endpoint to verify the API is running.

## Environment Variables

- `OPENAI_API_KEY` (Required): Your OpenAI API key
- `REPORT_TYPE` (Optional): Default report type for research
- `SERP_API_KEY` (Optional): For Google search functionality
- `BROWSERLESS_API_KEY` (Optional): For web browsing functionality

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 400: Bad Request (missing or invalid parameters)
- 500: Internal Server Error (processing errors)

## Response Format

Successful response:
```json
{
    "research_result": "Research findings...",
    "report": "Generated report..."
}
```

Error response:
```json
{
    "error": "Error message"
}
