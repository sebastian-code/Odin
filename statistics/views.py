from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from courses.models import Course, Partner
from helpers import division_or_zero
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
    partners = Partner.objects.filter(is_active=True)
    total_money_spent = 0
    average_cost_per_recruitment = 0
    total_started_working_ats = 0
    for partner in partners:
        partner_started_working_ats = StudentStartedWorkingAt.objects.filter(partner=partner).count()
        partner_cost_per_recruitment = division_or_zero(partner.money_spent, partner_started_working_ats)
        average_cost_per_recruitment += partner_cost_per_recruitment
        total_started_working_ats += partner_started_working_ats
        total_money_spent += partner.money_spent
        total_assignments = CourseAssignment.objects.filter(course__partner__in=partners).count()
    total_hired_percent = division_or_zero(total_started_working_ats, total_assignments) * 100
    return render(request, 'show_partners_stats.html', locals())


@staff_member_required
def show_partner_stats(request, partner_id):
    partner = Partner.objects.get(pk=partner_id)
    total_assignments = CourseAssignment.objects.filter(course__partner=partner).count()
    started_working_ats = StudentStartedWorkingAt.objects.filter(partner=partner).select_related('assignment')
    started_working_ats_count = started_working_ats.count()
    cost_per_recruitment = division_or_zero(partner.money_spent, started_working_ats_count)
    hired_percent = division_or_zero(started_working_ats_count, total_assignments) * 100
    return render(request, 'show_partner_company_stats.html', locals())


@staff_member_required
def show_companies_stats(request):
    companies = Partner.objects.filter(is_active=False)
    total_money_spent = 0
    average_cost_per_recruitment = 0
    total_started_working_ats = 0
    for company in companies:
        company_started_working_ats = StudentStartedWorkingAt.objects.filter(partner=company).count()
        company_cost_per_recruitment = division_or_zero(company.money_spent, company_started_working_ats)
        average_cost_per_recruitment += company_cost_per_recruitment
        total_started_working_ats += company_started_working_ats
        total_money_spent += company.money_spent
    total_assignments = CourseAssignment.objects.filter(course__partner__in=companies).count()
    total_hired_percent = division_or_zero(total_started_working_ats, total_assignments) * 100
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
    partners = course.partner.all()
    total_course_funds = 0
    for partner in partners:
        partner_course_funds = partner.money_spent / Course.objects.filter(partner=partner).count()
        total_course_funds += partner_course_funds
    total_assignments = CourseAssignment.objects.filter(course=course)
    started_working_ats = StudentStartedWorkingAt.objects.filter(assignment__in=total_assignments).select_related('assignment')
    started_working_ats_count = started_working_ats.count()
    hired_percent = division_or_zero(started_working_ats_count, total_assignments.count()) * 100
    return render(request, 'show_course_stats.html', locals())
