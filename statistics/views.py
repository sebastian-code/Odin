from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from courses.models import Partner
from students.models import CourseAssignment, StudentStartedWorkingAt


@staff_member_required
def show_all_stats(request):
    pass


@staff_member_required
def show_partners_stats(request):
    return render(request, 'show_stats.html', locals())


@staff_member_required
def show_partner_stats(request, partner_id):
    partner = Partner.objects.get(pk=partner_id)
    total_assignments = CourseAssignment.objects.filter(course__partner=partner).count()
    assignments = StudentStartedWorkingAt.objects.filter(partner=partner)
    cost_per_recruitment = partner.money_spent / assignments.count() if assignments.count() > 0 else 0
    return render(request, 'show_partner_company_stats.html', locals())


@staff_member_required
def show_companies_stats(request):
    return render(request, 'show_stats.html', locals())


@staff_member_required
def show_assignments_stats(request):
    assignments = CourseAssignment.objects.all()
    return render(request)


@staff_member_required
def show_courses_stats(request):
    pass


@staff_member_required
def show_course_stats(request, course_id):
    pass
