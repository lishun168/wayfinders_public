from django.shortcuts import render
from django.views import View
from .models import Thread, Post

class ForumDirectory(View):
    template_name='forum/forum_directory.html'

    def get(self, request):
        threads = Thread.objects.all()
        context = {
            'threads': threads
        }

        return render(request, self.template_name, context)

class ThreadPage(View):
    template_name='forum/thread.html'

    def get(self, request, pk):
        posts = Post.objects.filter(pk=pk)
        thread = Thread.objects.get(pk=pk)

        context = {
            'thread': thread,
            'posts': posts
        }

        return render(request, self.template_name, context)
