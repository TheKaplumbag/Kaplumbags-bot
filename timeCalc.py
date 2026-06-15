import re

def calc(duration_str: str) -> str:
  duration_str = duration_str.strip().lower()
    
  if duration_str in ["0", "perma", "perm", "0s"]:
    return "0s"
      
    match = re.match(r"^(\d+)([mhdw]?)$", duration_str)
    if not match:
      return "0s"
        
    value = int(match.group(1))
    unit = match.group(2)
    
    # multipliers
    multipliers = {
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800, 
        "": 1, #If empty excepts the time as seconds
        "s": 1 
    }
    
    exact_seconds = value * multipliers.get(unit, 1)
    return f"{exact_seconds}s"