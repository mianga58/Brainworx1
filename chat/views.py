from django.shortcuts import render
#from django.http.response import StreamingHttpResponse
#from chat.camera import VideoCamera
from django.core.exceptions import ObjectDoesNotExist
from payment.models import Subscription


def index(request):
    current_plan = ""
    try:
        current_plan = Subscription.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return render(request, 'payment/home.html')
    return render(request, 'chat/home.html', {'current_plan': current_plan})

def forum(request):
    current_plan = ""
    try:
        current_plan = Subscription.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return render(request, 'payment/home.html')
    return render(request, 'chat/forum.html', )

#def gen(camera):
   # while True:
  #      frame = camera.get_frame()
 #       yield (b'--frame\r\n'
#				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


#def video_feed(request):
 #   return StreamingHttpResponse(gen(VideoCamera()),
#		content_type='multipart/x-mixed-replace; boundary=frame')

