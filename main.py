import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime
import json

def save_to_file(content, content_type):
    # Create 'outputs' directory if it doesn't exist
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/{content_type}_{timestamp}.txt"
    
    # Save content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

def generate_content(model, prompt):
    response = model.generate_content(prompt)
    return response.text

def get_prompt_for_type(content_type):
    prompts = {
        '1': "Write a blog post about ",
        '2': "Write a social media post about ",
        '3': "Write a joke about ",
        '4': "Write a tutorial about "
    }
    topic = input("Enter the topic: ")
    return prompts[content_type] + topic

def main():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file")
        return
    
    # Configure Gemini
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        while True:
            print("\n=== Content Generator Menu ===")
            print("1. Generate Blog Post")
            print("2. Generate Social Media Post")
            print("3. Generate Joke")
            print("4. Generate Tutorial")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '5':
                print("Thank you for using the Content Generator!")
                break
            
            if choice not in ['1', '2', '3', '4']:
                print("Invalid choice. Please try again.")
                continue
            
            content_types = {
                '1': 'blog',
                '2': 'social',
                '3': 'joke',
                '4': 'tutorial'
            }
            
            # Get prompt based on content type
            prompt = get_prompt_for_type(choice)
            
            print("\nGenerating content...")
            content = generate_content(model, prompt)
            
            # Display the generated content
            print("\nGenerated Content:")
            print("=" * 50)
            print(content)
            print("=" * 50)
            
            # Ask if user wants to save the content
            if input("\nWould you like to save this content? (y/n): ").lower() == 'y':
                filename = save_to_file(content, content_types[choice])
                print(f"Content saved to: {filename}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("\nPossible solutions:")
        print("1. Check if your API key is correct")
        print("2. Make sure you're using a valid Gemini API key from: https://makersuite.google.com/app/apikey")
        print("3. Check your internet connection")

if __name__ == "__main__":
    main()