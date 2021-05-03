from django.shortcuts import redirect

def homepage(request):
    return redirect('golf_course_list')
