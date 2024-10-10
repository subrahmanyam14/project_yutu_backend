from django.http import JsonResponse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from translate import Translator
from gtts import gTTS
import os


@csrf_exempt 
def translate_text(request):
    if request.method == 'POST':
        try:
           
            data = json.loads(request.body)
            texts = data.get('texts')  
            target_language = data.get('target_language')  

            if not texts or not target_language:
                return JsonResponse({"error": "Invalid data"}, status=400)

            
            def translate_individual_text(text, target_language):
                translator = Translator(to_lang=target_language)
                return translator.translate(text)

            
            translated_texts = [translate_individual_text(text, target_language) for text in texts]

           
            return JsonResponse({"translated_texts": translated_texts}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST method required"}, status=405)




@csrf_exempt
def generate_speech(request):
    if request.method == 'POST':
        try:
           
            data = json.loads(request.body)
            text = data.get('text')  
            language = data.get('language')  

            if not text or not language:
                return JsonResponse({"error": "Text and language are required"}, status=400)

            
            tts = gTTS(text=text, lang=language)
            audio_file = "translated_speech.mp3"

           
            file_path = os.path.join("D:\Robot\myproject\hello", audio_file)  
            tts.save(file_path)

            
            with open(file_path, "rb") as f:
                file_data = f.read()

            
            response = HttpResponse(file_data, content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{audio_file}"'

            return response

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST method required"}, status=405)



@csrf_exempt
def hello(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Hello, Django!"}, status=200)
    else:
        return JsonResponse({"error": "GET method required"}, status=405)
