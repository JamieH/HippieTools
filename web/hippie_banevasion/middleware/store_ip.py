from ..utils import utils


# Store the IP in the DB for every client hitting us
def store_ip(get_response):
    def middleware(request):
        ip_obj = utils.store_ipaddress(utils.get_client_ip(request))
        request.ip_obj = ip_obj
        response = get_response(request)
        return response

    return middleware
