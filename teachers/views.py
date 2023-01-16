import csv

from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.views.generic.base import View


from teachers.models import Teacher, Subject
from teachers.serializers import TeacherSerializer, TeacherQuerySerializer
from teachers.forms import BulkImportForm


class TeachersView(View):
    """ View for list, get and bulk import teachers data with Template"""
    def get(self, request, teacher_id=None, *args, **kwargs):
        """ List and retrive Teachers details """
        template = loader.get_template("teacher_list.html")
        bulk_import_form = BulkImportForm()
        context = dict(detail_view=False, form=bulk_import_form)
        if teacher_id:
            teacher_details = Teacher.objects.get(id=teacher_id)
            context['detail_view'] = True
            context['teacher_details'] = teacher_details
        else:
            teachers = Teacher.objects.values()
            context['teachers'] = teachers
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        """ Method for Bulk import teachers data from file """
        if not request.user.is_authenticated:
            return HttpResponse('Only login users can import teachers.')
        student = BulkImportForm(request.POST, request.FILES)
        if student.is_valid():
            import_file = request.FILES['file'].read().decode('utf-8').splitlines()
            response = TeachersViewSet().bulk_import(request, import_file=import_file)
            http_response = "Bulk Import Failed."
            if response.status_code == 200:
                data_keys = list(response.data.keys())
                data_values = list(response.data.values())
                http_response = f'Successsfully Imported the file, Here is the status: <br><br> ' \
                                f'{data_keys[0]} : {data_values[0]}<br><br>'\
                                f'{data_keys[1]} : {data_values[1]}<br><br>' \
                                f'{data_keys[2]} : {data_values[2]}<br><br>'
            return HttpResponse(http_response)
        else:
            print("Not validddddd")
            return HttpResponse('No File Available')


class TeachersViewSet(viewsets.ModelViewSet):
    """
    Django Rest-API for bulk_import, list and retirve teachers data
    """
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all().prefetch_related('subjects_taught')

    def list(self, request, *args, **kwargs):
        """ Get a list of Teachers.

        - query_params last_name: optional
        - query_params subjects: optional

        - return: List<Teachers>
        """
        query_serializer = TeacherQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.data
        queryset = self.get_queryset()

        if query_params.get('last_name'):
            queryset = queryset.filter(last_name__startswith=query_params.get('last_name'))
        if query_params.get('subject'):
            queryset = queryset.filter(subjects_taught__name=query_params.get('subject'))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["post"], detail=False, url_path="bulk_import_teachers", permission_classes=[IsAuthenticated])
    def bulk_import(self, request, import_file=None):
        """ Import bulk teacher details

        Failure for adding new teachers:
        - The email already exists
        - The count of subjects taught is greater than 5
        """
        if import_file:
            teachers_data = import_file
        else:
            teachers_data = request.FILES['teachers-details.csv'].read().decode('utf-8').splitlines()
        reader = csv.DictReader(teachers_data)
        existing_subs = dict(Subject.objects.values_list('name', 'id'))
        failed_with_subjects, failed_existing, new_teachers = [], [], []
        teacher_subject = dict()
        new_subjects = set()
        for row in reader:
            email = row.get('Email Address')
            if not email:
                continue
            if Teacher.objects.filter(email_address=email).exists():
                # Email address is unique
                failed_existing.append(email)
                continue
            if row.get('Subjects taught'):
                subjects = row.get('Subjects taught').split(',')
                if len(subjects) > 5:
                    # Teachers cannot teach more than 5 subjects
                    failed_with_subjects.append(email)
                    continue
                teacher_subject[email] = [sub.strip().capitalize() for sub in subjects]
                new_subjects.update(set(teacher_subject[email]) - set(existing_subs.keys()))
            teacher_data = Teacher(
                    first_name=row.get('First Name'), last_name=row.get('Last Name'),
                    email_address=row.get("Email Address"), phone_number=row.get('Phone Number'),
                    room_number=row.get('Room Number')
                )
            if row.get('Profile picture').strip():
                teacher_data.profile_picture = f"profile_pictures/{row.get('Profile picture')}"
            new_teachers.append(teacher_data)

        # Creating new techers in bulk
        all_teachers = Teacher.objects.bulk_create(new_teachers)

        # Create subjects which are currently not exists
        Subject.objects.bulk_create([Subject(name=sub) for sub in new_subjects])
        all_subs = dict(Subject.objects.values_list('name', 'id'))

        # Adding subjects to the newly added teachers
        for each_teacher in all_teachers:
            each_teacher.subjects_taught.set(
                [all_subs[each_sub] for each_sub in teacher_subject.get(each_teacher.email_address)]
            )
        response = {
            "Newly added": len(all_teachers), "Failed due to more than 5 subjects": len(failed_with_subjects),
            "Existing email addresses": len(failed_existing)
        }
        return Response(response)
