import os
import json
from datetime import datetime
from collections import defaultdict

def scan_problems():
    """Scan all problem folders and collect statistics."""
    stats = {
        'easy': {'count': 0, 'problems': []},
        'medium': {'count': 0, 'problems': []},
        'hard': {'count': 0, 'problems': []},
        'topics': defaultdict(lambda: {'easy': 0, 'medium': 0, 'hard': 0}),
        'companies': defaultdict(int),
        'recent': []
    }
    
    # Updated to match actual folder structure
    difficulty_map = {
        '1. easy': 'easy',
        '2. medium': 'medium',
        '3. hard': 'hard'
    }
    
    for folder_name, difficulty in difficulty_map.items():
        if not os.path.exists(folder_name):
            continue
            
        for range_folder in os.listdir(folder_name):
            range_path = os.path.join(folder_name, range_folder)
            
            if not os.path.isdir(range_path):
                continue
            
            for problem_folder in os.listdir(range_path):
                problem_path = os.path.join(range_path, problem_folder)
                
                if not os.path.isdir(problem_path):
                    continue
                
                readme_path = os.path.join(problem_path, 'README.md')
                
                if os.path.exists(readme_path):
                    # Check if there's at least one Java solution file
                    has_solution = any(f.endswith('.java') for f in os.listdir(problem_path))
                    
                    stats[difficulty]['count'] += 1
                    
                    # Extract problem info from README
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Extract title
                        title_line = content.split('\n')[0]
                        title = title_line.split('].')[1].strip() if '].' in title_line else problem_folder
                        
                        # Extract topics
                        if '**Topics:**' in content:
                            topics_line = content.split('**Topics:**')[1].split('\n')[0]
                            topics = [t.strip('` ') for t in topics_line.split(',')]
                            for topic in topics:
                                if topic:
                                    stats['topics'][topic][difficulty] += 1
                        
                        # Extract companies
                        if '**Companies:**' in content:
                            companies_line = content.split('**Companies:**')[1].split('\n')[0]
                            companies = [c.strip('` ') for c in companies_line.split(',')]
                            for company in companies:
                                if company and company != 'N/A':
                                    stats['companies'][company] += 1
                        
                        # Extract date solved
                        date_solved = None
                        if '**Date Solved:**' in content:
                            date_line = content.split('**Date Solved:**')[1].split('\n')[0].strip()
                            date_solved = date_line
                        
                        # Count Java solutions
                        java_solutions = [f for f in os.listdir(problem_path) if f.endswith('.java')]
                        
                        problem_info = {
                            'number': problem_folder.split('-')[0],
                            'title': title,
                            'difficulty': difficulty,
                            'path': problem_path,
                            'date': date_solved,
                            'solutions': len(java_solutions)
                        }
                        
                        stats[difficulty]['problems'].append(problem_info)
                        stats['recent'].append(problem_info)
    
    # Sort recent by date (most recent first)
    def parse_date(date_str):
        if not date_str:
            return datetime.min
        try:
            return datetime.strptime(date_str, '%B %d, %Y')
        except:
            return datetime.min
    
    stats['recent'] = sorted(
        stats['recent'], 
        key=lambda x: parse_date(x['date']),
        reverse=True
    )[:10]
    
    return stats

