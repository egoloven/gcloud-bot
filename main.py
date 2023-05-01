import telebot
from google.cloud import vision
from google.oauth2 import service_account

# Replace these with your own values
TELEGRAM_TOKEN = ''
GOOGLE_CREDENTIALS_FILE = ''

# Set up the telebot and Google Cloud Vision clients
bot = telebot.TeleBot(TELEGRAM_TOKEN)
credentials = service_account.Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE)
vision_client = vision.ImageAnnotatorClient(credentials=credentials)

def get_image_text(image_content):
    image = vision.Image(content=image_content)
    response = vision_client.text_detection(image=image)
    return response.full_text_annotation.text

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello! Send me a picture, and I will extract the text from it.')

@bot.message_handler(content_types=['photo'])
def photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    image_content = bot.download_file(file_info.file_path)

    text = get_image_text(image_content)
    if text.strip():
        bot.reply_to(message, f'Text found in image:\n{text}')
    else:
        bot.reply_to(message, 'No text detected in the image.')

if __name__ == '__main__':
    bot.polling()
