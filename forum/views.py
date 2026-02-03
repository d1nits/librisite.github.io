from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import ForumThread, Comment
from .forms import ForumThreadForm, CommentForm
from django.utils.text import slugify



@login_required
def thread_create(request):
    if request.method == 'POST':
        form = ForumThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            slug = slugify(thread.title)
            original_slug = slug
            counter = 1
            while ForumThread.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            thread.slug = slug
            thread.save()
            return redirect('forum:thread_list')  
    else:
        form = ForumThreadForm()
    return render(request, 'forum/thread_create.html', {'form': form})


def thread_list(request):
    threads = ForumThread.objects.all().order_by('-created_at')
    return render(request, 'forum/thread_list.html', {'threads': threads})

@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(ForumThread, id=thread_id)
    comments = thread.comments.filter(parent_comment__isnull=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            parent_comment_id = request.POST.get('parent_comment')  
            parent_comment = None

            if parent_comment_id: 
                parent_comment = get_object_or_404(Comment, id=parent_comment_id)

        
            Comment.objects.create(
                thread=thread,
                author=request.user,
                content=content,
                parent_comment=parent_comment  
            )
            return redirect('forum:thread_detail', thread_id=thread.id)
    else:
        form = CommentForm()

    return render(request, 'forum/thread_detail.html', {
        'thread': thread,
        'comments': comments,
        'form': form
    })

@login_required
def thread_edit(request, thread_id):
    thread = get_object_or_404(ForumThread, id=thread_id)
    
    if request.method == 'POST':
        form = ForumThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('forum:thread_detail', thread_id=thread.id)
    else:
        form = ForumThreadForm(instance=thread)
    
    return render(request, 'forum/thread_edit.html', {'form': form, 'thread': thread})

@login_required
def thread_delete(request, thread_id):
    thread = get_object_or_404(ForumThread, id=thread_id)
    if request.user != thread.author:
        return redirect('forum:thread_list')  
    

    thread.delete()
    return redirect('forum:thread_list')



@login_required
def comment_create(request, thread_id):
    thread = get_object_or_404(ForumThread, id=thread_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            comment.save()
            return redirect('forum:thread_detail', thread_id=thread.id)
    else:
        form = CommentForm()

    return render(request, 'forum/comment_create.html', {'form': form})



@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('forum:thread_detail', thread_id=comment.thread.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('forum:thread_detail', thread_id=comment.thread.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'forum/comment_edit.html', {'form': form})


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('forum:thread_detail', thread_id=comment.thread.id)

    comment.delete()
    return redirect('forum:thread_detail', thread_id=comment.thread.id)

