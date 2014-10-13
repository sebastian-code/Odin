from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from courses.models import Course, Partner
from helpers import division_or_zero
from students.models import CourseAssignment, StudentStartedWorkingAt


@staff_member_required
def dashboard(request):
    companies = Partner.objects.filter(is_active=False).order_by('name')
    courses = Course.objects.all()
    partners = Partner.objects.filter(is_active=True).order_by('name')
    return render(request, 'dashboard.html', locals())


@staff_member_required
def show_partners_stats(request):
    partners = Partner.objects.filter(is_active=True).order_by('name')
    total_money_spent = 0
    total_started_working_ats = 0
    average_cost_per_recruitment = 0
    for partner in partners:
        partner_started_working_ats = StudentStartedWorkingAt.objects.filter(partner=partner).count()
        partner_cost_per_recruitment = division_or_zero(partner.money_spent, partner_started_working_ats)
        average_cost_per_recruitment += partner_cost_per_recruitment
        total_started_working_ats += partner_started_working_ats
        total_money_spent += partner.money_spent
    average_cost_per_recruitment = division_or_zero(average_cost_per_recruitment, partners.count())
    total_assignments = CourseAssignment.objects.filter(course__partner__in=partners).count()
    total_hired_percent = division_or_zero(total_started_working_ats, total_assignments) * 100
    return render(request, 'show_partners_stats.html', locals())


@staff_member_required
def show_partner_stats(request, partner_id):
    partner = get_object_or_404(Partner, pk=partner_id)
    total_assignments = CourseAssignment.objects.filter(course__partner=partner).count()
    started_working_ats = StudentStartedWorkingAt.objects.filter(partner=partner).select_related('assignment')
    started_working_ats_count = started_working_ats.count()
    cost_per_recruitment = division_or_zero(partner.money_spent, started_working_ats_count)
    hired_percent = division_or_zero(started_working_ats_count, total_assignments) * 100
    return render(request, 'show_partner_company_stats.html', locals())


@staff_member_required
def show_companies_stats(request):
    companies = Partner.objects.filter(is_active=False).order_by('name')
    total_money_spent = 0
    average_cost_per_recruitment = 0
    total_started_working_ats = 0
    for company in companies:
        company_started_working_ats = StudentStartedWorkingAt.objects.filter(partner=company).count()
        company_cost_per_recruitment = division_or_zero(company.money_spent, company_started_working_ats)
        average_cost_per_recruitment += company_cost_per_recruitment
        total_started_working_ats += company_started_working_ats
        total_money_spent += company.money_spent
    average_cost_per_recruitment = division_or_zero(average_cost_per_recruitment, companies.count())
    total_assignments = CourseAssignment.objects.filter(course__partner__in=companies).count()
    total_hired_percent = division_or_zero(total_started_working_ats, total_assignments) * 100
    return render(request, 'show_companies_stats.html', locals())


@staff_member_required
def show_assignments_stats(request):
    DEFAULT_AVATAR_URL = settings.STATIC_URL + settings.NO_AVATAR_IMG
    assignments_without_profile_picture = CourseAssignment.objects.filter(Q(user__avatar=DEFAULT_AVATAR_URL) |
                                                                          Q(user__avatar=None))
    assignments_without_mac = CourseAssignment.objects.filter(user__mac=None)

    total_assignments = CourseAssignment.objects.all().count()
    total_without_mac_address = assignments_without_mac.count()
    total_without_profile_picture = assignments_without_profile_picture.count()

    total_with_mac_address = total_assignments - total_without_mac_address
    total_with_profile_picture = total_assignments - total_without_profile_picture

    return render(request, 'show_assignment_stats.html', locals())


@staff_member_required
def show_courses_stats(request):
    courses = Course.objects.filter(is_free=True)
    partners = set()
    for course in courses:
        for partner in course.partner.all():
            partners.add(partner)

    total_courses_funds = 0
    average_cost_per_recruitment = 0

    for partner in partners:
        partner_started_working_ats = StudentStartedWorkingAt.objects.filter(partner=partner).count()
        partner_cost_per_recruitment = division_or_zero(partner.money_spent, partner_started_working_ats)
        average_cost_per_recruitment += partner_cost_per_recruitment
        total_courses_funds += partner.money_spent

    average_cost_per_recruitment = division_or_zero(average_cost_per_recruitment, len(partners))
    total_assignments = CourseAssignment.objects.filter(course__in=courses).count()
    total_started_working_ats = StudentStartedWorkingAt.objects.all()
    total_started_working_ats_count = total_started_working_ats.count()
    hired_percent = division_or_zero(total_started_working_ats_count, total_assignments) * 100
    return render(request, 'show_courses_stats.html', locals())


@staff_member_required
def show_course_stats(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    partners = course.partner.all()
    total_course_funds = 0
    average_cost_per_recruitment = 0
    for partner in partners:
        partner_started_working_ats = StudentStartedWorkingAt.objects.filter(partner=partner).count()
        partner_cost_per_recruitment = division_or_zero(partner.money_spent, partner_started_working_ats)
        average_cost_per_recruitment += partner_cost_per_recruitment
        partner_course_funds = division_or_zero(partner.money_spent, Course.objects.filter(partner=partner).count())
        total_course_funds += partner_course_funds
    total_assignments = CourseAssignment.objects.filter(course=course)
    started_working_ats = StudentStartedWorkingAt.objects.filter(assignment__in=total_assignments).select_related('assignment')
    started_working_ats_count = started_working_ats.count()
    average_cost_per_recruitment = division_or_zero(average_cost_per_recruitment, partners.count())
    hired_percent = division_or_zero(started_working_ats_count, total_assignments.count()) * 100
    return render(request, 'show_course_stats.html', locals())
