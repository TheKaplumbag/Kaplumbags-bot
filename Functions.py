import requests
import json
import os
from timeCalc import calc
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
UNIVERSE_ID = os.getenv("UNIVERSE_ID")
COOKIE = os.getenv("COOKIE")

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
  try:
    response = requests.post(url, headers=headers, json=Body)
    if response.status_code == 200:
      data = response.json()
      if "data" not in data or not data["data"]:
        return "NO DATA HAS BEEN FOUND"
      else:
        return data["data"][0]["id"]
    else:
      print(f"AN ERROR HAS BEEN ACCOURED! {response.status_code}: {response.text} ")
  except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False


def UserGameBan(userId: int, duration: str, display_reason: str, private_reason: str, ban_alts: bool):
  url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/user-restrictions/{userId}"
  headers={
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
  }
  parsed_duration = calc(duration)
  display_reason = display_reason + " (DM thekaplumbag.)"
  restriction_data = {
    "active": True,
    "displayReason": display_reason,
    "privateReason": private_reason,
    "excludeAltAccounts": not ban_alts
  }

  if parsed_duration is not None:
    restriction_data["duration"] = parsed_duration

  Body = {
    "gameJoinRestriction": restriction_data
  }
  try:
    response = requests.patch(url,headers=headers,json=Body)
    if response.status_code == 200:
      return True, "BANNED!"
    else: 
      return False, f"ERROR: {response.status_code}, {response.text}"
  except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False
  
  
def GetGameBanHistory():
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


def UnGameBan(userId: int, display_reason: str, private_reason: str):
  url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/user-restrictions/{userId}"
  headers={
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
  }
  data = {
    "gameJoinRestriction": {
      "active": False,
      "displayReason": display_reason,
      "privateReason": private_reason
    }
  }
  try:
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
      return True, "UNBANNED!"
    else: 
      return False, f"ERROR: {response.status_code}, {response.text}"
  except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    return False


def GetPlayerHistory(userId: int, player: str):
  url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/user-restrictions:listLogs"
  headers={
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
  }
  query={
    "filter": f"user == 'users/{userId}'"
  }
  response = requests.get(url, headers=headers, params= query)
  
  if response.status_code == 200:
    data = json.loads(response.text)
    
    if "logs" not in data or not data["logs"]:
      return "📋 **Ban Logs:** No active bans found."
    
    formatted_message = f"📋 **ROBLOX BAN LOG OF {player.strip()}**\n\n"
    
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


def GroupBan():
  pass
