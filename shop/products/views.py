from django import forms
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, UpdateView

from .models import Product, Filter_Product, Comments
from .forms import EmailPostForm, CommentsForm
from django.core.mail import send_mail
from django.conf import settings
from .utils import q_search

from .templatetags.products_tags import products_list_tags
from orders.models import OrderItem


def products_list(request):
    products_count = Product.objects.count()
    products = Product.objects.filter(is_have=True)
    filters = Filter_Product.objects.filter(is_have=True)
    # products = products_list_tags()
    page = request.GET.get('page', 1)
    per_page = 2
    title = 'Главная страница'

    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    color_white = request.GET.get('color_white', None)
    color_grey = request.GET.get('color_grey', None)
    query = request.GET.get('q', None)

    if query:
        products = q_search(query)
        title = f'Поиск по "{query}"'

    if on_sale:
        products = products.filter(discount__gt=0)

    if order_by and order_by != 'default':
        products = products.order_by(order_by)

    if color_white:
        products = products.filter(phone_color='Белый')

    if color_grey:
        products = products.filter(phone_color='Натуральный Титан')

    paginator = Paginator(products, per_page)
    current_page = paginator.page(int(page))
    return render(request, 'products/products.html', {'title': title,
                                                      'products': current_page, 'filters': filters, 'per_page': per_page,
                                                      'products_count': products_count})


# def products_detail(request, product_slug):
#     products = get_object_or_404(Product, slug=product_slug)
#
#     comments = products.comments_products.filter(active=True)
#
#     if request.method == 'POST':
#         comment_form = CommentsForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.product = products
#             new_comment.user = request.user
#             new_comment.save()
#
#             new_comment2 = Comments.objects.filter(product=new_comment.product, user=new_comment.user)
#             if new_comment2.exists():
#                 print('yes exists')
#                 #comment_form = ()
#                 return render(request, 'products/detail.html', {'products': products,
#                                                                 'title': products.name,
#                                                                 'comments': comments})
#
#             else:
#                 comment_form = CommentsForm()
#                 messages.success(request, 'Отзыв успешно добавлен!')
#                 return render(request, 'products/detail.html', {'products': products,
#                                                                 'title': products.name,
#                                                                 'comment_form': comment_form,
#                                                                 'comments': comments})
#
#
#
#     else:
#         comment_form = CommentsForm()
#         return render(request, 'products/detail.html', {'products': products,
#                                                         'title': products.name,
#                                                         'comment_form': comment_form,
#                                                         'comments': comments})


def products_detail(request, product_slug):
    products = get_object_or_404(Product, slug=product_slug)
    order_items = OrderItem.objects.filter(user=request.user, product=products)

    comments = products.comments_products.filter(active=True)
    comments2 = Comments.objects.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = products
            new_comment.user = request.user

            new_comment2 = Comments.objects.filter(product=new_comment.product, user=new_comment.user)
            if not new_comment2.exists() and order_items:
                # rating_comment = comment_form.cleaned_data['rating']
                # if rating_comment > 5 or rating_comment < 1:
                #     raise forms.ValidationError('Оценка не должна превышать 5 и быть меньше 1')
                new_comment.save()
                comment_form = CommentsForm()
                print('yes exists')
                messages.success(request, 'Отзыв успешно добавлен!')
                return render(request, 'products/detail.html', {'products': products,
                                                                 'title': products.name,
                                                                'comment_form': comment_form,
                                                                 'comments': comments, 'comments2': comments2})
            elif not order_items:
                messages.success(request, 'Приобретите товар, предже чем писать отзыв:)')
                return redirect(request.META['HTTP_REFERER'])

            else:
                messages.success(request, 'Вы уже оставили отзыв!')
                return redirect(request.META['HTTP_REFERER'])

    else:
        comment_form = CommentsForm()

        return render(request, 'products/detail.html', {'products': products,
                                                                'title': products.name,
                                                                'comment_form': comment_form,
                                                                'comments': comments, 'comments2': comments2})


def comment_remove(request, comment_id):
    comment = Comments.objects.get(id=comment_id)
    comment.delete()

    return redirect(request.META['HTTP_REFERER'])


class CommentUpdate(UpdateView):
    model = Comments
    form_class = CommentsForm
    # fields = ['body']
    template_name = 'products/update_detail.html'
    # products = get_object_or_404(Product, slug=form_class.pk)
    success_url = reverse_lazy('products:home')

    #def get(self, request, pk):
    #    next_url = request.GET.get('next')
    #    form = CommentsForm()
    #    return render(request, template_name=self.template_name, context={'form': form, "next": next_url})
    #    #return redirect(next_url)
#
    #def post(self, request, pk):
    #    form = CommentsForm(request.POST)
    #    next_url = request.POST.get('next')
    #    return redirect(next_url)

    # def get(self, request, *args, **kwargs):
    #     # TaskNotification.objects.filter(assigned_to=request.user).update(read=True)
    #     print(request.META.get('HTTP_REFERER'))
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#class ProductDetail(FormMixin, DetailView):
#    form_class = CommentsForm
#    template_name = 'products/detail.html'
#    context_object_name = 'products'
#    model = Product
#
#    def get_success_url(self):
#        return reverse_lazy('products:detail', kwargs={'product_slug': self.get_object().id})
#
#    def post(self, request, *args, **kwargs):
#        form = self.get_form()
#        if form.is_valid():
#            return self.form_valid(form)
#        else:
#            return self.form_invalid(form)
#
#    def form_valid(self, form):
#        self.object = form.save(commit=False)
#        self.object.product = self.get_object()
#        self.object.user = self.request.user
#        self.object.save()
#        return super().form_valid(form)





def product_share(request, product_slug):
    products = get_object_or_404(Product, slug=product_slug)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            #post_url = request.build_absolute_uri(products.get_absolute_url())
            subject = '{} ({}) recommends you buy "{}"'.format(cd['name'], settings.EMAIL_HOST_USER, products.name)
            message = 'Buy "{}" at \n\n{}\'s comments: {}'.format(products.name, cd['name'], cd['comments'])
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['email']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'products/share.html', {'products': products,
                                                                        'form': form, 'sent': sent, 'title': 'Отправка сообщения'})


#def message_email(request):
#   sent = False
#   if request.method == 'POST':
#       form = EmailPostForm(request.POST)
#
#       if form.is_valid():
#           cd = form.cleaned_data
#           subject = '{} ({}) recommends you buy '.format(cd['name'], settings.EMAIL_HOST_USER)
#           message = 'Buy  at \n\n{}\'s comments: {}'.format(cd['name'], cd['comments'])
#           send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['email']])
#       else:
#           form = EmailPostForm()
#       return render(request, 'products/share.html', {'form': form, 'sent': sent, 'title': 'Отправка сообщения'})


def send_message(request, product_slug):
    products = get_object_or_404(Product, slug=product_slug)
    name = f'{request.user.username}, рекомендуем вам {products.name}'
    email = request.user.email
    comments = f'Рекомендуем вам {products.name}, на него сейчас действует скидка!'
    send_mail(name, comments, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    messages.success(request, f'Вам отправлено сообщение на указанный вами раннее Email ({email})')

    return redirect(request.META['HTTP_REFERER'])

