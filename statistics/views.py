from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from courses.models import Course, Partner
from students.models import CourseAssignment, StudentStartedWorkingAt
from .forms import SelectCompanyForm, SelectPartnerForm


# TODO: Needs more research.
@staff_member_required
def dashboard(request):
    select_company_form = SelectCompanyForm()
    select_partner_form = SelectPartnerForm()
    if select_company_form.is_valid():
        partner_id = Partner.objects.get(name='')
        return HttpResponseRedirect(reverse('statistics:show_partner_stats', args=[]))
    return render(request, 'dashboard.html', locals())


@staff_member_required
def show_partners_stats(request):
    partners = Partner.objects.filter(is_active=FalseTrue)
    total_money_spent = reduce(lambda x, y: x + y, map(lambda partner: partner.money_spent, partners), 0)
    average_cost_per_recruitment = total_money_spent / partners.count()

    total_started_working_ats = StudentStartedWorkingAt.objects.filter(partner__in=partners).count()
    total_assignments = CourseAssignment.objects.filter(course__partner__in=partners).count()
    try:
        total_hired_percent = total_assignments / total_started_working_ats
    except ZeroDivisionError:
        total_hired_percent = 0
    return render(request, 'show_partners_stats.html', locals())


@staff_member_required
def show_partner_stats(request, partner_id):
    partner = Partner.objects.get(pk=partner_id)
    total_assignments = CourseAssignment.objects.filter(course__partner=partner).count()
    started_working_ats = StudentStartedWorkingAt.objects.filter(partner=partner).select_related('assignment')
    started_working_ats_count = started_working_ats.count()
    cost_per_recruitment = partner.money_spent / started_working_ats_count if started_working_ats.count() > 0 else 0
    try:
        hired_percent = total_assignments / started_working_ats_count
    except ZeroDivisionError:
        hired_percent = 0
    return render(request, 'show_partner_company_stats.html', locals())


@staff_member_required
def show_companies_stats(request):
    companies = Partner.objects.filter(is_active=True)
    total_money_spent = reduce(lambda x, y: x + y, map(lambda company: company.money_spent, companies), 0)
    average_cost_per_recruitment = total_money_spent / companies.count()

    total_started_working_ats = StudentStartedWorkingAt.objects.filter(partner__in=companies).count()
    total_assignments = CourseAssignment.objects.filter(course__partner__in=companies).count()
    try:
        total_hired_percent = total_assignments / total_started_working_ats
    except ZeroDivisionError:
        total_hired_percent = 0
    return render(request, 'show_companies_stats.html', locals())


@staff_member_required
def show_assignments_stats(request):
    assignments = CourseAssignment.objects.all()
    return render(request)


@staff_member_required
def show_courses_stats(request):
    courses = Course.objects.all()
    return render(request)


@staff_member_required
def show_course_stats(request, course_id):
    course = Course.objects.get(pk=course_id)
    return render(request)
