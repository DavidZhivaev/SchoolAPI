import asyncio
from student.student import Student
from utils.utils import *
from schedule.schedule import Schedule
from marks.marks import Marks
from homeworks.homeworks import Homeworks
from notification.notification import Notification
from school.school import School
from materials.materials import Materials


async def test():
    token = "eyJhbGciOiJIUzI1..."
    student = Student(token)

    day1 = Utils.getNormalDate(2024, 2, 4)
    day2 = Utils.getNormalDate(2025, 6, 1)
    
if __name__ == '__main__':
    asyncio.run(test())
