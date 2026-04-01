from django.shortcuts import render, redirect, get_object_or_404
from .models import Election, Candidate, Vote
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.dateparse import parse_datetime
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


#  Custom Login
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('home')


#  Home
@login_required
def home(request):
    elections = Election.objects.all()
    return render(request, 'home.html', {
        'elections': elections,
        'now': timezone.now(),
        'user': request.user
    })


#  Logout
def custom_logout(request):
    logout(request)
    return redirect('/login/')


#  Admin Dashboard
@staff_member_required
def admin_dashboard(request):
    elections = Election.objects.all()
    return render(request, 'admin_dashboard.html', {
        'elections': elections,
        'now': timezone.now()   # ✅ ADD THIS
    })


#  Create Election
@staff_member_required
def create_election(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = parse_datetime(request.POST.get('start_date'))
        end_date = parse_datetime(request.POST.get('end_date'))

        if start_date >= end_date:
            messages.error(request, "End date must be after start date")
            return redirect('create_election')

        Election.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date
        )

        messages.success(request, "Election created successfully")
        return redirect('admin_dashboard')

    return render(request, 'create_election.html')


#  Delete Election
@staff_member_required
def delete_election(request, election_id):
    election = get_object_or_404(Election, id=election_id)

    if request.method == 'POST':
        election.delete()
        return redirect('admin_dashboard')

    return render(request, 'delete_election.html', {'election': election})


#  Stop Voting
@staff_member_required
def stop_voting(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    election.end_date = timezone.now()
    election.save()

    messages.success(request, "Voting stopped successfully")
    return redirect('admin_dashboard')


# ➕ Add Candidate + LIST
@staff_member_required
def add_candidate(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election)

    if request.method == 'POST':
        name = request.POST.get('name')
        manifesto = request.POST.get('manifesto')

        Candidate.objects.create(
            election=election,
            name=name,
            manifesto=manifesto
        )

        messages.success(request, "Candidate added successfully")
        return redirect('add_candidate', election_id=election.id)

    return render(request, 'add_candidate.html', {
        'election': election,
        'candidates': candidates
    })


#  Delete Candidate
@staff_member_required
def delete_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    election_id = candidate.election.id

    candidate.delete()
    messages.success(request, "Candidate removed")

    return redirect('add_candidate', election_id=election_id)


#  Register
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        # Password check
        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Username check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        #  Email uniqueness check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        # College email restriction
        if not email.endswith('.nits.ac.in'):
            messages.error(request, "Use college email only")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')


#  Vote
@login_required
def vote(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election)

    now = timezone.now()

    if not (election.start_date <= now <= election.end_date):
        return render(request, 'error.html', {'message': 'Election is not active'})

    if Vote.objects.filter(user=request.user, election=election).exists():
        return render(request, 'error.html', {'message': 'You have already voted'})

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate')

        if not candidate_id:
            return render(request, 'error.html', {'message': 'Please select a candidate'})

        candidate = get_object_or_404(Candidate, id=candidate_id)

        Vote.objects.create(
            user=request.user,
            candidate=candidate,
            election=election
        )

        return redirect('home')

    return render(request, 'vote.html', {
        'election': election,
        'candidates': candidates
    })


#  Results
@login_required
def results(request, election_id):
    election = get_object_or_404(Election, id=election_id)

    now = timezone.now()

    # Restrict only normal users
    if not request.user.is_staff and election.end_date > now:
        return render(request, 'error.html', {
            'message': 'Results will be available after the election ends.'
        })

    # Admin can always see
    candidates = Candidate.objects.filter(election=election).annotate(
        total_votes=Count('vote')
    ).order_by('-total_votes')

    max_votes = candidates[0].total_votes if candidates else 0
    winners = [c for c in candidates if c.total_votes == max_votes]

    return render(request, 'results.html', {
        'candidates': candidates,
        'election': election,
        'winners': winners,
        'max_votes': max_votes,
        'is_admin': request.user.is_staff   # 🔥 IMPORTANT
    })