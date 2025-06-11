import aiohttp # type: ignore
import asyncio
import json
from utils.classCreater import JsonToClassConverter
from errors.errors import TokenError, DnevnikError
from student.student import Student
from typing import Union


class Schedule:
    def __init__(self, student: Student) -> None:
        self.student = student
        
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


    async def getScheduleByDates(self, begin_date: str, end_date: str):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/eventcalendar/v1/api/events?person_ids={self.student.person_id}&begin_date={begin_date}&end_date={end_date}",
                headers={
                    "Authorization": f"Bearer {self.student.token}",
                    "X-Mes-Subsystem": "familyweb",
                    "X-Mes-Role": "student"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/eventcalendar/v1/api/events?person_ids={self.student.person_id}&begin_date={begin_date}&end_date={end_date}",
                    headers={
                        "Authorization": f"Bearer {self.student.token}",
                        "X-Mes-Subsystem": "familyweb",
                        "X-Mes-Role": "student"
                    }
                )

            response = await response.json()

            ScheduleDays = JsonToClassConverter.convert("ScheduleDays", response)
            ScheduleDays.json = response

            return ScheduleDays
        

    async def getSchedulePeriods(self, nowPeriod: int = 13):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/ej/core/family/v1/periods_schedules?academic_year_id={nowPeriod}&student_profile_id={self.student.id}",
                headers={
                    "Authorization": f"Bearer {self.student.token}",
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/ej/core/family/v1/periods_schedules?academic_year_id={nowPeriod}&student_profile_id={self.student.id}",
                    headers={
                        "Authorization": f"Bearer {self.student.token}",
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            if isinstance(response, list):
                SchedulePeriods = JsonToClassConverter.convert("SchedulePeriods", {"payload": response})
            else:
                SchedulePeriods = JsonToClassConverter.convert("SchedulePeriods", response)

            SchedulePeriods.json = response

            return SchedulePeriods
        

    async def getControlTestDays(self, from_day: str, to_day: str):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/ej/plan/family/v1/test_lessons/period?student_profile_id={self.student.profiles[0]['id']}&from={from_day}&to={to_day}&student_person_id={self.student.person_id}",
                headers={
                    "Authorization": f"Bearer {self.student.token}",
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/ej/plan/family/v1/test_lessons/period?student_profile_id={self.student.profiles[0]['id']}&from={from_day}&to={to_day}&student_person_id={self.student.person_id}",
                    headers={
                        "Authorization": f"Bearer {self.student.token}",
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            if isinstance(response, list):
                SchedulePeriods = JsonToClassConverter.convert("SchedulePeriods", {"payload": response})
            else:
                SchedulePeriods = JsonToClassConverter.convert("SchedulePeriods", response)
                
            SchedulePeriods.json = response

            return SchedulePeriods
        