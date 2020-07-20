from .models import Basket

def basket_middleware(get_response):

    def middleware(request):
        if 'basket_id' in request.session:
            basket_id = request.session['basket_id']
            try:
                basket = Basket.objects.get(id=basket_id)
                request.basket = basket
            except Basket.DoesNotExist:
                del request.session['basket_id']
                request.basket = None
        else:
            request.basket = None
        response = get_response(request)
        return response
    return middleware