def update_root_readme(stats):
    """Update the root README.md with latest statistics."""
    
    total_solved = sum(stats[d]['count'] for d in ['easy', 'medium', 'hard'])
    
    # Approximate totals (update these based on actual LeetCode counts)
    total_easy = 700
    total_medium = 1500
    total_hard = 600
    total_problems = total_easy + total_medium + total_hard
    
    easy_pct = (stats['easy']['count'] / total_easy * 100) if total_easy > 0 else 0
    medium_pct = (stats['medium']['count'] / total_medium * 100) if total_medium > 0 else 0
    hard_pct = (stats['hard']['count'] / total_hard * 100) if total_hard > 0 else 0
    total_pct = (total_solved / total_problems * 100) if total_problems > 0 else 0
    
    progress_table = f"""| Difficulty | Solved | Total | Percentage |
|------------|--------|-------|------------|
| 🟢 Easy    | {stats['easy']['count']}    | {total_easy}   | {easy_pct:.1f}%      |
| 🟡 Medium  | {stats['medium']['count']}     | {total_medium}  | {medium_pct:.1f}%       |
| 🔴 Hard    | {stats['hard']['count']}     | {total_hard}   | {hard_pct:.1f}%       |
| **Total**  | **{total_solved}**| **{total_problems}** | **{total_pct:.1f}%** |"""

    # Recently solved table
    recent_table = "| # | Title | Difficulty | Solutions | Date |\n|---|-------|------------|-----------|------|\n"
    for i, problem in enumerate(stats['recent'][:5], 1):
        diff_emoji = '🟢' if problem['difficulty'] == 'easy' else '🟡' if problem['difficulty'] == 'medium' else '🔴'
        solutions_count = problem.get('solutions', 1)
        recent_table += f"| {i} | [{problem['title']}]({problem['path'].replace(os.sep, '/')}) | {diff_emoji} {problem['difficulty'].title()} | {solutions_count} Java | {problem['date']} |\n"
    
    # Topics table
    topics_table = ""
    sorted_topics = sorted(stats['topics'].items(), key=lambda x: sum(x[1].values()), reverse=True)[:10]
    for topic, counts in sorted_topics:
        total = sum(counts.values())
        topics_table += f"\n### {topic} ({total})\n"
        topics_table += f"- Easy: {counts['easy']} | Medium: {counts['medium']} | Hard: {counts['hard']}\n"
    
    readme_content = f"""# 🚀 LeetCode Solutions (Java)

My personal collection of LeetCode problem solutions in **Java** with multiple approaches and detailed explanations.

## 📊 Progress Statistics

{progress_table}

**Last Updated:** {datetime.now().strftime('%B %d, %Y')}

---

## 📁 Repository Structure

```
leetcode-solutions/
├── 1. easy/        # Easy problems organized by number ranges
├── 2. medium/      # Medium problems organized by number ranges
├── 3. hard/        # Hard problems organized by number ranges
├── resources/      # Patterns, algorithms, data structures guides
├── scripts/        # Automation scripts
└── stats/          # Progress tracking and topic-wise statistics
```

---

## 🔥 Recently Solved

{recent_table}

---

## 📚 Problems by Topic (Top 10)
{topics_table}

[See complete topic breakdown →](stats/topics.md)

---

## 🎯 Quick Start

### Create a new problem:
```bash
python scripts/create_problem.py <number> "<title>" <difficulty> "<topics>" "<companies>"
```

### Update statistics:
```bash
python scripts/update_stats.py
```

### Add a new solution:
```bash
python scripts/add_solution.py <problem-number> "<approach-name>"
```

### Compile and run a solution:
```bash
javac "1. easy/0000-0500/0001-two-sum/Solution1.java"
java -cp "1. easy/0000-0500/0001-two-sum" Solution1
```

---

## 🛠️ How to Use

1. **Navigate by difficulty and number range**
   ```
   1. easy/0000-0500/0001-two-sum/
   ```

2. **Each problem folder contains:**
   - `README.md` - Problem statement and all solutions
   - `Solution1.java`, `Solution2.java` - Java implementation files
   - `notes.md` - Personal insights (optional)

3. **Multiple solutions per problem:**
   - Optimal solution (marked with ⭐)
   - Alternative approaches
   - Brute force (for learning)

---

## 📖 Naming Conventions

- **Problem folders:** `0001-problem-name`
- **Solution files:** `Solution1.java`, `Solution2.java`, etc.
- **Always use:** 4-digit numbers, kebab-case, lowercase for folders

---

## 📝 Git Commit Convention

```bash
[Add] #0001: Two Sum - Hash map solution
[Optimize] #0042: Improved space complexity
[Update] #0015: Added two pointers approach
[Docs] Updated README with stats
```

---

**Author:** Your Name  
**Started:** January 1, 2025  
**Language:** Java ☕

---

*This repository is automatically updated using automation scripts.*
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Updated README.md")

def update_topics_md(stats):
    """Create detailed topics breakdown."""
    
    os.makedirs('stats', exist_ok=True)
    
    content = f"""# Topics Breakdown

**Last Updated:** {datetime.now().strftime('%B %d, %Y')}

---

"""
    
    sorted_topics = sorted(stats['topics'].items(), key=lambda x: sum(x[1].values()), reverse=True)
    
    difficulty_folder_map = {
        'easy': '1. easy',
        'medium': '2. medium',
        'hard': '3. hard'
    }
    
    for topic, counts in sorted_topics:
        total = sum(counts.values())
        content += f"## {topic} ({total} problems)\n\n"
        content += f"- 🟢 Easy: {counts['easy']}\n"
        content += f"- 🟡 Medium: {counts['medium']}\n"
        content += f"- 🔴 Hard: {counts['hard']}\n\n"
        
        # List problems for this topic
        content += "### Problems:\n\n"
        
        for difficulty in ['easy', 'medium', 'hard']:
            if counts[difficulty] > 0:
                for problem in stats[difficulty]['problems']:
                    readme_path = os.path.join(problem['path'], 'README.md')
                    if os.path.exists(readme_path):
                        with open(readme_path, 'r', encoding='utf-8') as f:
                            if topic in f.read():
                                rel_path = problem['path'].replace(os.sep, '/')
                                content += f"- [{problem['number']}. {problem['title']}](../{rel_path})\n"
        
        content += "\n---\n\n"
    
    with open('stats/topics.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated stats/topics.md")

def save_stats_json(stats):
    """Save statistics as JSON for other scripts to use."""
    os.makedirs('stats', exist_ok=True)
    
    # Convert defaultdict to regular dict for JSON serialization
    stats_json = {
        'easy': stats['easy'],
        'medium': stats['medium'],
        'hard': stats['hard'],
        'topics': dict(stats['topics']),
        'companies': dict(stats['companies']),
        'language': 'Java',
        'last_updated': datetime.now().isoformat()
    }
    
    with open('stats/data.json', 'w', encoding='utf-8') as f:
        json.dump(stats_json, f, indent=2)
    
    print("✅ Saved stats/data.json")

if __name__ == "__main__":
    print("🔄 Scanning problems...")
    stats = scan_problems()
    
    print("\n📝 Updating documentation...")
    update_root_readme(stats)
    update_topics_md(stats)
    save_stats_json(stats)
    
    print("\n✨ Statistics updated successfully!")
    print(f"\nSummary:")
    print(f"  Easy: {stats['easy']['count']}")
    print(f"  Medium: {stats['medium']['count']}")
    print(f"  Hard: {stats['hard']['count']}")
    print(f"  Total: {sum(stats[d]['count'] for d in ['easy', 'medium', 'hard'])}")
    print(f"  Language: Java ☕")