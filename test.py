import googletrans
from googletrans import Translator
 
# print(googletrans.LANGUAGES)
 
text1 = input()
 
 
translator = Translator()
 
print(translator.detect(text1))

 
trans1 = translator.translate(text1, src='en', dest='ja')

 
print("English to Japanese: ", trans1.text)
