import aiohttp # type: ignore
import asyncio
import json
from utils.classCreater import JsonToClassConverter
from errors.errors import TokenError, DnevnikError, LibError
from student.student import Student
from typing import Union


class Challenge:
    def __init__(self, student: Student = None) -> None:
        self.student = student

    async def getChallengeUuid(self, link):
        pass