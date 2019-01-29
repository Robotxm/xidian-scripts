# Copyright (C) 2019 by the XiDian Open Source Community.
#
# This file is part of xidian-scripts.
#
# xidian-scripts is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# xidian-scripts is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with xidian-scripts.  If not, see <http://www.gnu.org/licenses/>.

from icalendar import Calendar, Event
from datetime import datetime
import auth.ids
import credentials


TIMETABLE_URL = "https://xidian.cpdaily.com/comapp-timetable/sys/schoolTimetable/v2/api/weekTimetable"

START_YEAR = 2018  # Time when a school year starts
END_YEAR = 2019  # Time when a school year ends
END_MONTH = 5  # Month when timetable is changed in summer
END_DAY = 2 # Day when timetable is changed in summer

if __name__ == '__main__':
    # Time A(summer)
    section_start_time_a = ["08:00", "08:30", "09:20", "10:25", "11:15",  # morning
                            "14:30", "15:20", "16:25", "17:15",  # afternoon
                            "19:30", "20:20"]  # evening
    section_end_time_a = ["08:30", "09:15", "10:05", "11:10", "12:00",
                          "15:15", "16:05", "17:10", "18:00",
                          "20:15", "21:05"]

    # Time B(spring, autumn and winter)
    section_start_time_b = ["08:00", "08:30", "09:20", "10:25", "11:15",
                            "14:00", "14:50", "15:55", "16:45",
                            "19:00", "19:50"]
    section_end_time_b = ["08:30", "09:15", "10:05", "11:10", "12:00",
                          "14:45", "15:35", "16:40", "17:30",
                          "19:45", "20:35"]
    ses = auth.ids.get_login_session(
        'https://xidian.cpdaily.com/comapp-timetable/sys/schoolTimetable/v2/api/weekTimetable', credentials.IDS_USERNAME, credentials.IDS_PASSWORD)
    ses.get(TIMETABLE_URL)
    result = ses.get(TIMETABLE_URL).json()
    if result["code"] != '0':
        print(result['message'])
    else:
        allteachweeks = result["allTeachWeeks"]
        cal = Calendar()
        for current_week in range(allteachweeks):
            for current_day in range(7):
                if len(result["termWeeksCourse"][current_week]["courses"][current_day]["sectionCourses"]) != 0:
                    for current_course in range(len(result["termWeeksCourse"][current_week]["courses"][current_day]["sectionCourses"])):
                        course_day = result["termWeeksCourse"][current_week]["courses"][current_day]["date"]
                        course_name = result["termWeeksCourse"][current_week]["courses"][current_day]["sectionCourses"][current_course]["courseName"]
                        course_classroom = result["termWeeksCourse"][current_week]["courses"][current_day]["sectionCourses"][current_course]["classroom"]
                        course_start_number = result["termWeeksCourse"][current_week]["courses"][current_day]["sectionCourses"][current_course]["sectionStart"]
                        course_end_number = result["termWeeksCourse"][current_week]["courses"][current_day]["sectionCourses"][current_course]["sectionEnd"]
                        event = Event()
                        day_1 = datetime.strptime(course_day, "%Y-%m-%d")
                        day_2 = datetime(START_YEAR, 10, 8)
                        day_3 = datetime(END_YEAR, END_MONTH, END_DAY)
                        event.add('description', course_name + " @ " + course_classroom)
                        event.add('summary', course_name + " @ " + course_classroom)
                        if day_2 < day_1 < day_3:
                            event.add('dtstart', datetime.strptime(
                                course_day + " " + section_start_time_b[int(course_start_number)], "%Y-%m-%d %H:%M"))
                            event.add('dtend', datetime.strptime(
                                course_day + " " + section_end_time_b[int(course_end_number)], "%Y-%m-%d %H:%M"))
                        else:
                            event.add('dtstart', datetime.strptime(
                                course_day + " " + section_start_time_a[int(course_start_number)], "%Y-%m-%d %H:%M"))
                            event.add('dtend', datetime.strptime(
                                course_day + " " + section_end_time_a[int(course_end_number)], "%Y-%m-%d %H:%M"))
                        cal.add_component(event)
        f = open(credentials.IDS_USERNAME + '_' + result["yearTerm"] + ".ics", 'wb')
        f.write(cal.to_ical())
        f.close()
        print("iCalendar (.ics) file has been save to " + credentials.IDS_USERNAME + '_' + result["yearTerm"] + ".ics")
