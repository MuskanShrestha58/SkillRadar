from .models import Institute, Course, UserProfile, Review, Student
from django.db import models
from .forms import ReviewForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePage(TemplateView):
    template_name = 'mainapp/base.html'


class InstituteListView(ListView):
    model = Institute
    template_name = 'mainapp/institute_list.html'
    context_object_name = 'institutes'


class InstituteDetailView(DetailView):
    model = Institute
    template_name = 'mainapp/institute_detail.html'
    context_object_name = 'institute'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(institute=self.object)
        return context


class CourseListView(ListView):
    model = Course
    template_name = 'mainapp/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'mainapp/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(course=self.object)
        return context


class SubmitReviewView(LoginRequiredMixin, View):
    template_name = 'mainapp/submit_review.html'

    def get(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, pk=course_id)
        form = ReviewForm()
        return render(request, self.template_name, {'form': form, 'course': course})

    def post(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, pk=course_id)
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.course = course
            review.save()
            return redirect('course_detail', course_id=course_id)

        return render(request, self.template_name, {'form': form, 'course': course})


class UserProfileView(View):
    template_name = 'mainapp/user_profile.html'

    def get(self, request, username, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user__username=username)
        reviews = Review.objects.filter(user=user_profile.user)
        return render(request, self.template_name, {'user_profile': user_profile, 'reviews': reviews})


class StudentsListView(ListView):
    model = Student
    template_name = 'mainapp/student_list.html'
    context_object_name = 'students'


class StudentDetailView(DetailView):
    model = Student
    template_name = 'mainapp/student_detail.html'
    context_object_name = 'student'


class DiscoverView(View):
    template_name = 'mainapp/discover.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(institute__name__icontains=query) |
            Q(instructor__icontains=query)
        )
        return render(request, self.template_name, {'courses': courses, 'query': query})


class CompareCoursesView(View):
    template_name = 'mainapp/compare_courses.html'

    def get(self, request, *args, **kwargs):
        course_ids = request.GET.getlist('courses')
        courses = Course.objects.filter(pk__in=course_ids)
        return render(request, self.template_name, {'courses': courses})


class SaveCourseView(LoginRequiredMixin, View):
    def get(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, pk=course_id)
        request.user.userprofile.saved_courses.add(course)
        return redirect('course_detail', course_id=course_id)


class SavedCoursesView(LoginRequiredMixin, View):
    template_name = 'mainapp/saved_courses.html'

    def get(self, request, *args, **kwargs):
        saved_courses = request.user.userprofile.saved_courses.all()
        return render(request, self.template_name, {'saved_courses': saved_courses})


class AboutSkillRadarView(View):
    template_name = 'mainapp/about_skill_radar.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AboutDataView(View):
    template_name = 'mainapp/about_data.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class TermsOfUseView(View):
    template_name = 'mainapp/terms_of_use.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AccessibilityView(View):
    template_name = 'mainapp/accessibility.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class PrivacyCookiePolicyView(View):
    template_name = 'mainapp/privacy_cookie_policy.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ContactUsView(View):
    template_name = 'mainapp/contact_us.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
