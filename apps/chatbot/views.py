from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatMessage
from .groq_utils import process_message

class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_message = request.data.get('message')
        if not user_message:
            return Response({"error": "Message required"}, status=400)

        # Save user message
        ChatMessage.objects.create(user=request.user, message=user_message, is_user_message=True)

        # Process with AI
        bot_response = process_message(request.user, user_message)

        # Save bot response
        ChatMessage.objects.create(user=request.user, message=bot_response, is_user_message=False)

        return Response({"response": bot_response})
