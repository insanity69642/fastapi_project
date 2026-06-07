from dataclasses import dataclass
from dotenv import load_dotenv
from typing import *
import fastapi as fapi
import supabase as sb
import postgrest as sbt
import os

load_dotenv()

client: sb.Client = sb.create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
table: sbt.SyncRequestBuilder = client.from_("persons")