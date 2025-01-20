from typing import Annotated
import json
import logging
from livekit.agents import llm
import os
from dotenv import load_dotenv
import aiohttp

logger = logging.getLogger("functions")
logger.setLevel(logging.INFO)

class AssistantFnc(llm.FunctionContext):
    def __init__(self, room=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_user_transcript = None
        self.room = room  # Store the room object
        # Initialize environment variables
        load_dotenv(dotenv_path=".env.local")
        
    @llm.ai_callable()
    async def get_weather(
            self,
            location: Annotated[
                str, llm.TypeInfo(description="The location to get the weather for")
            ],
    ):
        """Called when the user asks about the weather. This function will return the weather for the given location."""
        logger.info(f"getting weather for {location}")
        url = f"https://wttr.in/{location}?format=%C+%t"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    weather_data = await response.text()
                    # Send weather data to frontend via RPC
                    if self.room and self.room.local_participant:
                        try:
                            await self.room.local_participant.perform_rpc(
                                destination_identity="frontend",  # Broadcast to all participants
                                method="displayWeather",
                                payload=json.dumps({
                                    "location": location,
                                    "weather": weather_data
                                })
                            )
                        except Exception as e:
                            logger.error(f"Failed to send weather data to frontend: {e}")
                    
                    return f"The weather in {location} is {weather_data}."
                else:
                    raise f"Failed to get weather data, status code: {response.status}"
  
