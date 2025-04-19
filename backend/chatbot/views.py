from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class AutoReplyAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        message = request.data.get("message", "").lower()
        replies = {
            "hi": "Hello! How can I help you today?",
            "price": "Our prices start from ₹100. Contact us for more info.",
            "open": "We're open 9 AM to 9 PM every day.",
        }
        for keyword in replies:
            if keyword in message:
                return Response({"reply": replies[keyword]})
        return Response({"reply": "Sorry, I didn't understand that."})
