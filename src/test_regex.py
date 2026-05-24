import re

def scan_file_for_injections(file_path):
    # Updated patterns using .* to catch filler words inserted by attackers
    danger_patterns = [
        r"ignore.*previous.*instructions",
        r"system.*override",
        r"reveal.*password"
    ]
    
    print(f"Reading target file: {file_path}")
    
    with open(file_path, "r") as file:
        content = file.read()
        
    print(f"File Contents: \"{content.strip()}\"")
    
    for pattern in danger_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"\n[ALERT DETECTED] Triggered security match for pattern: '{pattern}'")
            return True
            
    print("\n[CLEAN] No obvious rule-based risks detected.")
    return False

if __name__ == "__main__":
    scan_file_for_injections("attacks/sample_attack.txt")