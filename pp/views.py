from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import FileResponse
from django.urls import reverse_lazy
import os
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist


from .models import Book
from .forms import UploadBookForm
from payment.models import Subscription

@login_required(login_url='/signin')
def index(request):
    current_plan = ""
    try:
        current_plan = Subscription.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return render(request, 'payment/home.html')

    return render(request, 'pp/index_pp.html', {'current_plan':current_plan})

@method_decorator(login_required, name='dispatch')
class UploadBook(LoginRequiredMixin, View):
    init_form = UploadBookForm()
    def post(self, request):
        form = UploadBookForm(request.POST, request.FILES)
        books = Book.objects.all()
        if form.is_valid():
            book_name = form.cleaned_data.get('book')
            if str(book_name).lower().endswith('pdf'):
                obj = form.save(commit=False)
               # obj.owner = request.user
                obj.save()
                messages.success(
                    request, "Your file has been uploaded successfully!!!")
            else:
                messages.error(
                    request, "You should select pdf file (e.g: exampl.pdf).")

        else:
            messages.error(
                request, "Sorry!! you didn't select anything.")
        return render(request, 'pp/index_pp.html', {
            'form': self.init_form,
            'books': books
        })

@login_required(login_url='/signin')
def download_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return FileResponse(book.book.open(), content_type='application/pdf')

@login_required(login_url='/signin')
def read_book(request, pk, file_=None):
    book = get_object_or_404(Book, pk=pk)
    cred_id = os.environ.get('CRED_ID')     # credentail_id for adobe reader
    return render(request, 'pp/pdf_viewer.html', {'book': book})

@login_required(login_url='/signin')
def view_book(request):
    return render(request, 'pp/viewer.html')

@method_decorator(login_required, name='dispatch')
class DeleteBook(DeleteView):
    model = Book
    template_name = 'pp/confirm_delete.html'
    context_object_name = 'book'
    success_url = reverse_lazy('pp:home')

