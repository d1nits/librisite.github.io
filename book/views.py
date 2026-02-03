from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Review, Category, Selection
from .forms import ReviewForm, SelectionForm, BookForm


def home(request):
    return render(request, 'book/indexx.html')


def homepage(request):
    return render(request, 'book/homepage.html')


@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect('review_create', book_slug=book.slug)
    else:
        form = BookForm()

    return render(request, 'book/book_form.html', {
        'form': form
    })


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book/book_list.html', {'books': books})


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    reviews = Review.objects.filter(book=book).select_related('author')
    return render(
        request,
        'book/book_detail.html',
        {'book': book, 'reviews': reviews}
    )




def review_list(request):
    reviews = Review.objects.select_related('book', 'author')
    return render(request, 'book/review_list.html', {'reviews': reviews})


def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)

    return render(request, 'book/review_detail.html', {
        'review': review
    })



@login_required
def review_create(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.author = request.user.profile
            review.save()
            return redirect('book_detail', slug=book.slug)
    else:
        form = ReviewForm()

    return render(request, 'book/review_form.html', {
        'form': form,
        'book': book
    })

@login_required
def review_edit(request, pk):
    review = get_object_or_404(
        Review,
        pk=pk,
        author=request.user.profile
    )

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_detail', pk=review.pk)
    else:
        form = ReviewForm(instance=review)

    return render(
    request,
    'book/review_form.html',
    {
        'form': form,
        'review': review,
        'book': review.book,   
        'is_edit': True
    }
)


@login_required
def review_delete(request, pk):
    review = get_object_or_404(
        Review,
        pk=pk,
        author=request.user.profile
    )

    if request.method == 'POST':
        review.delete()
        return redirect('review_list')

    return render(
        request,
        'book/review_delete.html',
        {'review': review}
    )




def category_list(request):
    categories = Category.objects.all()
    return render(
        request,
        'book/category_list.html',
        {'categories': categories}
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    reviews = Review.objects.filter(book__category=category)
    return render(
        request,
        'book/category_detail.html',
        {'category': category, 'reviews': reviews}
    )




@login_required
def selection_list(request):
    selections = Selection.objects.filter(user=request.user)
    return render(
        request,
        'book/selection_list.html',
        {'selections': selections}
    )


@login_required
def selection_detail(request, pk):
    selection = get_object_or_404(
        Selection,
        pk=pk,
        user=request.user
    )
    return render(
        request,
        'book/selection_detail.html',
        {'selection': selection}
    )


@login_required
def create_selection(request):
    if request.method == 'POST':
        form = SelectionForm(request.POST)
        if form.is_valid():
            selection = form.save(commit=False)
            selection.user = request.user
            selection.save()
            form.save_m2m()
            return redirect('selection_list')
    else:
        form = SelectionForm()

    return render(
        request,
        'book/selection_form.html',
        {'form': form}
    )


@login_required
def edit_selection(request, pk):
    selection = get_object_or_404(
        Selection,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        form = SelectionForm(request.POST, instance=selection)
        if form.is_valid():
            form.save()
            return redirect('selection_detail', pk=pk)
    else:
        form = SelectionForm(instance=selection)

    return render(
        request,
        'book/selection_form.html',
        {'form': form}
    )



@login_required
def delete_selection(request, pk):
    selection = get_object_or_404(
        Selection,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        selection.delete()
        return redirect('selection_list')

    return render(
        request,
        'book/delete_selection.html',
        {'selection': selection}
    )
