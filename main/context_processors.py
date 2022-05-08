from django.urls import resolve

def message_processor(request):
    url_name = resolve(request.path_info).url_name

    if url_name == 'dashboard':
        num = 1
    elif url_name == 'registration':
        num = 2
    elif url_name == 'registration_room':
        num = 2
    elif url_name == 'rooms':
        num = 3
    elif url_name == 'room_page':
        num = 3
    elif url_name == 'clients':
        num = 4
    elif url_name == 'payment':
        num = 5
    elif url_name == 'history':
        num = 6
    else:
        num = 0
    return {
        'page_num' : num
    }