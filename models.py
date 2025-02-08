from multiprocessing.spawn import old_main_modules
from statistics import mode
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(default = 1)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    contact = models.CharField(max_length=250)
    dob = models.DateField(blank=True, null = True)
    address = models.TextField(blank=True, null = True)
    avatar = models.ImageField(blank=True, null = True, upload_to= 'images/')
    user_type = models.IntegerField(default = 2)
    gender = models.CharField(max_length=100, choices=[('Male','Male'),('Female','Female')], blank=True, null= True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank= True, null = True)

    def __str__(self):
        return self.user.username
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print(instance)
    try:
        profile = UserProfile.objects.get(user = instance)
    except Exception as e:
        UserProfile.objects.create(user=instance)
    instance.profile.save()

class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(default = 1)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    student_code = models.CharField(max_length=250,blank=True, null= True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, blank=True, null= True)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=100, choices=[('Male','Male'),('Female','Female')], blank=True, null= True)
    dob = models.DateField(blank=True, null= True)
    contact = models.CharField(max_length=250, blank=True, null= True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student_code + " - " + self.first_name+ " - " + self.middle_name+ " - " + self.last_name


class Class(models.Model):
    assigned_faculty = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    school_year = models.CharField(max_length=250)
    level = models.CharField(max_length=250)
    name = models.CharField(max_length=250)

    def __str__(self):
        return "[" + self.level + "] "+ self.level+ '-' +self.name

class ClassStudent(models.Model):
    classIns = models.ForeignKey(Class,on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE) 

    def __str__(self):
        return self.student.student_code

    def get_present(self):
        student =  self.student
        _class =  self.classIns
        try:
            present = Attendance.objects.filter(classIns= _class, student=student, type = 1).count()
            return present
        except:
            return 0
    
    def get_tardy(self):
        student =  self.student
        _class =  self.classIns
        try:
            present = Attendance.objects.filter(classIns= _class, student=student, type = 2).count()
            return present
        except:
            return 0

    def get_absent(self):
        student =  self.student
        _class =  self.classIns
        try:
            present = Attendance.objects.filter(classIns= _class, student=student, type = 3).count()
            return present
        except:
            return 0

class Attendance(models.Model):
    classIns = models.ForeignKey(Class,on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    type = models.CharField(max_length=250, choices = [('1','Present'),('2','Tardy'),('1','Absent')] )
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.classIns.name + "  " +self.student.student_code
