import runpod
from vllm import LLM, SamplingParams

# Initialize vLLM model globally to avoid reloading on each request
print("Loading GPT-OSS-20B model...")
llm = LLM(
    model="openai/gpt-oss-20b",  # Using a smaller model for testing - replace with actual GPT-OSS-20B path
    tensor_parallel_size=1,
    gpu_memory_utilization=0.8
)
print("Model loaded successfully!")

def handler(event):
    try:
        print("Worker Start")
        input_data = event['input']
        
        prompt = input_data.get('prompt')
        if not prompt:
            return {"error": "No prompt provided"}
        
        # Get generation parameters
        max_tokens = input_data.get('max_tokens', 512)
        temperature = input_data.get('temperature', 0.8)
        top_p = input_data.get('top_p', 0.9)
        
        print(f"Received prompt: {prompt}")
        print(f"Max tokens: {max_tokens}, Temperature: {temperature}, Top-p: {top_p}")
        
        # Set up sampling parameters
        sampling_params = SamplingParams(
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
        
        # Generate response
        print("Generating response...")
        outputs = llm.generate([prompt], sampling_params)
        
        # Extract generated text
        generated_text = outputs[0].outputs[0].text
        
        result = {
            "generated_text": generated_text,
            "prompt": prompt,
            "parameters": {
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p
            }
        }
        
        print("Generation completed successfully")
        return result
        
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        return {"error": str(e)}

# Start the Serverless function when the script is run
if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})