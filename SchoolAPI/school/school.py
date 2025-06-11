import aiohttp # type: ignore
import asyncio
import json
from utils.classCreater import JsonToClassConverter
from errors.errors import TokenError, DnevnikError
from student.student import Student

class School:
    def __init__(self, student: Student) -> None:
        self.student = student

    async def getSchoolInfo(self):
        async with aiohttp.ClientSession() as session:
            profile = await self.student.getStudentProfiles()
            response = await session.get(
                f"https://school.mos.ru/api/family/web/v1/school_info?class_unit_id={profile.class_unit.id}&school_id={profile.school_id}&student_id={profile.id}",
                headers={
                    "Authorization": f"Bearer {self.student.token}",
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/family/web/v1/school_info?class_unit_id={profile.class_unit.id}&school_id={profile.school_id}&student_id={profile.id}",
                    headers={
                        "Authorization": f"Bearer {self.student.token}",
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            SchoolObject = JsonToClassConverter.convert("SchoolObject", response)
            SchoolObject.json = response

            return SchoolObject
      

    async def getSubjects(self):
        async with aiohttp.ClientSession() as session:
            profile = await self.student.getStudentProfiles()
            response = await session.get(
                f"https://school.mos.ru/api/family/web/v1/programs/parallel_curriculum/{profile.curricula.id}?student_id={profile.id}",
                headers={
                    "Authorization": f"Bearer {self.student.token}",
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/family/web/v1/programs/parallel_curriculum/{profile.curricula.id}?student_id={profile.id}",
                    headers={
                        "Authorization": f"Bearer {self.student.token}",
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            SchoolObject = JsonToClassConverter.convert("SchoolObject", response)
            SchoolObject.json = response

            return SchoolObject
      

    async def getMoscowSchools(self):
        async with aiohttp.ClientSession() as session:
            profile = await self.student.getStudentProfiles()
            response = await session.get(
                f"https://school.mos.ru/api/nsi/dictionaries/v1/family_moscow_organizations",
                headers={
                    "Authorization": f"Bearer {self.student.token}",
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                await self.student.refresh()
                
                response = await session.get(
                    f"https://school.mos.ru/api/nsi/dictionaries/v1/family_moscow_organizations",
                    headers={
                        "Authorization": f"Bearer {self.student.token}",
                        "X-Mes-Subsystem": "familyweb"
                    }
                )

            response = await response.json()

            if isinstance(response, list):
                SchoolObject = JsonToClassConverter.convert("SchoolObject", {"payload": response})
            else:
                SchoolObject = JsonToClassConverter.convert("SchoolObject", response)
            SchoolObject.json = response

            return SchoolObject
      