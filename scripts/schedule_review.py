import os
import json
from datetime import datetime, timedelta

REVIEW_INTERVALS = [1, 3, 7, 14, 30, 60]  # Days

def load_review_data():
    """Load review schedule data."""
    if os.path.exists('stats/reviews.json'):
        with open('stats/reviews.json', 'r') as f:
            return json.load(f)
    return {}

def save_review_data(data):
    """Save review schedule data."""
    os.makedirs('stats', exist_ok=True)
    with open('stats/reviews.json', 'w') as f:
        json.dump(data, f, indent=2)

def find_problem_path(problem_number):
    """Find the path to a problem folder."""
    problem_num = str(problem_number).zfill(4)
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
                    return os.path.join(range_path, folder), folder
    
    return None, None

def mark_reviewed(problem_number):
    """Mark a problem as reviewed and schedule next review."""
    data = load_review_data()
    problem_id = str(problem_number).zfill(4)
    
    # Find the problem to get its title
    problem_path, folder_name = find_problem_path(problem_number)
    
    if not problem_path:
        print(f"❌ Problem #{problem_number} not found!")
        return
    
    title = ' '.join(folder_name.split('-')[1:]).title()
    
    if problem_id not in data:
        data[problem_id] = {
            'title': title,
            'review_count': 0,
            'last_reviewed': None,
            'next_review': None
        }
    
    review_count = data[problem_id]['review_count']
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Calculate next review date
    if review_count < len(REVIEW_INTERVALS):
        days_until_next = REVIEW_INTERVALS[review_count]
    else:
        days_until_next = 90  # Review every 3 months after mastery
    
    next_review = (datetime.now() + timedelta(days=days_until_next)).strftime('%Y-%m-%d')
    
    data[problem_id]['review_count'] = review_count + 1
    data[problem_id]['last_reviewed'] = today
    data[problem_id]['next_review'] = next_review
    data[problem_id]['title'] = title
    
    save_review_data(data)
    
    print(f"✅ Marked #{problem_number}: {title} as reviewed")
    print(f"📅 Next review scheduled for: {next_review}")
    print(f"🔢 Review count: {review_count + 1}")

def show_due_reviews():
    """Show problems that need review today."""
    data = load_review_data()
    today = datetime.now().strftime('%Y-%m-%d')
    
    due_problems = []
    
    for problem_id, info in data.items():
        if info['next_review'] and info['next_review'] <= today:
            due_problems.append({
                'id': problem_id,
                'title': info.get('title', 'Unknown'),
                'next_review': info['next_review'],
                'review_count': info['review_count']
            })
    
    if not due_problems:
        print("🎉 No problems due for review today!")
        return
    
    print(f"📚 {len(due_problems)} problem(s) due for review:\n")
    
    due_problems.sort(key=lambda x: x['next_review'])
    
    for problem in due_problems:
        print(f"  #{problem['id']}: {problem['title']}")
        print(f"    Review #{problem['review_count'] + 1} | Due: {problem['next_review']}")
        print()

def show_schedule():
    """Show complete review schedule."""
    data = load_review_data()
    
    if not data:
        print("No problems scheduled for review yet.")
        return
    
    upcoming = []
    for problem_id, info in data.items():
        if info['next_review']:
            upcoming.append({
                'id': problem_id,
                'title': info.get('title', 'Unknown'),
                'date': info['next_review'],
                'count': info['review_count']
            })
    
    upcoming.sort(key=lambda x: x['date'])
    
    print("📅 Upcoming Reviews:\n")
    
    current_date = None
    for item in upcoming[:20]:  # Show next 20
        if item['date'] != current_date:
            print(f"\n{item['date']}:")
            current_date = item['date']
        
        print(f"  • #{item['id']}: {item['title']} (Review #{item['count'] + 1})")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Commands:")
        print("  python schedule_review.py due       - Show problems due today")
        print("  python schedule_review.py schedule  - Show complete schedule")
        print("  python schedule_review.py mark <#>  - Mark problem as reviewed")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "due":
        show_due_reviews()
    elif command == "schedule":
        show_schedule()
    elif command == "mark" and len(sys.argv) > 2:
        mark_reviewed(sys.argv[2])
    else:
        print("Invalid command!")