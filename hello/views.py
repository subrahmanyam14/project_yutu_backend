from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from translate import Translator

@csrf_exempt  # Allows POST requests without CSRF token for simplicity (remove in production if CSRF protection is required)
def translate_text(request):
    if request.method == 'POST':
        try:
            # Decode JSON data from request body
            data = json.loads(request.body)
            texts = data.get('texts')  # Get the array of texts from the JSON body
            target_language = data.get('target_language')  # Get the target language from the JSON body

            if not texts or not target_language:
                return JsonResponse({"error": "Invalid data"}, status=400)

            # Function to handle the translation
            def translate_individual_text(text, target_language):
                translator = Translator(to_lang=target_language)
                return translator.translate(text)

            # Translate each text in the array
            translated_texts = [translate_individual_text(text, target_language) for text in texts]

            # Return translated text as JSON
            return JsonResponse({"translated_texts": translated_texts}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST method required"}, status=405)

