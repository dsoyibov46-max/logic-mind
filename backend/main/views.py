from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Avg, Max, Count
from django.contrib import messages
from users.forms import CustomUserCreationForm, CustomLoginForm
from game_app.models import Game
from results.models import GameResult
from .models import ClassGroup
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClassGroupForm
from .models import ClassGroup
from .models import ClassGroup, Assignment
from .forms import ClassGroupForm, AssignmentForm
User = get_user_model()


def get_user_role(user):
    if hasattr(user, 'role'):
        return user.role

    if hasattr(user, 'profile'):
        return user.profile.role

    return None


def index(request):
    return render(request, 'main/index.html')


def redirect_by_role(user):
    role = get_user_role(user)

    if role == 'student':
        return redirect('student_dashboard')
    elif role == 'teacher':
        return redirect('teacher_dashboard')
    elif role == 'parent':
        return redirect('parent_dashboard')

    return redirect('index')


def register_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_by_role(user)
    else:
        form = CustomUserCreationForm()

    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_by_role(user)
    else:
        form = CustomLoginForm()

    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def student_dashboard(request):
    role = get_user_role(request.user)

    if role != 'student':
        return HttpResponseForbidden("Sizda bu sahifaga kirish huquqi yo‘q.")

    results = GameResult.objects.filter(user=request.user).select_related('game')

    total_tasks = results.count()
    completed_tasks = results.filter(score__gte=50).count()
    pending_tasks = total_tasks - completed_tasks

    avg_score = results.aggregate(avg=Avg('score'))['avg'] or 0
    monitoring = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    my_groups = ClassGroup.objects.filter(
        students=request.user
    ).prefetch_related('students')

    assignments = Assignment.objects.filter(
        group__in=my_groups,
        status='published'
    ).select_related(
        'group',
        'teacher'
    ).order_by('-created_at')

    context = {
        'title': 'Student Dashboard',
        'monitoring': monitoring,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'average_score': int(avg_score),
        'games': Game.objects.filter(is_active=True),
        'results': results.order_by('-played_at'),

        # yangi qo‘shilganlar
        'my_groups': my_groups,
        'assignments': assignments,
    }

    return render(request, 'main/student_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    role = get_user_role(request.user)

    if role != 'teacher':
        return redirect('index')

    if hasattr(User, 'role'):
        students = User.objects.filter(role='student')
    else:
        students = User.objects.filter(profile__role='student')

    student_stats = []

    for student in students:

        results = GameResult.objects.filter(user=student)

        student_stats.append({
            'id': student.id,
            'username': student.username,
            'avatar': student.avatar,

            'total_games': results.count(),

            'best_score':
                results.aggregate(best=Max('score'))['best'] or 0,
        })

    total_students = students.count()

    total_games_played = GameResult.objects.count()

    avg_score = (
        GameResult.objects.aggregate(avg=Avg('score'))['avg'] or 0
    )

    avg_time = (
        GameResult.objects.aggregate(avg=Avg('time_spent'))['avg'] or 0
    )

    top_students = (
    GameResult.objects
    .values(
        'user__id',
        'user__username',
        'user__avatar'
    )
    .annotate(best_score=Max('score'))
    .order_by('-best_score')[:5]
    )
    groups = ClassGroup.objects.filter(teacher=request.user)
    context = {
        'title': 'Teacher Dashboard',
        'groups': groups,

        'students': students,
        'student_stats': student_stats,

        'total_students': total_students,
        'total_games_played': total_games_played,

        'avg_score': avg_score,
        'avg_time': avg_time,

        'top_students': top_students,
    }

    return render(
        request,
        'main/teacher.html',
        context
    )
    role = get_user_role(request.user)

    if role != 'teacher':
        return redirect('index')

    if hasattr(User, 'role'):
        students = User.objects.filter(role='student')
    else:
        students = User.objects.filter(profile__role='student')

    student_stats.append({
         'id': student.id,
         'username': student.username,
         'avatar': student.avatar,
         'total_games': results.count(),
          'best_score':
         results.aggregate(best=Max('score'))['best'] or 0,
        })

    total_students = students.count()
    total_games_played = GameResult.objects.count()

    avg_score = GameResult.objects.aggregate(avg=Avg('score'))['avg'] or 0
    avg_time = GameResult.objects.aggregate(avg=Avg('time_spent'))['avg'] or 0

    top_students = (
        GameResult.objects
        .values('user__id', 'user__username')
        .annotate(best_score=Max('score'))
        .order_by('-best_score')[:5]
    )

    context = {
        'title': 'Teacher Dashboard',
        'students': students,
        'student_stats': student_stats,
        'total_students': total_students,
        'total_games_played': total_games_played,
        'avg_score': avg_score,
        'avg_time': avg_time,
        'top_students': top_students,
    }

    return render(request, 'main/teacher.html', context)


@login_required
def teacher_student_detail(request, student_id):
    role = get_user_role(request.user)

    if role != 'teacher':
        return redirect('index')

    student = get_object_or_404(User, id=student_id)

    student_results = (
        GameResult.objects
        .filter(user=student)
        .select_related('game')
        .order_by('-played_at')
    )

    total_games = student_results.count()
    best_score = student_results.aggregate(best=Max('score'))['best'] or 0
    avg_score = student_results.aggregate(avg=Avg('score'))['avg'] or 0
    avg_time = student_results.aggregate(avg=Avg('time_spent'))['avg'] or 0

    game_stats = (
        student_results
        .values('game__title')
        .annotate(
            played_count=Count('id'),
            best_score=Max('score'),
            avg_score=Avg('score'),
        )
        .order_by('-best_score')
    )

    chart_results = student_results.order_by('played_at')

    score_labels = []
    score_data = []
    time_data = []

    for result in chart_results:
        score_labels.append(result.played_at.strftime("%d.%m"))
        score_data.append(result.score)
        time_data.append(result.time_spent)

    if avg_score >= 80:
        performance_status = "Excellent"
        performance_class = "excellent"
    elif avg_score >= 50:
        performance_status = "Good"
        performance_class = "good"
    else:
        performance_status = "Needs Improvement"
        performance_class = "weak"

    context = {
        'student': student,
        'student_results': student_results,
        'total_games': total_games,
        'best_score': best_score,
        'avg_score': avg_score,
        'avg_time': avg_time,
        'game_stats': game_stats,

        'score_labels': score_labels,
        'score_data': score_data,
        'time_data': time_data,
        'performance_status': performance_status,
        'performance_class': performance_class,
    }

    return render(request, 'main/teacher_student_detail.html', context)

@login_required
def parent_dashboard(request):
    role = get_user_role(request.user)

    if role != 'parent':
        return HttpResponseForbidden("Sizda bu sahifaga kirish huquqi yo‘q.")

    child = User.objects.filter(
    role='student',
    parent=request.user
    ).first()

    if child:
        child_results = GameResult.objects.filter(user=child).select_related('game')
    else:
        child_results = GameResult.objects.none()

    total_games = child_results.count()
    best_score = child_results.aggregate(best=Max('score'))['best'] or 0
    avg_score = child_results.aggregate(avg=Avg('score'))['avg'] or 0
    avg_time = child_results.aggregate(avg=Avg('time_spent'))['avg'] or 0

    if avg_score >= 80:
        ai_status = "A’lo natija"
        ai_recommendation = "Farzandingiz yuqori natija ko‘rsatmoqda. Murakkabroq mantiqiy mashqlar berish tavsiya etiladi."
    elif avg_score >= 50:
        ai_status = "O‘rtacha natija"
        ai_recommendation = "Farzandingiz natijalari o‘rtacha. Muntazam mashq qilish orqali natijani oshirish mumkin."
    else:
        ai_status = "Qo‘shimcha nazorat kerak"
        ai_recommendation = "Farzandingizga qo‘shimcha yordam va ko‘proq amaliy mashqlar kerak."

    context = {
        'title': 'Parent Dashboard',
        'child': child,
        'child_results': child_results.order_by('-played_at')[:10],
        'total_games': total_games,
        'best_score': best_score,
        'avg_score': avg_score,
        'avg_time': avg_time,
        'ai_status': ai_status,
        'ai_recommendation': ai_recommendation,
    }

    return render(request, 'main/parent_dashboard.html', context)
@login_required
def profile_settings(request):
    user = request.user

    if request.method == "POST":

        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.email = request.POST.get("email", "")

        if hasattr(user, "phone"):
            user.phone = request.POST.get("phone", "")

        if request.FILES.get("avatar"):
            user.avatar = request.FILES.get("avatar")

        user.save()

        messages.success(
            request,
            "Profil muvaffaqiyatli yangilandi."
        )

        return redirect("profile_settings")

    return render(
        request,
        "main/profile_settings.html"
    )
@login_required
def group_create(request):
    if request.user.role != 'teacher':
        return redirect('index')

    if request.method == 'POST':
        form = ClassGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.teacher = request.user
            group.save()
            form.save_m2m()
            return redirect('teacher_dashboard')
    else:
        form = ClassGroupForm()

    return render(request, 'main/group_create.html', {
        'form': form
    })


@login_required
def group_detail(request, group_id):
    if request.user.role != 'teacher':
        return redirect('index')

    group = get_object_or_404(
        ClassGroup,
        id=group_id,
        teacher=request.user
    )

    students = group.students.all()
    assignments = group.assignments.all()

    return render(request, 'main/group_detail.html', {
        'group': group,
        'students': students,
        'assignments': assignments
    })
@login_required
def assignment_create(request):
    if request.user.role != 'teacher':
        return redirect('index')

    if request.method == 'POST':
        form = AssignmentForm(request.POST, teacher=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user
            assignment.save()
            return redirect('group_detail', group_id=assignment.group.id)
    else:
        form = AssignmentForm(teacher=request.user)

    return render(request, 'main/assignment_create.html', {
        'form': form
    })