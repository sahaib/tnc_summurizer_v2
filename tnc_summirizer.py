import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tkhtmlview import HTMLLabel
import markdown
import json
from datetime import datetime
import itertools
import time
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import openai
import os
import threading
import re

# Set up API keys and clients
openai_client = OpenAI(api_key=os.getenv(''))
anthropic_client = Anthropic(api_key=os.getenv(''))

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv(''))

class PrivacyPolicySummarizer:
    def __init__(self, master):
        self.master = master
        master.title("Privacy Policy Summarizer")
        
        # Initialize API clients
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        self.input_label = ttk.Label(master, text="Enter Privacy Policy URL or Text:")
        self.input_label.pack()
        
        self.input_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=10)
        self.input_text.pack()
        
        self.model_label = ttk.Label(master, text="Select AI Model:")
        self.model_label.pack()
        
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(master, textvariable=self.model_var, values=["GPT", "Claude"])
        self.model_dropdown.pack()
        self.model_dropdown.set("GPT")  # Default value
        
        self.summarize_button = ttk.Button(master, text="Summarize", command=self.summarize)
        self.summarize_button.pack()
        
        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=20)
        self.result_text.pack()
        
        # Add a button to show history
        self.history_button = ttk.Button(master, text="Show History", command=self.show_history)
        self.history_button.pack()
        
        self.history = []

    def fetch_privacy_policy(self, input_text):
        if re.match(r'https?://', input_text):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(input_text, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup.body.get_text(strip=True)
            except requests.RequestException as e:
                raise Exception(f"Error fetching the webpage: {str(e)}")
        else:
            return input_text

    def get_summary_prompt(self, policy_text):
        return f"""Summarize the following privacy policy:

{policy_text}

Focus on these main areas:
1. What personal data is collected
2. How the data is used
3. Data sharing practices
4. User rights and controls
5. Important policy changes or unique clauses

Present the summary as a bulleted list with clear, concise points. Use Markdown formatting for better readability. Start each point with a relevant emoji. For example:
- 📧 for email-related information
- 📍 for location data
- 🖼️ for photos or images
- 👤 for personal profile information
- 🔒 for security-related points
- 🤝 for data sharing practices
- ⚖️ for legal or policy changes
"""

    def summarize_with_gpt(self, policy_text):
        prompt = self.get_summary_prompt(policy_text)
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes privacy policies."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def summarize_with_claude(self, policy_text):
        prompt = self.get_summary_prompt(policy_text)
        response = self.anthropic_client.completions.create(
            model="claude-2.1",
            max_tokens_to_sample=1000,
            prompt=f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}",
        )
        return response.completion

    def summarize(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        model = self.model_var.get()
        
        if not input_text:
            self.show_error("Please enter a URL or privacy policy text.")
            return

        try:
            policy_text = self.fetch_privacy_policy(input_text)
            
            if not policy_text:
                raise ValueError("No content could be extracted from the provided input.")
            
            if model == "GPT":
                summary = self.summarize_with_gpt(policy_text)
            elif model == "Claude":
                summary = self.summarize_with_claude(policy_text)
            else:
                raise ValueError("Invalid model selection")
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, summary)
            
            # Add to history
            self.history.append({"input": input_text, "model": model, "summary": summary})
            
        except Exception as e:
            self.show_error(str(e))

    def show_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("Summary History")
        
        # Create a frame to hold the canvas and scrollbar
        frame = ttk.Frame(history_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if not self.history:
            ttk.Label(scrollable_frame, text="No history available.").pack(padx=10, pady=10)
        else:
            for i, entry in enumerate(self.history, 1):
                entry_frame = ttk.Frame(scrollable_frame)
                entry_frame.pack(padx=10, pady=10, fill="x", expand=True)

                ttk.Label(entry_frame, text=f"Entry {i}:", font=("", 12, "bold")).pack(anchor="w")
                ttk.Label(entry_frame, text=f"Input: {entry['input'][:100]}...").pack(anchor="w")
                ttk.Label(entry_frame, text=f"Model: {entry['model']}").pack(anchor="w")

                summary_text = scrolledtext.ScrolledText(entry_frame, wrap=tk.WORD, width=80, height=10)
                summary_text.pack(padx=5, pady=5, fill="both", expand=True)
                summary_text.insert(tk.END, entry['summary'])
                summary_text.config(state=tk.DISABLED)  # Make the text read-only

                ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", padx=10, pady=10)

        # Set a reasonable size for the window
        history_window.geometry("800x600")

    def show_error(self, message):
        error_message = f"Error: {message}\n\nPlease check your input and try again."
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, error_message)

def main():
    root = tk.Tk()
    app = PrivacyPolicySummarizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()