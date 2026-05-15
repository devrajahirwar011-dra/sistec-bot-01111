"""
API Client Examples for SISTec RAG Chatbot
Shows how to interact with the chatbot API
"""
import requests
import json
from typing import List, Dict


class SISTecChatbotClient:
    """Python client for SISTec Chatbot API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict:
        """Check if chatbot is running"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def initialize(self, documents_path: str = "./documents") -> Dict:
        """Initialize vector database with documents"""
        payload = {"documents_path": documents_path}
        try:
            response = self.session.post(
                f"{self.base_url}/initialize",
                json=payload
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def query(self, question: str, top_k: int = 5) -> Dict:
        """Send a single query to the chatbot"""
        payload = {
            "query": question,
            "top_k": top_k
        }
        try:
            response = self.session.post(
                f"{self.base_url}/query",
                json=payload
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def batch_query(self, questions: List[str]) -> Dict:
        """Send multiple queries at once"""
        payload = {
            "requests": [{"query": q} for q in questions]
        }
        try:
            response = self.session.post(
                f"{self.base_url}/batch-query",
                json=payload
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_query_types(self) -> Dict:
        """Get supported query types"""
        try:
            response = self.session.get(f"{self.base_url}/query-types")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_system_rules(self) -> Dict:
        """Get system behavior rules"""
        try:
            response = self.session.get(f"{self.base_url}/rules")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_system_prompt(self) -> Dict:
        """Get current system prompt"""
        try:
            response = self.session.get(f"{self.base_url}/system-prompt")
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def example_basic_query():
    """Example: Basic query"""
    print("\n" + "="*60)
    print("Example 1: Basic Query")
    print("="*60)
    
    client = SISTecChatbotClient()
    
    # Check health
    print("\n1. Checking server health...")
    health = client.health_check()
    print(json.dumps(health, indent=2))
    
    # Initialize (if not already done)
    print("\n2. Initializing chatbot...")
    init_result = client.initialize()
    print(json.dumps(init_result, indent=2))
    
    # Send query
    print("\n3. Sending query...")
    result = client.query("What is the B.Tech fee structure?")
    print(json.dumps(result, indent=2))


def example_batch_queries():
    """Example: Batch queries"""
    print("\n" + "="*60)
    print("Example 2: Batch Queries")
    print("="*60)
    
    client = SISTecChatbotClient()
    
    queries = [
        "What are the eligibility criteria?",
        "Tell me about CSE department",
        "What is the placement rate?"
    ]
    
    print(f"\nSending {len(queries)} queries...")
    result = client.batch_query(queries)
    print(json.dumps(result, indent=2))


def example_get_info():
    """Example: Get system information"""
    print("\n" + "="*60)
    print("Example 3: System Information")
    print("="*60)
    
    client = SISTecChatbotClient()
    
    print("\n1. Query Types:")
    types_result = client.get_query_types()
    print(json.dumps(types_result, indent=2))
    
    print("\n2. System Rules:")
    rules_result = client.get_system_rules()
    print(json.dumps(rules_result, indent=2))


def example_curl_commands():
    """Print curl command examples"""
    print("\n" + "="*60)
    print("CURL Command Examples")
    print("="*60)
    
    examples = [
        {
            "name": "Health Check",
            "command": 'curl -X GET "http://localhost:8000/health"'
        },
        {
            "name": "Initialize",
            "command": '''curl -X POST "http://localhost:8000/initialize" \\
  -H "Content-Type: application/json" \\
  -d '{"documents_path": "./documents"}'
'''
        },
        {
            "name": "Single Query",
            "command": '''curl -X POST "http://localhost:8000/query" \\
  -H "Content-Type: application/json" \\
  -d '{"query": "What is the B.Tech fee structure?", "top_k": 5}'
'''
        },
        {
            "name": "Batch Query",
            "command": '''curl -X POST "http://localhost:8000/batch-query" \\
  -H "Content-Type: application/json" \\
  -d '{
    "requests": [
      {"query": "What are the departments?"},
      {"query": "What is the placement rate?"}
    ]
  }'
'''
        },
        {
            "name": "Get Query Types",
            "command": 'curl -X GET "http://localhost:8000/query-types"'
        }
    ]
    
    for example in examples:
        print(f"\n{example['name']}:")
        print(example['command'])


def example_javascript_client():
    """Print JavaScript client example"""
    print("\n" + "="*60)
    print("JavaScript/Node.js Client Example")
    print("="*60)
    
    code = '''
// Using Fetch API
const baseUrl = "http://localhost:8000";

// Single query
async function query(question) {
    const response = await fetch(`${baseUrl}/query`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({query: question, top_k: 5})
    });
    return await response.json();
}

// Batch queries
async function batchQuery(questions) {
    const response = await fetch(`${baseUrl}/batch-query`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            requests: questions.map(q => ({query: q}))
        })
    });
    return await response.json();
}

// Example usage
(async () => {
    const result = await query("What is the eligibility?");
    console.log(result);
})();
'''
    print(code)


def example_python_integration():
    """Print Python integration example"""
    print("\n" + "="*60)
    print("Python Integration Example")
    print("="*60)
    
    code = '''
from api_client_examples import SISTecChatbotClient

# Create client
client = SISTecChatbotClient("http://localhost:8000")

# Initialize
client.initialize("./documents")

# Query
result = client.query("What is the placement rate?")
print(result['answer'])
print(f"Sources: {result['sources']}")

# Batch query
results = client.batch_query([
    "What are the fees?",
    "Tell me about CSE",
    "What is the hostel cost?"
])

for r in results['results']:
    print(f"Q: {r['query']}")
    print(f"A: {r['answer']}")
    print()
'''
    print(code)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        example = sys.argv[1]
        
        if example == "basic":
            example_basic_query()
        elif example == "batch":
            example_batch_queries()
        elif example == "info":
            example_get_info()
        elif example == "curl":
            example_curl_commands()
        elif example == "js":
            example_javascript_client()
        elif example == "python":
            example_python_integration()
        else:
            print(f"Unknown example: {example}")
    else:
        print("\n" + "="*60)
        print("SISTec Chatbot API - Client Examples")
        print("="*60)
        print("\nUsage: python api_client_examples.py [example]")
        print("\nAvailable examples:")
        print("  basic    - Basic query example")
        print("  batch    - Batch queries example")
        print("  info     - Get system information")
        print("  curl     - CURL command examples")
        print("  js       - JavaScript client example")
        print("  python   - Python integration example")
        print("\nExample: python api_client_examples.py basic")
        print("="*60 + "\n")
