from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained model and tokenizer
model_name = "gpt2-large"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def get_local_gpt2_response(prompt, max_length=150, num_return_sequences=1):
    try:
        # Encode the prompt
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        
        # Generate response
        outputs = model.generate(
            inputs, 
            max_length=max_length, 
            num_return_sequences=num_return_sequences,
            no_repeat_ngram_size=2,  # Prevent repeating n-grams
            early_stopping=True      # Stop early if end-of-sequence token is generated
        )
        
        # Decode the response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

    