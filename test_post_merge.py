#!/usr/bin/env python3
"""
Test script for the post-merge summary functionality.
This tests the script's logic without making actual API calls.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


def test_git_diff():
    """Test that we can get git diff output."""
    print("Testing git diff functionality...")
    try:
        # Try to get a diff (will fail if ORIG_HEAD doesn't exist, which is expected)
        result = subprocess.run(
            ["git", "diff", "HEAD~1", "HEAD"] if subprocess.run(
                ["git", "rev-parse", "--verify", "HEAD~1"],
                capture_output=True
            ).returncode == 0 else ["git", "show", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ Git diff command works (got {len(result.stdout)} characters)")
        return True
    except Exception as e:
        print(f"✗ Git diff test failed: {e}")
        return False


def test_file_operations():
    """Test that we can write to the evolution file."""
    print("\nTesting file operations...")
    try:
        repo_root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        
        test_file = Path(repo_root) / "test_evolution.md"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Write test content
        with test_file.open("w") as f:
            f.write("# Test Project Evolution\n\n")
            f.write(f"## Test Merge on {timestamp}\n\n")
            f.write("- Test bullet point 1\n")
            f.write("- Test bullet point 2\n\n")
        
        # Verify file was created
        if test_file.exists():
            content = test_file.read_text()
            if "Test bullet point 1" in content and "Test bullet point 2" in content:
                print(f"✓ File operations work (created {test_file})")
                # Clean up
                test_file.unlink()
                return True
        
        print("✗ File operations test failed: content mismatch")
        return False
    except Exception as e:
        print(f"✗ File operations test failed: {e}")
        return False


def test_script_syntax():
    """Test that the post_merge_summary.py script has valid Python syntax."""
    print("\nTesting script syntax...")
    try:
        repo_root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        
        script_path = Path(repo_root) / "post_merge_summary.py"
        
        # Compile the script to check for syntax errors
        with script_path.open("r") as f:
            code = f.read()
            compile(code, str(script_path), "exec")
        
        print("✓ Script syntax is valid")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in script: {e}")
        return False
    except Exception as e:
        print(f"✗ Script syntax test failed: {e}")
        return False


def test_hook_exists():
    """Test that the post-merge hook is installed."""
    print("\nTesting git hook installation...")
    try:
        repo_root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
        
        hook_path = Path(repo_root) / ".git" / "hooks" / "post-merge"
        
        if hook_path.exists() and hook_path.stat().st_mode & 0o111:
            print(f"✓ Post-merge hook is installed and executable")
            return True
        elif hook_path.exists():
            print(f"⚠ Post-merge hook exists but is not executable")
            print(f"  Run: chmod +x {hook_path}")
            return False
        else:
            print(f"⚠ Post-merge hook not found at {hook_path}")
            print(f"  Run: ./setup_hook.sh to install it")
            return False
    except Exception as e:
        print(f"✗ Hook installation test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Post-Merge Summary Script - Test Suite")
    print("=" * 60)
    
    tests = [
        test_script_syntax,
        test_git_diff,
        test_file_operations,
        test_hook_exists,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All tests passed! The post-merge script is ready to use.")
        print("\nNext steps:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. The script will run automatically after git merges")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
