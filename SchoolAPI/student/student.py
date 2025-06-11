import aiohttp # type: ignore
import asyncio
import json
from utils.classCreater import JsonToClassConverter
from errors.errors import TokenError, DnevnikError, LibError

class Student:
    def __init__(self, token: str) -> None:
        self.token = token
        self.isActivate = False
        self.session = None

    def __str__(self):
        if self.isActivate:
            return f"Student Object: {self.session.last_name} {self.session.first_name} {self.session.middle_name} [{self.session.id}]\nID: {self.session.person_id}\nDate of birth: {self.session.date_of_birth}"
        else:
            return f"Student Object: not activate!"


    def __getattribute__(self, name):
        allowed_attrs = ["__str__", 'token', 'isActivate', "activate", "getSession", "getPassport", "getPerson", "getStudentProfiles", "getUserInfo", "refresh", "session"]
        if name not in allowed_attrs and not super().__getattribute__('isActivate'):
            raise LibError("The object is not activated! Call `await Student.activate()` before use.")
        return super().__getattribute__(name)


    async def getSession(self):
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                'https://school.mos.ru/api/ej/acl/v1/sessions',
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Authorization": f"Bearer {self.token}",
                    "X-Mes-Subsystem": "familyweb"
                }, json={"auth_token": self.token}
            )

            if response.status != 200:
                self.token = await self.refresh()
                response = await session.post(
                    'https://school.mos.ru/api/ej/acl/v1/sessions',
                    headers={
                        "Accept": "application/json, text/plain, */*",
                        "Authorization": f"Bearer {self.token}",
                        "X-Mes-Subsystem": "familyweb"
                    }, json={"auth_token": self.token}
                )

                if response.status != 200:
                    raise TokenError(self.token)

            response = await response.json()
            for key, value in response.items():
                if key not in ["authentication_token"]:
                    setattr(self, key, value)

            Session = JsonToClassConverter.convert("Session", response)
            Session.json = response

            self.session = Session
            self.sessionJson = response
            self.isActivate = True
            return Session
        
    
    async def activate(self):
        if self.isActivate is False:
            await self.getSession()
            self.isActivate = True
            return self
        else:
            raise LibError("The object has already been activated, you can use it!")


    async def getPassport(self):
        if self.session is None:
            await self.getSession()
            self.isActivate = True

        async with aiohttp.ClientSession() as session:
            response = await session.get(
                'https://school.mos.ru/api/passport/agents/v1/utils/person',
                headers = {
                    "Authorization": f"Bearer {self.token}",
                    "X-Mes-Subsystem": "passportweb"
                }
            )

            if response.status != 200:
                raise DnevnikError(f"Code: {response.status}\nResponse: {response.text}")

            response = await response.json()

            Passport = JsonToClassConverter.convert("Passport", response)
            Passport.json = response

            self.passport = Passport
            self.passportJson = response
            return Passport
        

    async def getPerson(self):
        if self.session is None:
            await self.getSession()
            self.isActivate = True

        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f'https://school.mos.ru/api/persondata/v1/persons/{self.person_id}',
                headers = {
                    "Authorization": f"Bearer {self.token}",
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                raise DnevnikError(f"Code: {response.status}\nResponse: {response.text}")

            response = await response.json()

            Person = JsonToClassConverter.convert("Person", response)
            Person.json = response

            self.person = Person
            self.personJson = response
            return Person
        

    async def getUserInfo(self):
        if self.session is None:
            await self.getSession()
            self.isActivate = True

        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f'https://school.mos.ru/v3/userinfo',
                headers = {
                    "Authorization": f"Bearer {self.token}"
                }
            )

            if response.status != 200:
                raise DnevnikError(f"Code: {response.status}\nResponse: {response.text}")

            response = await response.json()

            UserInfo = JsonToClassConverter.convert("UserInfo", response)
            UserInfo.json = response

            self.userinfo = UserInfo
            self.userInfoJson = response
            return UserInfo
        

    async def getStudentProfiles(self):
        if self.session is None:
            await self.getSession()
            self.isActivate = True

        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f'https://dnevnik.mos.ru/core/api/student_profiles/',
                headers = {
                    "Authorization": f"Bearer {self.token}"
                }
            )

            if response.status != 200:
                raise DnevnikError(f"Code: {response.status}\nResponse: {response.text}")

            response = (await response.json())[0]

            studentProfile = JsonToClassConverter.convert("studentProfile", response)
            studentProfile.json = response

            self.studentProfile = studentProfile
            self.studentProfileJson = response
            return studentProfile
        

    async def getSferumAccount(self):
        if self.session is None:
            await self.getSession()
            self.isActivate = True

        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f'https://school.mos.ru/v2/external-partners/check-for-vk-user?person_id={self.person_id}&staff_id=',
                headers = {
                    "Authorization": f"Bearer {self.token}",
                    "X-Mes-Subsystem": "familyweb"
                }
            )

            if response.status != 200:
                raise DnevnikError(f"Code: {response.status}\nResponse: {response.text}")

            response = await response.json()

            studentVk = JsonToClassConverter.convert("studentVk", response)
            studentVk.json = response

            self.studentVk = studentVk
            self.studentVkJson = response
            return studentVk
        

    async def refresh(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                'https://school.mos.ru/v2/token/refresh?roleId=1&subsystem=2',
                headers={
                    'Authorization': f'Bearer {self.token}',
                    'Accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'X-Mes-Subsystem': 'familyweb',
                }
            )

            if response.status != 201:
                raise TokenError(self.token)

            response = await response.text()
            self.token = response
            self.session = None
            await self.getSession()

            self.isActivate = True

            return response