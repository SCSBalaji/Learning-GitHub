import os
import sys

def add_solution(problem_number, approach_name, status="Accepted"):
    """
    Add a new solution file (including TLE/Brute Force approaches).
    
    Usage:
        python scripts/add_solution.py 1458 "brute-force" TLE
        python scripts/add_solution.py 1458 "optimized-dp" Accepted
    """
    
    problem_num = str(problem_number).zfill(4)
    problem_path = None
    
    for difficulty in ['1. easy', '2. medium', '3. hard']:
        if not os.path.exists(difficulty):
            continue
        for range_folder in os.listdir(difficulty):
            range_path = os.path.join(difficulty, range_folder)
            if not os.path.isdir(range_path):
                continue
            for folder in os.listdir(range_path):
                if folder.startswith(problem_num):
                    problem_path = os.path.join(range_path, folder)
                    break
    
    if not problem_path:
        print(f"❌ Problem #{problem_number} not found!")
        return
    
    # Count existing solutions
    solution_count = len([f for f in os.listdir(problem_path) if f.startswith('Solution') and f.endswith('.java')])
    next_num = solution_count + 1
    
    # Get title from folder
    title = ' '.join(os.path.basename(problem_path).split('-')[1:]).title()
    
    # Status emoji
    status_map = {
        'accepted': '✅ Accepted',
        'tle': '❌ TLE',
        'mle': '❌ MLE',
        'wa': '⚠️ Wrong Answer'
    }
    status_text = status_map.get(status.lower(), '✅ Accepted')
    
    content = f"""// LeetCode #{problem_num}: {title}
// Approach: {approach_name.replace('-', ' ').title()}
// Status: {status_text}
// Time: O()  |  Space: O()

class Solution {{
    // Paste your LeetCode solution here
}}
"""
    
    filename = f"Solution{next_num}.java"
    with open(os.path.join(problem_path, filename), 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created {filename}")
    print(f"   Status: {status_text}")
    print(f"   Path: {problem_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python add_solution.py <number> <approach> [status]")
        print("Status: Accepted (default), TLE, MLE, WA")
        print('Example: python add_solution.py 1458 "brute-force" TLE')
        sys.exit(1)
    
    add_solution(
        sys.argv[1], sys.argv[2],
        sys.argv[3] if len(sys.argv) > 3 else "Accepted"
    )