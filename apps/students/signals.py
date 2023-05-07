import csv
import os
from io import StringIO

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.corecode.models import StudentClass , scheme

from .models import Student, StudentBulkUpload


@receiver(post_save, sender=StudentBulkUpload)
def create_bulk_student(sender, created, instance, *args, **kwargs):
    if created:
        opened = StringIO(instance.csv_file.read().decode())
        reading = csv.DictReader(opened, delimiter=",")
        students = []
        for row in reading:
            if "enrollment_number" in row and row["enrollment_number"]:
                reg = row["enrollment_number"]
                name = row["name"] if "name" in row and row["name"] else ""
                dob = (
                    row["dob"] if "dob" in row and row["dob"] else ""
                )
                an = (
                    row["aadhar_no"]
                    if "aadhar_no" in row and row["aadhar_no"]
                    else ""
                )
                fname = row["fathername"] if "fathername" in row and row["fathername"] else ""
                mname = row["Mother_name"] if "Mother_name" in row and row["Mother_name"] else ""
                current_class = (
                    row["course"]
                    if "course" in row and row["course"]
                    else ""
                )
                if current_class:
                    theclass, kind = StudentClass.objects.get_or_create(
                        name=current_class
                    )
                
                source = row["source"] if "source" in row and row["source"] else ""
                if source:
                    sche, kind = scheme.objects.get_or_create(
                        name=source
                    )
                
                doj = (
                    row["doj"]
                    if "doj" in row and row["doj"]
                    else ""
                )
                
                fee = row["Total_fee"] if "Total_fee" in row and row["Total_fee"] else ""
                gender = (
                    (row["gender"]).lower() if "gender" in row and row["gender"] else ""
                )
                
                phone = (
                    row["phone_number"]
                    if "phone_number" in row and row["phone_number"]
                    else ""
                )
                quli = row["Student_qualification"] if "Student_qualification" in row and row["Student_qualification"] else ""
                address = row["address"] if "address" in row and row["address"] else ""
                

                check = Student.objects.filter(enrollment_number=reg).exists()
                if not check:
                    students.append(
                        Student(
                            enrollment_number=reg,
                            Total_fee = fee,
                            mother_name = mname,
                            student_qulaification = quli,
                            name=name,
                            guardian_name = fname,
                            aadhar_no = an,
                            date_of_birth = dob,
                            date_of_admission =doj,
                            gender=gender,
                            course=theclass,
                            parent_mobile_number=phone,
                            address=address,
                            current_status="active",
                            Source = sche,
                        )
                    )

        Student.objects.bulk_create(students)
        instance.csv_file.close()
        instance.delete()


def _delete_file(path):
    """Deletes file from filesystem."""
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=StudentBulkUpload)
def delete_csv_file(sender, instance, *args, **kwargs):
    if instance.csv_file:
        _delete_file(instance.csv_file.path)


@receiver(post_delete, sender=Student)
def delete_passport_on_delete(sender, instance, *args, **kwargs):
    if instance.passport:
        _delete_file(instance.passport.path)
