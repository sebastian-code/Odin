import os
import datetime

from django.core.management import call_command
from django.test import TestCase

from .models import User, CourseAssignment
from courses.models import Course


class GetCommandsTest(TestCase):
    def setUp(self):
        self.filename = 'students.txt'
        self.user_without_github = User.objects.create_user('asd@gmail.com', '123')
        self.user_without_github.first_name = 'Asd'
        self.user_without_github.save()

        self.user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.user.first_name = 'Ivo'
        self.user.status = User.STUDENT
        self.user.github_account = 'https://github.com/Ivaylo-Bachvarov'
        self.user.save()

    def tearDown(self):
        os.remove(self.filename)

    def test_get_people_with_no_github(self):
        expected = '[1] {} - {}\n'.format(self.user_without_github.first_name, self.user_without_github.email)
        call_command('get_people_with_no_github', self.filename)
        with open(self.filename, 'r') as f:
            actual = f.read()
        self.assertEqual(expected, actual)

    def test_get_github_accounts(self):
        expected = '{} - {} - {}\n'.format(self.user.first_name, self.user.email, self.user.github_account)
        call_command('get_github_accounts', self.filename)
        with open(self.filename, 'r') as f:
            actual = f.read()
        self.assertEqual(expected, actual)

# 
# class PeopleImportTest(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         cls.course = Course.objects.create(
#             name='Test Course',
#             url='test-course',
#             application_until=datetime.datetime.now(),
#         )
#         cls.filename = 'students.csv'
#         csv_file = open(cls.filename, "w")
#         csv_file.write('ivo@abv.bg, Ivayo Ivov, 1, {}, ,'.format(cls.course.id))
#         csv_file.close()
#
#     @classmethod
#     def tearDownClass(cls):
#         os.remove(cls.filename)
#
#     def test_import_users_from_csv(self):
#         call_command('import_users_from_csv', self.filename)
#         new_users = User.objects.filter(email='ivo@abv.bg')
#         self.assertEqual(new_users.count(), 1)
#
#     def test_import_users_from_csv_course_assignment(self):
#         call_command('import_users_from_csv', self.filename)
#         new_user = User.objects.filter(email='ivo@abv.bg').count()
#         course_assignments = CourseAssignment.objects.filter(user=new_user)
#         self.assertEqual(course_assignments.count(), 1)
#
#     # def test_import_existing_user(self):
#     #     existing_student = User.objects.create_user('ivo@abv.bg', '123')
#     #     existing_course = Course.objects.create(
#     #         name='Old Course',
#     #         url='old-course',
#     #         application_until=datetime.datetime.now(),
#     #     )
#     #
#     #     self.assignment = CourseAssignment.objects.create(
#     #         user=existing_student,
#     #         course=existing_course,
#     #         group_time=CourseAssignment.EARLY
#     #     )
#     #
#     #     call_command('import_users_from_csv', self.filename)
#     #     new_user = User.objects.filter(email='ivo@abv.bg').count()
#     #     course_assignments = CourseAssignment.objects.filter(user=new_user)
#     #
#     #     self.assertEqual(course_assignments.count(), 2)
