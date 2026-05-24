import ollama

def test_local_model():
    print("Sending request to local Mistral engine...")
    try:
        # We are telling the local model to reply with a very specific constraint
        response = ollama.chat(model='mistral', messages=[
            {
                'role': 'user',
                'content': 'Respond with exactly one sentence: Hello, the connection is successful!',
            },
        ])
        
        print("\n[SUCCESS] Local LLM Response:")
        print(response['message']['content'])
        
    except Exception as e:
        print(f"\n[ERROR] Connection failed. Is Ollama running? Error details: {e}")

if __name__ == "__main__":
    test_local_model()