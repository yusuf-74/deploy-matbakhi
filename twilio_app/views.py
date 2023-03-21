from django.shortcuts import render
from .openai_api import text_complition
from .twilio_api import send_message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
class Send(APIView):
    def post(self,request):
        data = request.data
        message = data['Body']
        to = data['From']
        response = text_complition(message)
        if response['status'] == 1:
            send_message(to=to, message=response['response'])
        else:
            send_message(request.POST.get('from'), 'I am not able to answer your question right now, please try again later.')
        return Response(data={'status': 1}, status=status.HTTP_200_OK)




