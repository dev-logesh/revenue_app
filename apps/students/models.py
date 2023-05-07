from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from apps.corecode.models import StudentClass ,scheme


class Student(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("Discontinued", "Discontinued"),("Break","break"),
                      ("Long Absent","Long Absent")]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    OUALIFICATION_CHOISES = [
        ("Student","Student"),
        ("House Wife","House Wife"),
        ("Employed","Employed"),
        ("Unemployed","Unemployed"),
        ("Business","Business"),
        ("others","others"),

        ]
    RELIGION_CHOISES =[
        ("HINDU","HINDU"),
        ("MUSLIM","MUSLIM"),
        ("Christian","Christian"),
        ("OTHERS","OTHERS"),


    ]
    COMMUNITY_CHOISES = [
        ("OC","OC"),
        ("BC","BC"),
        ("MBC","MBC"),
        ("ST/SC","ST/SC"),
        ("Others" , "Others"),
    ]


    current_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="active"
    )
    enrollment_number = models.CharField("Enrollment Number",max_length=200, unique=True)
    name = models.CharField("Student Name",max_length=200,default=None)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    course = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, blank=True, null=True
    )
    Total_fee = models.IntegerField("Total Fees",default=0)
    date_of_admission = models.DateField(default=timezone.now)
    Source = models.ForeignKey(
        scheme, on_delete=models.SET_NULL, blank=True, null=True
    )
    aadhar_no = models.IntegerField("Aadhar Card Number",default=None)
    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    parent_mobile_number = models.CharField("Mobile Number",
        validators=[mobile_num_regex], max_length=13, blank=True
    )
    guardian_name = models.CharField("Father\'s/Husband\'s Name" , max_length=500,default=None,blank=True,null=True)
    mother_name = models.CharField("Mother\'s Name" , max_length=500,default=None,blank=True,null=True)
    guardian_occ = models.CharField("Father\'s/Husband\'s Occupation",max_length=500,default=None,blank=True,null=True)
    student_occupation = models.CharField("Student Occupation",choices=OUALIFICATION_CHOISES,max_length=200,default=None,blank=True,null=True)
    student_company = models.CharField("Company Name",max_length=500,default=None,blank=True,null=True)
    student_qulaification = models.CharField("Student Qualification",max_length=500,default=None,blank=True,null=True)
    student_religion = models.CharField("Student Religion",choices=RELIGION_CHOISES,max_length=500,default=None,blank=True,null=True)
    student_community = models.CharField("Student Community",choices=COMMUNITY_CHOISES,max_length=500,default=None,blank=True,null=True)


    address = models.TextField(blank=True)
    others = models.TextField(blank=True)
    passport = models.ImageField(blank=True, upload_to="students/passports/")

    class Meta:
        ordering = ["enrollment_number"]

    def __str__(self):
        return f"{self.name} ({self.enrollment_number})"

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})


class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/")
