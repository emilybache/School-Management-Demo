import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.corecode.models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,
)
from apps.finance.models import Invoice, InvoiceItem, Receipt
from apps.result.models import Result
from apps.students.models import Student

SITE_CONFIG = {
    "school_name": "School Management System",
    "school_slogan": "A great school",
    "school_address": "123 Main Street, Anytown",
}

# The last session listed becomes the current one.
SESSIONS = ["2019/2020", "2020/2021", "2021/2022"]
CURRENT_TERM = "1st Term"
TERMS = ["1st Term", "2nd Term", "3rd Term"]
SUBJECTS = ["Mathematics", "English", "Physics"]
CLASSES = ["JSS 1", "JSS 2", "11th Math", "11th"]

ADMISSION_DATE = datetime.date(2022, 1, 7)

STUDENTS = [
    {
        "registration_number": "1",
        "surname": "Doe",
        "firstname": "John",
        "date_of_birth": datetime.date(2006, 3, 15),
        "current_class": "11th Math",
        "address": "123 Main Street, Anytown",
        "parent_mobile_number": "5550100001",
        "passport": "students/passports/person-0030-1_InkyBlue.png",
    },
    {
        "registration_number": "2",
        "surname": "Roe",
        "firstname": "Richard",
        "date_of_birth": datetime.date(2006, 7, 22),
        "current_class": "11th",
        "address": "456 Oak Avenue, Anytown",
        "parent_mobile_number": "5550100002",
        "passport": "students/passports/person-0033-3_InkyBlue.png",
    },
    {
        "registration_number": "3",
        "surname": "Smith",
        "firstname": "James",
        "date_of_birth": datetime.date(2005, 11, 5),
        "current_class": "11th Math",
        "address": "789 Pine Road, Anytown",
        "parent_mobile_number": "5550100003",
        "passport": "students/passports/person-0028-3_InkyBlue.png",
    },
]

# (student registration number, subject, test score, exam score)
RESULTS = [
    ("1", "English", 50, 51),
    ("1", "Mathematics", 50, 50),
    ("1", "Physics", 50, 50),
]

INVOICE_STUDENT = "1"
INVOICE_ITEMS = [
    ("class fee", 1000),
    ("exam fee", 500),
    ("dress fees", 500),
    ("sport fee", 500),
]
RECEIPT = {"amount_paid": 2000, "date_paid": ADMISSION_DATE, "comment": "fees paid"}


class Command(BaseCommand):
    help = "Load demo data (sessions, classes, students, results, an invoice). Safe to re-run."

    @transaction.atomic
    def handle(self, *args, **options):
        for key, value in SITE_CONFIG.items():
            SiteConfig.objects.update_or_create(key=key, defaults={"value": value})

        for name in SESSIONS:
            AcademicSession.objects.update_or_create(
                name=name, defaults={"current": name == SESSIONS[-1]}
            )
        for name in TERMS:
            AcademicTerm.objects.update_or_create(
                name=name, defaults={"current": name == CURRENT_TERM}
            )
        # The post_save signals reset "current" on the others, so re-fetch these.
        session = AcademicSession.objects.get(current=True)
        term = AcademicTerm.objects.get(current=True)

        subjects = {
            name: Subject.objects.get_or_create(name=name)[0] for name in SUBJECTS
        }
        classes = {
            name: StudentClass.objects.get_or_create(name=name)[0] for name in CLASSES
        }

        students = {}
        for data in STUDENTS:
            data = dict(data, current_class=classes[data["current_class"]])
            reg_no = data.pop("registration_number")
            students[reg_no], _ = Student.objects.update_or_create(
                registration_number=reg_no,
                defaults=dict(data, date_of_admission=ADMISSION_DATE),
            )

        for reg_no, subject, test_score, exam_score in RESULTS:
            student = students[reg_no]
            Result.objects.update_or_create(
                student=student,
                session=session,
                term=term,
                subject=subjects[subject],
                defaults={
                    "current_class": student.current_class,
                    "test_score": test_score,
                    "exam_score": exam_score,
                },
            )

        student = students[INVOICE_STUDENT]
        invoice, _ = Invoice.objects.get_or_create(
            student=student,
            session=session,
            term=term,
            defaults={"class_for": student.current_class},
        )
        for description, amount in INVOICE_ITEMS:
            InvoiceItem.objects.update_or_create(
                invoice=invoice, description=description, defaults={"amount": amount}
            )
        Receipt.objects.get_or_create(invoice=invoice, **RECEIPT)

        self.stdout.write(self.style.SUCCESS("Demo data loaded."))
