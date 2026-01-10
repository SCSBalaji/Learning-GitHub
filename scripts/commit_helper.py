import os
import sys
import subprocess

def git_commit(problem_number, commit_type="Add", description=""):
    """
    Create a properly formatted git commit.
    
    Usage:
        python scripts/commit_helper.py 1458 Add "DP solution"
    """
    
    problem_num = str(problem_number).zfill(4)
    
    # Find problem title
    title = None
    difficulty_folders = ['1. easy', '2. medium', '3. hard']
    
    for difficulty in difficulty_folders:
        if not os.path.exists(difficulty):
            continue
        
        for range_folder in os.listdir(difficulty):
            range_path = os.path.join(difficulty, range_folder)
            
            if not os.path.isdir(range_path):
                continue
            
            for folder in os.listdir(range_path):
                if folder.startswith(problem_num):
                    title = ' '.join(folder.split('-')[1:]).title()
                    break
            
            if title:
                break
        
        if title:
            break
    
    if not title:
        print(f"❌ Problem #{problem_number} not found!")
        return
    
    # Create commit message
    if description:
        commit_msg = f"[{commit_type}] #{problem_num}: {title} - {description}"
    else:
        commit_msg = f"[{commit_type}] #{problem_num}: {title}"
    
    print(f"📝 Commit message: {commit_msg}")
    
    confirm = input("\nProceed? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        return
    
    # Git operations
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
    
    push = input("\n🚀 Push to GitHub? (y/n): ")
    if push.lower() == 'y':
        subprocess.run(['git', 'push'], check=True)
        print("✅ Pushed successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python commit_helper.py <problem_number> <type> [description]")
        print("Types: Add, Update, Optimize, Fix, Docs")
        print('Example: python commit_helper.py 1458 Add "DP solution"')
        sys.exit(1)
    
    problem_number = sys.argv[1]
    commit_type = sys.argv[2]
    description = sys.argv[3] if len(sys.argv) > 3 else ""
    
    git_commit(problem_number, commit_type, description)