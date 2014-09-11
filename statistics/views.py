from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from courses.models import Partner
from students.models import CourseAssignment


@staff_member_required
def show_all_stats(request):
    pass


@staff_member_required
def show_partners_stats(request):
    return render(request, 'show_stats.html', locals())


@staff_member_required
def show_partner_stats(request, partner_id):
    partner = Partner.objects.get(pk=partner_id)
    print partner
    course_assignments = CourseAssignment.objects.filter(course__partner=partner)
    print course_assignments
    return render(request, 'show_partner_company_stats', locals())


@staff_member_required
def show_companies_stats(request):
    return render(request, 'show_stats.html', locals())


@staff_member_required
def show_assignments_stats(request):
    assignments = CourseAssignment.objects.all()
    return render(request);


@staff_member_required
def show_courses_stats(request):
    pass


@staff_member_required
def show_course_stats(request, course_id):
    pass
