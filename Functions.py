import request 
import json
import 

def FindUserId(username: str):
  username = username.strip()
  url = "https://users.roblox.com/v1/usernames/users"
  headers = {
    "Content-Type": "application/json"
  }
  Body = {
    "usernames": [
      username
      ],
      "excludeBannedUsers": True
  }
  response = requests.post(url, headers=headers, json=Body)
  if response.status_code == 200:
    data = response.json()
    if "data" not in data or not data["data"]:
      return "NO DATA HAS BEEN FOUND"
    else:
      return data["data"][0]["id"]
  else:
    print(f"AN ERROR HAS BEEN ACCOURED! {response.status_code}: {response.text} ")
    return f"AN ERROR HAS BEEN ACCOURED! {response.status_code}: {response.text}"


def UserGameBan(userId: int, duration: str, display-reason: str, private-reason: str, ban-alts: bool):
  url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/user-restrictions/{userId}"
  headers={
    "Content-Type": "application/json"
  }
  Body = {
      "gameJoinRestriction": {
        "active": True,
        "duration": duration,
        "displayReason": display-reason,
        "privateReason": private-reason,
        "excludeAltAccounts": not ban-alts
      }
    }
  response = requests.patch(url,headers=headers,json=Body)
  if response.status_code == 200:
    return True, "BANNED!"
  else: 
    return False, f"ERROR: {response.status_code}, {response.text}"
  

def GetFullBanList():
  url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/user-restrictions:listLogs"
  headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
  }
  
  response = requests.get(url, headers=headers)
  
  if response.status_code == 200:
    data = json.loads(response.text)
    
    if "logs" not in data or not data["logs"]:
      return "📋 **Ban Logs:** No active bans found."
    
    formatted_message = "📋 **ROBLOX BAN LOGS**\n\n"
    
    for log in data["logs"]:
      user_id = log["user"].split("/")[-1]
      mod_id = log["moderator"]["robloxUser"].split("/")[-1]
      
      user_link = f"https://www.roblox.com/users/{user_id}/profile"
      mod_link = f"https://www.roblox.com/users/{mod_id}/profile"
      
      public_reason = log.get("displayReason", "No reason provided")
      private_reason = log.get("privateReason", "No internal reason")
      
      formatted_message += f"👤 **User:** [Profile Link]({user_link}) *(ID: {user_id})*\n"
      formatted_message += f"🛠️ **Moderator:** [Profile Link]({mod_link})\n"
      formatted_message += f"📄 **Reason:** {public_reason}\n"
      formatted_message += f"🔒 **Internal Note:** *{private_reason}*\n"
      formatted_message += "---------------------------------------\n"
        
    return formatted_message

  else:
    print(f"API Error {response.status_code}: {response.text}")
    return f"⚠️ API Error: {response.status_code}"

