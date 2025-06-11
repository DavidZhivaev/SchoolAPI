import aiohttp # type: ignore
import asyncio
import json
from typing import Union
from utils.classCreater import JsonToClassConverter
from errors.errors import TokenError, DnevnikError
from student.student import Student


class Notification:
    def __init__(self, student: Student) -> None:
        self.student = student

    async def getNotifications(self):
        async with aiohttp.ClientSession() as session:
            profile = await self.student.getStudentProfiles()
            response = await session.get(f"https://school.mos.ru/api/family/mobile/v1/notifications/search?student_id={self.student.id}",
                headers={
                    'Auth-Token': self.student.token,
                    'Profile-Id': str(profile.id),
                    "x-mes-subsystem": "familymp"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(f"https://school.mos.ru/api/family/mobile/v1/notifications/search?student_id={self.student.id}",
                    headers={
                        'Auth-Token': self.student.token,
                        'Profile-Id': str(profile.id),
                        "x-mes-subsystem": "familymp"
                    }
                )

            response = await response.json()

            notifications = JsonToClassConverter.convert("Notifications", response)
            return notifications