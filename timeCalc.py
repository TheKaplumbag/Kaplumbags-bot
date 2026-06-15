import re

def calc(duration_str: str) -> str:
  duration_str = duration_str.strip().lower()
  perms =  ["0", "perma", "perm", "0s"]
  if duration_str in perms:
    return None
  else: 
      match = re.match(r"^(\d+)([mhdw]?)$", duration_str)
      if not match:
        return None
        
      value = int(match.group(1))
      unit = match.group(2)
    
    # multipliers
      multipliers = {
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800, 
        "": 1, #If empty excepts the time as seconds
        }
    
      exact_seconds = value * multipliers.get(unit, 1)
      return f"{exact_seconds}s"