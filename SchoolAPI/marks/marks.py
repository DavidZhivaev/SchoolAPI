import aiohttp # type: ignore
import asyncio
import json
from utils.classCreater import JsonToClassConverter
from errors.errors import TokenError, DnevnikError
from student.student import Student

class Marks:
    def __init__(self, student: Student) -> None:
        self.student = student

    async def getMarksByDate(self, from_date: str, to_date: str):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/family/web/v1/marks?student_id={self.student.id}&from={from_date}&to={to_date}",
                headers={
                    "Auth-Token": self.student.token,
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/family/web/v1/marks?student_id={self.student.id}&from={from_date}&to={to_date}",
                    headers={
                        "Auth-Token": self.student.token,
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            MarksObject = JsonToClassConverter.convert("MarksObject", response)
            MarksObject.json = response

            return MarksObject
        
    
    async def getSubjectsMarks(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/family/web/v1/subject_marks?student_id={self.student.profiles[0]['id']}",
                headers={
                    "Authorization": f"Bearer {self.student.token}",
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/family/web/v1/subject_marks?student_id={self.student.profiles[0]['id']}",
                    headers={
                        "Authorization": f"Bearer {self.student.token}",
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            MarksObject = JsonToClassConverter.convert("MarksObject", response)
            MarksObject.json = response

            return MarksObject
        

    async def getFinalMarks(self, period: int = 13):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/family/web/v1/final_marks/v2?person_id={self.student.person_id}&academic_year_id={period}",
                headers={
                    "Authorization": f"Bearer {self.student.token}",
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/family/web/v1/final_marks/v2?person_id={self.student.person_id}&academic_year_id={period}",
                    headers={
                        "Authorization": f"Bearer {self.student.token}",
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()
            print(response)

            if isinstance(response, list):
                MarksObject = JsonToClassConverter.convert("MarksObject", {"payload": response})
            else:
                MarksObject = JsonToClassConverter.convert("MarksObject", response)

            MarksObject.json = response

            return MarksObject
        

    async def getAcademicYears(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/ej/core/family/v1/academic_years",
                headers={
                    "Authorization": f"Bearer {self.student.token}",
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/ej/core/family/v1/academic_years",
                    headers={
                        "Authorization": f"Bearer {self.student.token}",
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()
            print(response)

            if isinstance(response, list):
                ScheduleObject = JsonToClassConverter.convert("ScheduleObject", {"payload": response})
            else:
                ScheduleObject = JsonToClassConverter.convert("ScheduleObject", response)

            ScheduleObject.json = response

            return ScheduleObject