from datetime import datetime, timedelta
from calendar import monthrange
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Meeting
from .forms import MeetingForm


def home(request):
    meetings = Meeting.objects.all().order_by('date', 'time')

    total_meetings = meetings.count()
    scheduled_count = meetings.filter(status__iexact='Scheduled').count()
    completed_count = meetings.filter(status__iexact='Completed').count()
    cancelled_count = meetings.filter(status__iexact='Cancelled').count()

    return render(request, 'schedule/home.html', {
        'meetings': meetings,
        'title': 'Upcoming Meetings',
        'total_meetings': total_meetings,
        'scheduled_count': scheduled_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
    })


def weekly(request):
    today = datetime.today().date()
    week_start = today
    week_end = today + timedelta(days=6)

    grouped_meetings = {}
    for i in range(7):
        day = today + timedelta(days=i)
        day_meetings = Meeting.objects.filter(date=day).order_by('time')
        grouped_meetings[day] = list(day_meetings)

    return render(request, 'schedule/weekly.html', {
        'grouped_meetings': grouped_meetings,
        'week_start': week_start,
        'week_end': week_end,
        'title': 'Weekly View'
    })


def monthly(request):
    today = datetime.today().date()
    meetings = Meeting.objects.filter(
        date__year=today.year,
        date__month=today.month
    ).order_by('date', 'time')

    days_in_month = monthrange(today.year, today.month)[1]
    calendar_days = []

    for day in range(1, days_in_month + 1):
        current_date = today.replace(day=day)
        day_meetings = meetings.filter(date=current_date)
        calendar_days.append({
            'date': current_date,
            'meetings': day_meetings
        })

    return render(request, 'schedule/monthly.html', {
        'calendar_days': calendar_days,
        'title': 'Monthly Meetings'
    })


def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meeting created successfully.')
            return redirect('home')
    else:
        form = MeetingForm()
    return render(request, 'schedule/create_meeting.html', {'form': form})


def meeting_detail(request, id):
    meeting = get_object_or_404(Meeting, id=id)
    return render(request, 'schedule/meeting_detail.html', {'meeting': meeting})


def edit_meeting(request, id):
    meeting = get_object_or_404(Meeting, id=id)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meeting updated successfully.')
            return redirect('meeting_detail', id=meeting.id)
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'schedule/edit_meeting.html', {
        'form': form,
        'meeting': meeting
    })


def delete_meeting(request, id):
    meeting = get_object_or_404(Meeting, id=id)
    if request.method == 'POST':
        meeting.delete()
        messages.success(request, 'Meeting deleted.')
        return redirect('home')
    return render(request, 'schedule/delete_meeting.html', {'meeting': meeting})


def cancel_meeting(request, id):
    """Cancel a meeting by updating its status to Cancelled."""
    meeting = get_object_or_404(Meeting, id=id)
    if request.method == 'POST':
        meeting.status = 'Cancelled'
        meeting.save()
        messages.success(request, 'Meeting cancelled.')
    return redirect('meeting_detail', id=meeting.id)