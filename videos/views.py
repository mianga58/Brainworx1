from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Video
from payment.models import Subscription
from .services import open_file

# Create your views here.
from django.core.exceptions import ObjectDoesNotExist


@login_required(login_url='/signin')
def index(request):
    current_plan = ""
    try:
        current_plan = Subscription.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return render(request, 'payment/home.html')
    #except Subscription.DoesNotExist:
     #   current_plan = None
    #try:
     #   enddate = current_plan.reg_date + timedelta(days=current_plan.plan.validity_days)
    #except ObjectDoesNotExist:
      #  redirect("payment:price")
    video = Video.objects.all()


    return render(request, 'videos/index_vid.html',{'current_plan':current_plan,  'video_list': video})

#def get_list_video(request):
    #return render(request, 'videos/home.html', {'video_list': Video.objects.all()})

@login_required(login_url='/signin')
def get_video(request, pk: int):
    _video = get_object_or_404(Video, id=pk)
    return render(request, "videos/video.html", {"video": _video})

@login_required(login_url='/signin')
def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response
