from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from .models import Product, Category, Review
from .forms import ReviewForm

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)



class SubmitReview(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "products/add_review.html"
    # fields = '__all__'
    def form_valid(self, form):
        product = Product.objects.get(pk=self.kwargs['product_id'])
        form.instance.product = product
        #form.instance.product = self.kwargs['product_id']
        #form.instance.product = Product.objects.get(id=self.kwargs['product_id'])
        form.save()
        return redirect(reverse('products'))



class UpdateReview(UpdateView):
    model = Review
    template_name = 'products/edit_review.html'
    fields = ['body']

class DeleteReview(DeleteView):
    model = Review
    template_name = 'products/delete_review.html'