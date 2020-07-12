from .models import Order

def order_middleware(get_response):

    def middleware(request):
        if 'order_id' in request.session:
            order_id = request.session['order_id']
            order = Order.objects.get(id=order_id)
            request.order = order
        else:
            request.order = None
        response = get_response(request)
        return response
    return middleware
