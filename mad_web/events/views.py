import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView, FormView
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from mad_web.events.serializers import EventSerializer
from mad_web.utils.utils import TaOrOfficerRequiredMixin
from .forms import ConfirmAttendanceForm
from .models import Event, EventCalendar, EventTag
from ..users.models import User


class EventListView(ListView):
    model = Event
    # These next two lines tell the view to index lookups by username
    slug_field = 'startTime'
    slug_url_kwarg = 'startTime'

    def get_queryset(self):
        qs = super(EventListView, self).get_queryset()
        now = datetime.datetime.now()
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return qs.filter(start_time__gte=now)


def calendar(request, year=datetime.datetime.now().year, month=datetime.datetime.now().month):
    # setup arguments, as it is a string and needs to be an int
    year = int(year)
    month = int(month)

    event_list = Event.objects.order_by('start_time').filter(
        start_time__year=year, start_time__month=month
    )
    calendar_html = EventCalendar(event_list).formatmonth(year, month)

    data = {
        'calendar': mark_safe(calendar_html)
    }
    return render(request, 'events/event_calendar.html', context=data)


class EventDetailView(DetailView):
    model = Event
    slug_field = 'id'
    slug_url_kwarg = 'id'


class EventConfirmAttendanceView(TaOrOfficerRequiredMixin, FormView):
    template_name = 'events/event_confirm_attendance.html'
    form_class = ConfirmAttendanceForm
    success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        context = super(EventConfirmAttendanceView, self).get_context_data(**kwargs)
        id = int(self.kwargs.get("id"))
        context['event'] = get_object_or_404(Event, pk=id)
        context['user'] = get_object_or_404(User, username=self.kwargs.get("username"))
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.confirm_attendance()
        return super(EventConfirmAttendanceView, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Confirmed!')
        return reverse('home:feed')


# ViewSets define the view behavior.
class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.order_by('-start_time')
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = EventSerializer
    ordering = ('-start_time',)

    def get_queryset(self):
        # Optionally filter by tag
        queryset = Event.objects.order_by('-start_time')
        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            clean_tag = int(tag)
            tag_object = None
            try:
                tag_object = EventTag.objects.get(pk=clean_tag)
            except EventTag.DoesNotExist:
                raise NotFound(detail="The tag does not exist")
            if tag_object is not None:
                queryset = tag_object.event_tags.all()
                #queryset = Event.objects.raw(                'SELECT * FROM "events_event" WHERE %d = ANY ("events_event"."event_tags") ORDER BY "events_event"."start_time" DESC' % (                clean_tag))
        return queryset
