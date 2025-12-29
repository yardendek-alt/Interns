# Interns

This repository includes an automated post-merge hook that generates a summary of changes using an LLM.

## Setup

### Prerequisites
- Python 3.7 or higher
- OpenAI API key

### Installation

1. Run the setup script to install the git hook:
```bash
./setup_hook.sh
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Or export it in your shell:
export OPENAI_API_KEY="your_api_key_here"
```

The git hook will now run automatically after each merge.

## Testing

You can verify the installation is correct by running the test script:

```bash
python3 test_post_merge.py
```

This will test that:
- The Python script has valid syntax
- Git operations work correctly
- File operations work correctly
- The post-merge hook is installed and executable

## How It Works

After each successful git merge, the post-merge hook will:
1. Get the git diff between ORIG_HEAD and HEAD
2. Send the diff to an LLM (GPT-3.5-turbo) for summarization
3. Generate a 2-bullet-point summary of the changes
4. Append the summary with a timestamp to `Change_Log.md`

## Manual Testing

You can manually test the script without performing a merge:

```bash
# Ensure OPENAI_API_KEY is set
export OPENAI_API_KEY="your_api_key_here"

# Run the script directly
python3 post_merge_summary.py
```

Note: The script requires ORIG_HEAD to exist, which is typically created during a merge operation.