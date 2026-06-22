# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


discount_codes_store = {
    "WELCOME50": {"discount": 50, "redeemed_by": []},
    "SUMMER20": {"discount": 20, "redeemed_by": []},
}

def redeem_discount_code(code: str, user_id: str) -> str:
    """Redeems a single-use discount code for a registered user.

    Args:
        code: The discount code to redeem (e.g., WELCOME50, SUMMER20).
        user_id: The ID of the registered user attempting to redeem the code.

    Returns:
        A string indicating the success or failure of the redemption.
    """
    code = code.upper()
    if code not in discount_codes_store:
        return f"Invalid discount code: {code}."

    code_data = discount_codes_store[code]
    if user_id in code_data["redeemed_by"]:
        return f"User {user_id} has already redeemed the code {code}."

    code_data["redeemed_by"].append(user_id)
    return f"Successfully redeemed code {code} for user {user_id}. Applied {code_data['discount']}% discount."


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        api_key="AIzaSyD-mock-key-value-12345",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are a helpful AI shopping assistant for a retail store.",
    tools=[redeem_discount_code],
)

app = App(
    root_agent=root_agent,
    name="app",
)
