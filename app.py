from flask import Flask, request, jsonify
from gpt_researcher import GPTResearcher
import asyncio
from dotenv import load_dotenv
import os
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == os.getenv('API_KEY'):
            return f(*args, **kwargs)
        return jsonify({'error': 'Invalid or missing API key'}), 401
    return decorated

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

@app.route('/research', methods=['POST'])
@require_api_key
def conduct_research():
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        query = data['query']
        report_type = data.get('report_type', os.getenv('REPORT_TYPE', 'research_report'))
        
        # Initialize researcher
        researcher = GPTResearcher(query=query, report_type=report_type)
        
        # Conduct research
        research_result = run_async(researcher.conduct_research())
        
        # Generate report
        report = run_async(researcher.write_report())
        
        return jsonify({
            'research_result': '',#research_result,
            'report': report
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
@require_api_key
def health_check():
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

if __name__ == '__main__':
    if not os.getenv('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY not found in environment variables")
    if not os.getenv('API_KEY'):
        print("Warning: API_KEY not found in environment variables")
    app.run(debug=True, port=5000)
