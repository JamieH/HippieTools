def user_player(request):
    if request.current_player is not None:
        return {'current_player': request.current_player}
    return {}
