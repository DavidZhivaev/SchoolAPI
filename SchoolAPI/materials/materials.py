import aiohttp # type: ignore
import asyncio
import json
from utils.classCreater import JsonToClassConverter
from errors.errors import TokenError, DnevnikError
from student.student import Student
from typing import Union


class Materials:
    def __init__(self, student: Student) -> None:
        self.student = student
        
    async def getAllMaterials(self):
        async with aiohttp.ClientSession() as session:
            payload = {
                "query": {
                    "filter": {
                        "sorting": {
                            "field": "published_at",
                            "direction": "desc"
                        }
                    }
                }, 
                "sort": {
                    "field": "published_at",
                    "order": "desc"
                }, 
                "page": 1,
                "per_page": 100000,
                "scope":"catalogue"
            }

            response = await session.post(
                f"https://uchebnik.mos.ru/search/api/v3/materials",
                headers={
                    "Authorization": f"Bearer {self.student.token}",
                    "User-Id": str(self.student.id),
                    "Profile-Id": str(self.student.profiles[0]['id']),
                    "Profile": str({"id":self.student.profiles[0]['id'],"type":"student","x-mes-globalRoleId":"1","organizationIds":"[]"})
                }, json=payload
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.post(
                    f"https://uchebnik.mos.ru/search/api/v3/materials",
                    headers={
                        "Authorization": f"Bearer {self.student.token}",
                        "User-Id": str(self.student.id),
                        "Profile-Id": str(self.student.profiles[0]['id']),
                        "Profile": str({"id":self.student.profiles[0]['id'],"type":"student","x-mes-globalRoleId":"1","organizationIds":"[]"})
                    }, json=payload
                )

            response = await response.json()

            Materials = JsonToClassConverter.convert("Materials", response)
            Materials.json = response

            return Materials
        
    
    async def getScheduleByDate(self, date: str):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/family/web/v1/schedule?student_id={self.student.id}&date={date}",
                headers={
                    "Auth-Token": self.student.token,
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/family/web/v1/schedule?student_id={self.student.id}&date={date}",
                    headers={
                        "Auth-Token": self.student.token,
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            ScheduleDay = JsonToClassConverter.convert("ScheduleDay", response)
            ScheduleDay.json = response

            return ScheduleDay
        
    
    async def getScheduleByDate(self, date: str):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/family/web/v1/schedule?student_id={self.student.id}&date={date}",
                headers={
                    "Auth-Token": self.student.token,
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/family/web/v1/schedule?student_id={self.student.id}&date={date}",
                    headers={
                        "Auth-Token": self.student.token,
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            ScheduleDay = JsonToClassConverter.convert("ScheduleDay", response)
            ScheduleDay.json = response

            return ScheduleDay
        

    async def getScheduleByDate(self, date: str):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/family/web/v1/schedule?student_id={self.student.id}&date={date}",
                headers={
                    "Auth-Token": self.student.token,
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/family/web/v1/schedule?student_id={self.student.id}&date={date}",
                    headers={
                        "Auth-Token": self.student.token,
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            ScheduleDay = JsonToClassConverter.convert("ScheduleDay", response)
            ScheduleDay.json = response

            return ScheduleDay
        

    async def getScheduleByDate(self, date: str):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/family/web/v1/schedule?student_id={self.student.id}&date={date}",
                headers={
                    "Auth-Token": self.student.token,
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/family/web/v1/schedule?student_id={self.student.id}&date={date}",
                    headers={
                        "Auth-Token": self.student.token,
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            ScheduleDay = JsonToClassConverter.convert("ScheduleDay", response)
            ScheduleDay.json = response

            return ScheduleDay
        

    async def getScheduleByDate(self, date: str):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/family/web/v1/schedule?student_id={self.student.id}&date={date}",
                headers={
                    "Auth-Token": self.student.token,
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/family/web/v1/schedule?student_id={self.student.id}&date={date}",
                    headers={
                        "Auth-Token": self.student.token,
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            ScheduleDay = JsonToClassConverter.convert("ScheduleDay", response)
            ScheduleDay.json = response

            return ScheduleDay