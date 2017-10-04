def user_player(request):
    if hasattr(request, 'current_player'):
        return {'current_player': request.current_player}
    return {}
