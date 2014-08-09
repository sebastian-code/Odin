from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from courses.models import Course, Task

import re
from github import Github


def get_api_repo(github_parameters):
    github_client = Github(settings.GITHUB_OATH_TOKEN)
    return github_client.get_user(github_parameters['user']).get_repo(github_parameters['repo_name'])


def get_user_and_repo_names(github_url):
    # Ex: https://github.com/syndbg/HackBulgaria/tree/master/Core-Java-1
    # Becomes  [u'https:', u'', u'github.com', u'syndbg', u'HackBulgaria', u'tree', u'master', u'Core-Java-1']
    # Only 4th and 5th elements are relevant
    github_url_split = github_url.split('/')[3:]
    return {'user': github_url_split[0], 'repo_name': github_url_split[1]} if len(github_url_split) >= 2 else {'user': github_url_split[0]}


def is_weekly_task(tree_element):
    regex = re.compile(r'^week\d+')
    # paths as week1/2-jQuery-Gauntlet/<N>/README.md won't be counted as single tasks
    # instead there'll be only one week1/2-jQuery-Gauntlet/README.md task
    return regex.match(tree_element.path) != None and tree_element.path.count('/') < 3


def is_exam_task(tree_element):
    regex = re.compile(r'^exams/exam\d+')
    # paths as <exams/exam2/README.md> won't be counted as tasks
    return regex.match(tree_element.path) != None and tree_element.path.count('/') > 2


def get_dir_and_task_names(path):
    regex = re.compile(r'(week\d|exam\d)(/.+?/)')
    result = regex.search(path).groups()
    return {'dir': result[0], 'raw_task': result[1]}


def get_deadline():
    deadline = timezone.now()
    # deadline is always 7 days from today
    return deadline.replace(day=deadline.day + 7, hour=23, minute=56, second=56)


def get_formatted_task_url(raw_task_url, dir_task_names, is_exam):
    raw_task_url = raw_task_url if raw_task_url[-1] != '/' else raw_task_url[:-1]
    dir_name = 'exams/{}'.format(dir_task_names['dir']) if is_exam else dir_task_names['dir']
    return '{}/tree/master/{}{}'.format(raw_task_url, dir_name, dir_task_names['raw_task'])


def get_formatted_task_name(raw_task_name):
    raw_task_name = raw_task_name[1:-1].replace('-', ' ').split(' ')
    output = '<{}>'.format(raw_task_name[0])
    for i in range(1, len(raw_task_name)):
        output += ' {}'.format(raw_task_name[i])
    return output


def create_db_task(course, tree_element, is_exam):
    dir_task_names = get_dir_and_task_names(tree_element.path)
    task_github_url = get_formatted_task_url(course.git_repository, dir_task_names, is_exam)
    task_name = get_formatted_task_name(dir_task_names['raw_task'])
    deadline = get_deadline()

    obj, created = Task.objects.get_or_create(name=task_name, description=task_github_url, course=course, is_exam=is_exam, week=dir_task_names['dir'], defaults={'deadline': deadline})
    if created:
        print 'Created task {} - {}'.format(task_name, task_github_url)


class Command(BaseCommand):
    args = '<course_id>'
    help = '''
        Generates tasks from <course_id>'s github repository.
    '''

    def handle(self, *args, **options):
        arg_course_id = args[0]
        course = Course.objects.get(id=arg_course_id)
        course_github_url = course.git_repository
        if '://github.com/' in course_github_url:
            github_parameters = get_user_and_repo_names(course_github_url)
            api_repo = get_api_repo(github_parameters)
            api_repo_tree = api_repo.get_git_tree(sha='master', recursive=True)
            # filters tree elements by depth of 2, when base is considered 0
            blob_tree_elements = filter(
                lambda x: 'README.md' in x.path and x.path.count('/') > 1 and x.type == 'blob', api_repo_tree.tree)
            for element in blob_tree_elements:
                if is_exam_task(element):
                    create_db_task(course, element, is_exam=True)
                elif is_weekly_task(element):
                    create_db_task(course, element, is_exam=False)
        else:
            print 'No github repo set for course <{}>'.format(course.name)
