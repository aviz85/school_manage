from .models import Message

def unread_messages_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_messages_count': count}
    return {'unread_messages_count': 0}