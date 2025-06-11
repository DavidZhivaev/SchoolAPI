import aiohttp # type: ignore
import asyncio
import json
from typing import Union
from utils.classCreater import JsonToClassConverter
from errors.errors import TokenError, DnevnikError
from student.student import Student

class Homeworks:
    def __init__(self, student: Student):
        self.student = student

    async def getHomeworkByDate(self, from_date: str, to_date: str):
        async with aiohttp.ClientSession() as session:
            profile = await self.student.getStudentProfiles()
            response = await session.get(
                f"https://school.mos.ru/api/family/web/v1/homeworks?from={from_date}&to={to_date}&student_id={profile.id}",
                headers={
                    "Auth-Token": self.student.token,
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/family/web/v1/homeworks?from={from_date}&to={to_date}&student_id={profile.id}",
                    headers={
                        "Auth-Token": self.student.token,
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            HomeworkObject = JsonToClassConverter.convert("HomeworkObject", response)
            HomeworkObject.json = response

            return HomeworkObject
        
    
    async def additionalMaterials(self, uuid: Union[list[str], str], homework_entry_student_id: int):
        payload = {
            "materials": []
        }

        if isinstance(uuid, list):
            for id in uuid:
                payload["materials"].append({
                    "uuid": id,
                    "purpose": "for_home",
                    "selected_mode": "execute",
                    "homework_entry_student_id": homework_entry_student_id
                })
        elif isinstance(uuid, str):
            payload["materials"].append({
                "uuid": uuid,
                "purpose": "for_home",
                "selected_mode": "execute",
                "homework_entry_student_id": homework_entry_student_id
            })

        print(payload)

        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://school.mos.ru/api/family/materials/v1/additional_materials",
                headers={
                    "Auth-Token": self.student.token,
                    "X-Mes-Subsystem": "familyweb"
                }, json=payload
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.post(
                    f"https://school.mos.ru/api/family/materials/v1/additional_materials",
                    headers={
                        'Content-Type': 'application/json;charset=UTF-8',
                        "Auth-Token": self.student.token,
                        "X-Mes-Subsystem": "familyweb"
                    }, json=payload
                )

            response = await response.json()

            MaterialsObject = JsonToClassConverter.convert("MaterialsObject", response)
            MaterialsObject.json = response

            return MaterialsObject
        
    
    async def getShortHomeworkByDates(self, dates: Union[list[str], str]):
        if dates is str:
            dates = dates
        elif dates is list:
            dates = '%2'.join(dates)

        async with aiohttp.ClientSession() as session:
            profile = await self.student.getStudentProfiles()
            response = await session.get(
                f"https://school.mos.ru/api/family/web/v1/schedule/short?student_id={profile.id}&dates={dates}",
                headers={
                    "Auth-Token": self.student.token,
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/family/web/v1/schedule/short?student_id={profile.id}&dates={'%2'.join(dates)}",
                    headers={
                        "Auth-Token": self.student.token,
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            HomeworkObject = JsonToClassConverter.convert("HomeworkObject", response)
            HomeworkObject.json = response

            return HomeworkObject