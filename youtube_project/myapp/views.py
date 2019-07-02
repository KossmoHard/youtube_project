import json

from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin

from .youtube_api import youtube_search
from .models import *


class VideoDetailView(DetailView):
    model = Video
    template_name = 'myapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Video.objects.get(pk=self.kwargs['pk'])
        context['liked_video'] = Like.objects.filter(user=self.request.user)
        context['like'] = Like.objects.filter(object_id=obj.id, user=self.request.user)

        return context


class IndexListView(ListView):
    model = Video
    template_name = 'myapp/index.html'
    ordering = ['-published']
    paginate_by = 15

    def get_queryset(self):
        if self.request.GET.get('q'):
            obj_search = self.model.objects.filter(title__icontains=self.request.GET['q'])

            if obj_search:
                return obj_search
            else:
                video_list = youtube_search(self.request.GET['q'])
                objs = [
                    Video(
                        video_id=video['video_id'],
                        title=video['title'],
                        description=video['description'],
                        preview=video['preview'],
                        published=video['published']
                    )
                    for video in video_list
                ]
                Video.objects.bulk_create(objs)

                return video_list

        return super().get_queryset()


class LikedVideosListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'myapp/liked-videos.html'
    ordering = ['-published']
    paginate_by = 15

    def get_queryset(self):
            return Like.objects.filter(user=self.request.user)


@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        video_id = request.POST.get('slug', None)
        video_obj = Video.objects.get(video_id=video_id)
        obj_type = ContentType.objects.get_for_model(video_obj)
        likes = Like.objects.filter(content_type=obj_type, object_id=video_obj.id, user=user)

        if not likes:
            Like.objects.create(content_type=obj_type, object_id=video_obj.id, user=user)
            liked = True
        else:
            Like.objects.filter(content_type=obj_type, object_id=video_obj.id, user=user).delete()
            liked = False

    ctx = {'liked': liked}

    return HttpResponse(json.dumps(ctx), content_type='application/json')


