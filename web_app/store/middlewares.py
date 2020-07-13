from .models import Order

def order_middleware(get_response):

    def middleware(request):
        if 'order_id' in request.session:
            order_id = request.session['order_id']
            try:
                order = Order.objects.get(id=order_id)
                request.order = order
            except Order.DoesNotExist:
                del request.session['order_id']
                request.order = None
        else:
            request.order = None
        response = get_response(request)
        return response
    return middleware
