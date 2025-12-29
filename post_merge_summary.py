#!/usr/bin/env python3
"""
Post-merge script that generates a summary of changes using an LLM.

This script:
1. Gets the git diff between ORIG_HEAD and HEAD
2. Sends the diff to an LLM API for summarization
3. Appends the summary with timestamp to project_evolution.md
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Try to import openai, but provide helpful error if not installed
try:
    from openai import OpenAI
except ImportError:
    print("Error: OpenAI library not installed. Run: pip install openai", file=sys.stderr)
    sys.exit(1)


def get_git_diff():
    """Get the git diff between ORIG_HEAD and HEAD."""
    try:
        # Check if ORIG_HEAD exists (it's created during merge)
        result = subprocess.run(
            ["git", "diff", "ORIG_HEAD", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return None


def summarize_with_llm(diff_text):
    """Send diff to LLM and get a 2-bullet-point summary."""
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    try:
        client = OpenAI(api_key=api_key)
        
        prompt = f"""Analyze the following git diff and provide a summary of what changed in exactly 2 bullet points. 
Each bullet point should be concise and describe a key change or set of related changes.

Git diff:
{diff_text}

Provide only the 2 bullet points, nothing else. Format each bullet point starting with '- '."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes code changes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"Error calling LLM API: {e}", file=sys.stderr)
        sys.exit(1)


def append_to_evolution_file(summary):
    """Append the summary with timestamp to project_evolution.md."""
    repo_root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True
    ).stdout.strip()
    
    evolution_file = Path(repo_root) / "project_evolution.md"
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create file with header if it doesn't exist
    if not evolution_file.exists():
        with evolution_file.open("w") as f:
            f.write("# Project Evolution\n\n")
            f.write("This file tracks changes made to the project after merges.\n\n")
    
    # Append the new entry
    with evolution_file.open("a") as f:
        f.write(f"## Merge on {timestamp}\n\n")
        f.write(f"{summary}\n\n")
    
    print(f"Summary appended to {evolution_file}")


def main():
    """Main function to orchestrate the post-merge summary."""
    print("Running post-merge summary...")
    
    # Get the diff
    diff = get_git_diff()
    if not diff:
        print("No diff found or error occurred. Skipping summary.")
        return
    
    # If diff is empty, skip
    if not diff.strip():
        print("No changes detected in diff. Skipping summary.")
        return
    
    # Summarize with LLM
    print("Generating summary with LLM...")
    summary = summarize_with_llm(diff)
    
    # Append to file
    append_to_evolution_file(summary)
    print("Post-merge summary completed successfully!")


if __name__ == "__main__":
    main()
