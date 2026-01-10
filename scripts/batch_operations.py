import os
import sys

def list_all_solutions():
    """List all Java solution files in the repository."""
    total_problems = 0
    total_solutions = 0
    
    difficulty_folders = ['1. easy', '2. medium', '3. hard']
    
    for difficulty in difficulty_folders:
        if not os.path.exists(difficulty):
            continue
        
        print(f"\n📁 {difficulty.upper()}")
        print("-" * 50)
        
        problem_count = 0
        
        for range_folder in sorted(os.listdir(difficulty)):
            range_path = os.path.join(difficulty, range_folder)
            
            if not os.path.isdir(range_path):
                continue
            
            for problem_folder in sorted(os.listdir(range_path)):
                problem_path = os.path.join(range_path, problem_folder)
                
                if not os.path.isdir(problem_path):
                    continue
                
                java_files = [f for f in os.listdir(problem_path) if f.endswith('.java')]
                
                if java_files:
                    problem_count += 1
                    total_problems += 1
                    total_solutions += len(java_files)
                    print(f"  #{problem_folder.split('-')[0]}: {' '.join(problem_folder.split('-')[1:]).title()}")
                    print(f"       Solutions: {len(java_files)} | Files: {', '.join(java_files)}")
        
        print(f"\n  Subtotal: {problem_count} problems")
    
    print(f"\n{'='*50}")
    print(f"✅ Total Problems: {total_problems}")
    print(f"✅ Total Solutions: {total_solutions}")

def show_stats():
    """Show quick statistics."""
    stats = {'easy': 0, 'medium': 0, 'hard': 0}
    
    difficulty_map = {
        '1. easy': 'easy',
        '2. medium': 'medium', 
        '3. hard': 'hard'
    }
    
    for folder, diff in difficulty_map.items():
        if not os.path.exists(folder):
            continue
        
        for range_folder in os.listdir(folder):
            range_path = os.path.join(folder, range_folder)
            if os.path.isdir(range_path):
                for problem in os.listdir(range_path):
                    if os.path.isdir(os.path.join(range_path, problem)):
                        stats[diff] += 1
    
    total = sum(stats.values())
    
    print("\n📊 LeetCode Progress")
    print("=" * 30)
    print(f"🟢 Easy:   {stats['easy']}")
    print(f"🟡 Medium: {stats['medium']}")
    print(f"🔴 Hard:   {stats['hard']}")
    print("-" * 30)
    print(f"📈 Total:  {total}")

def find_problem(query):
    """Search for a problem by number or name."""
    query = query.lower()
    results = []
    
    difficulty_folders = ['1. easy', '2. medium', '3. hard']
    
    for difficulty in difficulty_folders:
        if not os.path.exists(difficulty):
            continue
        
        for range_folder in os.listdir(difficulty):
            range_path = os.path.join(difficulty, range_folder)
            
            if not os.path.isdir(range_path):
                continue
            
            for problem_folder in os.listdir(range_path):
                if query in problem_folder.lower():
                    results.append({
                        'folder': problem_folder,
                        'path': os.path.join(range_path, problem_folder),
                        'difficulty': difficulty
                    })
    
    if not results:
        print(f"❌ No problems found matching '{query}'")
        return
    
    print(f"\n🔍 Found {len(results)} result(s):\n")
    for r in results:
        print(f"  {r['difficulty']}: {r['folder']}")
        print(f"  Path: {r['path']}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Commands:")
        print("  python batch_operations.py list       - List all problems and solutions")
        print("  python batch_operations.py stats      - Show quick statistics")
        print("  python batch_operations.py find <q>   - Search for a problem")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        list_all_solutions()
    elif command == "stats":
        show_stats()
    elif command == "find" and len(sys.argv) > 2:
        find_problem(sys.argv[2])
    else:
        print(f"Unknown command: {command}")