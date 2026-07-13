# IMPORTING LIBS
import os
import json
import requests
from dotenv import load_dotenv
from Functions.Utilities import send_log, FindUserId

# RETRIEVING ENVIRONMENT VARIABLES
load_dotenv()
GROUP_API : str = os.getenv("GROUP_API_KEY")
GROUP_ID : str = os.getenv("GROUP_ID")
COOKIE : str = os.getenv("COOKIE")

# Main Functions

def groupBans() -> str:
  pass

def groupBan() -> str:
  pass

def groupUnban() -> str:
  pass

def groupRoles() -> list:
  pass