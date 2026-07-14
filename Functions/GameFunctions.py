import requests
import json
import os
from Functions.Utilities import calculate
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
UNIVERSE_ID = os.getenv("UNIVERSE_ID")
COOKIE = os.getenv("COOKIE")


def UserGameBan(userId: int, duration: str, display_reason: str, private_reason: str, ban_alts: bool) -> bool | str:
  url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/user-restrictions/{userId}"
  headers={
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
  }
  parsed_duration = calculate(duration)
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
  

def GetCurrentBans() -> str:
  url = f"https://apis.roblox.com/cloud/v2/universes/{UNIVERSE_ID}/user-restrictions"
  headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    data = json.loads(response.text)

    if "logs" not in data or not data["logs"]:
      return "📋 **Ban Logs:** No active bans found."

    user_ids = []
    for log in data["logs"]:
      user_id = log["user"].split("/")[-1]
      user_ids.append(int(user_id))

    user_ids = list(set(user_ids))

    username_map = {}
    if user_ids:
      users_url = "https://users.roblox.com/v1/users"
      payload = {"userIds": user_ids, "excludeBannedUsers": False}
      try:
        users_res = requests.post(users_url, json=payload)
        if users_res.status_code == 200:
          users_data = users_res.json().get("data", [])
          for user in users_data:
            username_map[str(user["id"])] = user["name"]
      except Exception as e:
        print(f"Error fetching usernames: {e}")

    formatted_message = "📋 **ROBLOX BAN LOGS**\n\n"

    for log in data["logs"]:
      user_id = log["user"].split("/")[-1]
      mod_id = log["moderator"]["robloxUser"].split("/")[-1]

      username = username_map.get(user_id, "Unknown_Player")

      user_link = f"https://www.roblox.com/users/{user_id}/profile"
      mod_link = f"https://www.roblox.com/users/{mod_id}/profile"

      public_reason = log.get("displayReason", "No reason provided")
      private_reason = log.get("privateReason", "No internal reason")

      formatted_message += (
          f"👤 **User:** [{username}]({user_link}) *(ID: {user_id})*\n"
      )
      formatted_message += (
          f"🛠️ **Moderator:** [Profile Link]({mod_link})\n"
      )
      formatted_message += f"📄 **Reason:** {public_reason}\n"
      formatted_message += f"🔒 **Internal Note:** {private_reason}\n"
      formatted_message += (
          "--------------------------------------------------\n"
      )

    return formatted_message

  else:
    print(f"API Error {response.status_code}: {response.text}")
    return f"⚠️ API Error: {response.status_code}"


def UnGameBan(userId: int, display_reason: str, private_reason: str) -> bool | str:
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


def GetPlayerHistory(userId: int, player: str) -> str:
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
      return "📋 **Ban History:** No history found."
    
    formatted_message = f"📋 **ROBLOX BAN HISTORY OF {player.strip()}**\n\n"
    
    for log in data["logs"]:
      user_id = log["user"].split("/")[-1]
      mod_id = log["moderator"]["robloxUser"].split("/")[-1]
      
      user_link = f"https://www.roblox.com/users/{user_id}/profile"
      mod_link = f"https://www.roblox.com/users/{mod_id}/profile"
      
      public_reason = log.get("displayReason", "No reason provided")
      private_reason = log.get("privateReason", "No internal reason")
      isActive = log.get("active", "N/A")
      
      formatted_message += f"👤 **User:** [{player}]({user_link}) *(ID: {user_id})*\n"
      formatted_message += f"🛠️ **Moderator:** [Profile Link]({mod_link})\n"
      formatted_message += f"❓ **Is Active:** {isActive}\n"
      formatted_message += f"📄 **Reason:** {public_reason}\n"
      formatted_message += f"🔒 **Internal Note:** *{private_reason}*\n"
      formatted_message += "---------------------------------------\n"
        
    return formatted_message
  else:
    print(f"API Error {response.status_code}: {response.text}")
    return f"⚠️ API Error: {response.status_code}"
