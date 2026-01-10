import os
import sys
from datetime import datetime

def create_problem(number, title, difficulty, topics, companies="", link=""):
    """
    Create a new problem folder with README and Solution1.java
    
    Usage:
        python scripts/create_problem.py 1458 "Max Dot Product of Two Subsequences" hard "Array,Dynamic Programming"
    """
    
    problem_num = str(number).zfill(4)
    folder_name = f"{problem_num}-{title.lower().replace(' ', '-').replace('/', '-')}"
    
    # Determine range folder
    num = int(number)
    if num <= 500:
        range_folder = "0000-0500"
    elif num <= 1000:
        range_folder = "0501-1000"
    elif num <= 1500:
        range_folder = "1001-1500"
    elif num <= 2000:
        range_folder = "1501-2000"
    elif num <= 2500:
        range_folder = "2001-2500"
    else:
        range_folder = "2501-3000"
    
    difficulty_map = {
        'easy': '1. easy',
        'medium': '2. medium',
        'hard': '3. hard'
    }
    
    difficulty_folder = difficulty_map.get(difficulty.lower())
    problem_path = os.path.join(difficulty_folder, range_folder, folder_name)
    
    os.makedirs(problem_path, exist_ok=True)
    print(f"✅ Created folder: {problem_path}")
    
    # Create README.md
    topics_formatted = ', '.join([f'`{t.strip()}`' for t in topics.split(',')])
    companies_formatted = ', '.join([f'`{c.strip()}`' for c in companies.split(',')]) if companies else 'N/A'
    
    readme_content = f"""# [{problem_num}]. {title}

**Difficulty:** {difficulty.title()}  
**Topics:** {topics_formatted}  
**Companies:** {companies_formatted}  
**Link:** [{title}](https://leetcode.com/problems/{title.lower().replace(' ', '-')}/)

---

## Problem Statement

[Paste problem description here]

**Example 1:**
```
Input: 
Output: 
Explanation: 
```

**Example 2:**
```
Input: 
Output: 
```

**Constraints:**
- 

---

## Solutions

### ⭐ Solution 1: [Approach Name]
**File:** `Solution1.java`  
**Status:** ✅ Accepted / ❌ TLE / ❌ MLE / ⚠️ Wrong Answer

**Approach:**
- 

**Complexity:**
- ⏱️ Time: O()
- 💾 Space: O()

---

## Key Insights

- 

---

**Date Solved:** {datetime.now().strftime('%B %d, %Y')}  
**Review Count:** 0  
**Next Review:** {datetime.now().strftime('%B %d, %Y')}
"""
    
    with open(os.path.join(problem_path, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✅ Created README.md")
    
    # Create Solution1.java
    solution_content = f"""// LeetCode #{problem_num}: {title}
// Approach: [Approach Name]
// Status: ✅ Accepted / ❌ TLE / ❌ MLE
// Time: O()  |  Space: O()

class Solution {{
    // Paste your LeetCode solution here
}}
"""
    
    with open(os.path.join(problem_path, "Solution1.java"), 'w', encoding='utf-8') as f:
        f.write(solution_content)
    print(f"✅ Created Solution1.java")
    
    print(f"\n🎉 Done! Location: {problem_path}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python create_problem.py <number> <title> <difficulty> <topics> [companies]")
        print('Example: python create_problem.py 1458 "Max Dot Product" hard "Array,DP"')
        sys.exit(1)
    
    create_problem(
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
        sys.argv[5] if len(sys.argv) > 5 else ""
    )