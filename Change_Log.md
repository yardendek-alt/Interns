# Change Log

All notable changes to the **Interns** project are documented in this file.

---

## [Unreleased] - 2025-12-29

### 🚀 Feature Branch: `copilot/add-git-merge-script`

#### Added
- **Post-merge summarization script** (`post_merge_summary.py`)
  - Automatically generates AI-powered summaries after git merges
  - Uses OpenAI GPT-3.5-turbo to analyze git diffs
  - Appends 2-bullet-point summaries with timestamps to `Change_Log.md`

- **Setup automation** (`setup_hook.sh`)
  - One-command installation of the git post-merge hook
  - Configures the hook to run automatically after each merge

- **Test suite** (`test_post_merge.py`)
  - Validates Python script syntax
  - Tests git operations functionality
  - Verifies file operations work correctly
  - Confirms post-merge hook is installed and executable

- **Configuration files**
  - `.env.example` - Template for OpenAI API key setup
  - `.gitignore` - Standard Python ignores
  - `requirements.txt` - Python dependencies (openai, python-dotenv)

#### Changed
- Renamed output file from `project_evolution.md` to `Change_Log.md`
- Improved error handling and code readability based on code review feedback

---

## [1.0.0] - 2025-12-29

### Initial Release

#### Added
- Repository initialization
- Basic `README.md` with project title

---

## How This Project Works

This tool automates changelog generation by:
1. Hooking into git's post-merge event
2. Capturing the diff between `ORIG_HEAD` and `HEAD`
3. Sending the diff to an LLM for intelligent summarization
4. Auto-appending summaries to this changelog file

---

*This changelog follows [Keep a Changelog](https://keepachangelog.com/) format.*

