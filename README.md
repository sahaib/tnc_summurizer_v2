# Privacy Policy Summarizer

## Description

The Privacy Policy Summarizer is a Python application that uses AI to summarize privacy policies from websites or text input. It provides an easy-to-use graphical interface for users to input privacy policy text or URLs, choose between different AI models (GPT and Claude), and receive concise summaries.

## Features

- Summarize privacy policies from URLs or plain text input
- Choose between OpenAI's GPT and Anthropic's Claude AI models
- User-friendly GUI built with tkinter
- View summarization history
- Error handling for various input scenarios

## Requirements

- Python 3.7+
- tkinter
- requests
- beautifulsoup4
- openai
- anthropic

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/privacy-policy-summarizer.git
   cd privacy-policy-summarizer
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your API keys as environment variables:
   ```
   export OPENAI_API_KEY='your-openai-api-key'
   export ANTHROPIC_API_KEY='your-anthropic-api-key'
   ```

## Usage
Run the script:python tnc_summurizer.py

1. Enter a URL or paste the privacy policy text into the input box.
2. Select the AI model you want to use (GPT or Claude).
3. Click the "Summarize" button.
4. View the summary in the result text area.
5. Click "Show History" to view previous summaries.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for the GPT model
- Anthropic for the Claude model
- The open-source community for the various libraries used in this project
- Cursor IDE

