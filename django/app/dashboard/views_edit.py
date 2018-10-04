from django.http import Http404
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.views import generic
from django.contrib.auth.models import User


from core.models import Author, Bibtex, Book
from dashboard import forms



"""
User
"""
def get_login_user(user_id):
    return get_object_or_404(User, pk=user_id)


"""
Bibtex
"""
def bibtex_edit(request, bibtex_id=None):
    msg = False
    if bibtex_id:
        bibtex = get_object_or_404(Bibtex, pk=bibtex_id)
        submit_url = reverse("dashboard:bibtex_edit",
                             kwargs={'bibtex_id':bibtex.id})
    else:
        bibtex = Bibtex()
        submit_url = reverse("dashboard:bibtex_add")
        
    if request.method == 'POST':
        form = forms.BibtexForm(request.POST, instance=bibtex)
        if form.is_valid():
            bibtex_new = form.save(commit=False)
            bibtex_new.owner = get_login_user(request.user.id)
            bibtex_new.save()
            print("Saved", bibtex)
            return redirect('dashboard:index')
        else:
            print("validation fail")
    else:
        form = forms.BibtexForm(instance=bibtex)
        
    return render(request,
                  'dashboard/bibtex/edit.html',
                  {'msg': msg,
                   'form':form,
                   'bibtex': bibtex,
                   'submit_url': submit_url})



def bibtex_edit_step1(request):
    msg = False
    bibtex = Bibtex()
    submit_url = reverse("dashboard:bibtex_add_step1")
        
    if request.method == 'POST':
        form = forms.BibtexFormStep1(request.POST)
        if form.is_valid():
            bibtex.language = form.cleaned_data['lang']
            if form.cleaned_data['lang'] == 'EN':
                bibtex.title_en = form.cleaned_data['title']
            elif form.cleaned_data['lang'] == 'JA':
                bibtex.title_ja = form.cleaned_data['title']
            bibtex.book = form.cleaned_data['book']
            bibtex.owner = get_login_user(request.user.id)
            bibtex.save()
            print("Saved", bibtex)
            return redirect('dashboard:bibtex_edit', bibtex_id=bibtex.id,)
        else:
            print("validation fail")
    else:
        form = forms.BibtexFormStep1()
        
    return render(request,
                  'dashboard/bibtex/edit_step1.html',
                  {'msg': msg,
                   'form':form,
                   'submit_url': submit_url})



"""
Book
"""
def book_edit(request, book_id=None):
    msg = False
    if book_id:
        book = get_object_or_404(Book, pk=book_id)
        submit_text = "更新"
        submit_url = reverse("dashboard:book_edit",kwargs={'book_id':book.id})
    else:
        book = Book()
        submit_text = "登録"
        submit_url = reverse("dashboard:book_add")
        
    if request.method == 'POST':
        form = forms.BookForm(request.POST, instance=book)
        if form.is_valid():
            book_new = form.save(commit=False)
            book_new.owner = get_login_user(request.user.id)
            book_new.save()
            return redirect('dashboard:book_index')        

    form = forms.BookForm(instance=book)    
    return render(request,
                  'dashboard/book/edit.html',
                  {'msg': msg,
                   'form':form,
                   'book': book,
                   'submit_text': submit_text,
                   'submit_url': submit_url})
    


"""
Author
"""
def author_edit(request, author_id=None):
    msg = False
    if author_id:
        author = get_object_or_404(Author, pk=author_id)
        submit_url = reverse("dashboard:author_edit",
                             kwargs={'author_id':author.id})
    else:
        author = Author()
        submit_url = reverse("dashboard:author_add")
        
    if request.method == 'POST':
        form = forms.AuthorForm(request.POST, instance=author)
        if form.is_valid():
            author_new = form.save(commit=False)
            author_new.owner = get_login_user(request.user.id)
            author_new.save()
            return redirect('dashboard:author_index')

    form = forms.AuthorForm(instance=author)    
    return render(request,
                  'dashboard/author/edit.html',
                  {'msg': msg,
                   'form':form,
                   'author': author,
                   'submit_url': submit_url})


