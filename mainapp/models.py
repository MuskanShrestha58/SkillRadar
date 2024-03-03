from django.db import models
from django.contrib.auth.models import User


class Institute(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    website = models.URLField()
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields as needed

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField()  # Duration in weeks, for example
    price = models.DecimalField(max_digits=10, decimal_places=2)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    # Add other fields as needed

    def __str__(self):
        return self.title


class Instructor(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    courses_taught = models.ManyToManyField(Course)
    # Add other fields as needed

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    # Add other fields as needed

    def __str__(self):
        return self.user.username


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    # Add other fields as needed

    def __str__(self):
        return f"{self.user.username} - {self.course.title} Review"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields for the Student model as needed

    def __str__(self):
        return self.user.username
