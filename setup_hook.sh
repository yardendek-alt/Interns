#!/bin/bash
#
# Setup script to install the git post-merge hook
#
# This script copies the post-merge hook to .git/hooks/

set -e

echo "Setting up post-merge hook..."

# Get the repository root
REPO_ROOT=$(git rev-parse --show-toplevel)

# Check if we're in a git repository
if [ ! -d "$REPO_ROOT/.git" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Create the hooks directory if it doesn't exist
mkdir -p "$REPO_ROOT/.git/hooks"

# Create the post-merge hook
cat > "$REPO_ROOT/.git/hooks/post-merge" << 'EOF'
#!/bin/bash
#
# Git post-merge hook
# This hook is called after a successful git merge
# It runs the Python script to summarize the changes

# Get the repository root directory
REPO_ROOT=$(git rev-parse --show-toplevel)

# Path to the Python script
SCRIPT_PATH="$REPO_ROOT/post_merge_summary.py"

# Check if the script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Warning: post_merge_summary.py not found at $SCRIPT_PATH"
    exit 0
fi

# Run the Python script
python3 "$SCRIPT_PATH"

# Exit with 0 even if the script fails to not block the merge
exit 0
EOF

# Make it executable
chmod +x "$REPO_ROOT/.git/hooks/post-merge"

echo "✓ Post-merge hook installed successfully!"
echo ""
echo "Next steps:"
echo "1. Install dependencies: pip install -r requirements.txt"
echo "2. Set your OPENAI_API_KEY: export OPENAI_API_KEY='your_key_here'"
echo "3. The hook will run automatically after git merges"
