from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode
import speech_recognition as sr
import os
import uuid
from io import BytesIO
from pytube import YouTube
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, vfx
import shutil
from moviepy.editor import TextClip

# Токен вашего телеграм-бота
TOKEN = "6673045880:AAFyEN4jHRjqETu1yIY3HimwXfFIORA5xjE"

# Создание объекта Updater и использование контекста
updater = Updater(token=TOKEN, use_context=True)

user_defined_words = {
    'after': 'c:/Users/dell/Downloads/After.mp4',
    'again': 'c:/Users/dell/Downloads/Again.mp4',
    'against': 'c:/Users/dell/Downloads/Against.mp4',
    'age': 'c:/Users/dell/Downloads/Age.mp4',
    'all': 'c:/Users/dell/Downloads/All.mp4',
    'alone': 'c:/Users/dell/Downloads/Alone.mp4',
    'also': 'c:/Users/dell/Downloads/Also.mp4',
    'and': 'c:/Users/dell/Downloads/And.mp4',
    'ask': 'c:/Users/dell/Downloads/Ask.mp4',
    'at': 'c:/Users/dell/Downloads/At.mp4',
    'be': 'c:/Users/dell/Downloads/Be.mp4',
    'beautiful': 'c:/Users/dell/Downloads/Beautiful.mp4',
    'before': 'c:/Users/dell/Downloads/Before.mp4',
    'best': 'c:/Users/dell/Downloads/Best.mp4',
    'better': 'c:/Users/dell/Downloads/Better.mp4',
    'busy': 'c:/Users/dell/Downloads/Busy.mp4',
    'but': 'c:/Users/dell/Downloads/But.mp4',
    'bye': 'c:/Users/dell/Downloads/Bye.mp4',
    'can': 'c:/Users/dell/Downloads/Can.mp4',
    'cannot': 'c:/Users/dell/Downloads/Cannot.mp4',
    'change': 'c:/Users/dell/Downloads/Change.mp4',
    'college': 'c:/Users/dell/Downloads/College.mp4',
    'come': 'c:/Users/dell/Downloads/Come.mp4',
    'computer': 'c:/Users/dell/Downloads/Computer.mp4',
    'day': 'c:/Users/dell/Downloads/Day.mp4',
    'distance': 'c:/Users/dell/Downloads/Distance.mp4',
    'do': 'c:/Users/dell/Downloads/Do.mp4',
    'eat': 'c:/Users/dell/Downloads/Eat.mp4',
    'engineer': 'c:/Users/dell/Downloads/Engineer.mp4',
    'fight': 'c:/Users/dell/Downloads/Fight.mp4',
    'finish': 'c:/Users/dell/Downloads/Finish.mp4',
    'from': 'c:/Users/dell/Downloads/From.mp4',
    'glitter': 'c:/Users/dell/Downloads/Glitter.mp4',
    'go': 'c:/Users/dell/Downloads/Go.mp4',
    'god': 'c:/Users/dell/Downloads/God.mp4',
    'gold': 'c:/Users/dell/Downloads/Gold.mp4',
    'good': 'c:/Users/dell/Downloads/Good.mp4',
    'great': 'c:/Users/dell/Downloads/Great.mp4',
    'hand': 'c:/Users/dell/Downloads/Hand.mp4',
    'hands': 'c:/Users/dell/Downloads/Hands.mp4',
    'happy': 'c:/Users/dell/Downloads/Happy.mp4',
    'hello': 'c:/Users/dell/Downloads/Hello.mp4',
    'help': 'c:/Users/dell/Downloads/Help.mp4',
    'her': 'c:/Users/dell/Downloads/Her.mp4',
    'here': 'c:/Users/dell/Downloads/Here.mp4',
    'his': 'c:/Users/dell/Downloads/His.mp4',
    'home': 'c:/Users/dell/Downloads/Home.mp4',
    'homepage': 'c:/Users/dell/Downloads/Homepage.mp4',
    'how': 'c:/Users/dell/Downloads/How.mp4',
    'invent': 'c:/Users/dell/Downloads/Invent.mp4',
    'it': 'c:/Users/dell/Downloads/It.mp4',
    'keep': 'c:/Users/dell/Downloads/Keep.mp4',
    'language': 'c:/Users/dell/Downloads/Language.mp4',
    'laugh': 'c:/Users/dell/Downloads/Laugh.mp4',
    'learn': 'c:/Users/dell/Downloads/Learn.mp4',
    'me': 'c:/Users/dell/Downloads/ME.mp4',
    'more': 'c:/Users/dell/Downloads/More.mp4',
    'my': 'c:/Users/dell/Downloads/My.mp4',
    'name': 'c:/Users/dell/Downloads/Name.mp4',
    'next': 'c:/Users/dell/Downloads/Next.mp4',
    'not': 'c:/Users/dell/Downloads/Not.mp4',
    'now': 'c:/Users/dell/Downloads/Now.mp4',
    'of': 'c:/Users/dell/Downloads/Of.mp4',
    'on': 'c:/Users/dell/Downloads/On.mp4',
    'our': 'c:/Users/dell/Downloads/Our.mp4',
    'out': 'c:/Users/dell/Downloads/Out.mp4',
    'pretty': 'c:/Users/dell/Downloads/Pretty.mp4',
    'right': 'c:/Users/dell/Downloads/Right.mp4',
    'sad': 'c:/Users/dell/Downloads/Sad.mp4',
    'safe': 'c:/Users/dell/Downloads/Safe.mp4',
    'see': 'c:/Users/dell/Downloads/See.mp4',
    'self': 'c:/Users/dell/Downloads/Self.mp4',
    'sign': 'c:/Users/dell/Downloads/Sign.mp4',
    'sing': 'c:/Users/dell/Downloads/Sing.mp4',
    'so': 'c:/Users/dell/Downloads/So.mp4',
    'sound': 'c:/Users/dell/Downloads/Sound.mp4',
    'study': 'c:/Users/dell/Downloads/Study.mp4',
    'stay': 'c:/Users/dell/Downloads/Stay.mp4',
    'talk': 'c:/Users/dell/Downloads/Talk.mp4',
    'television': 'c:/Users/dell/Downloads/Television.mp4',
    'thank': 'c:/Users/dell/Downloads/Thank.mp4',
    'that': 'c:/Users/dell/Downloads/That.mp4',
    'they': 'c:/Users/dell/Downloads/They.mp4',
    'this': 'c:/Users/dell/Downloads/This.mp4',
    'those': 'c:/Users/dell/Downloads/Those.mp4',
    'time': 'c:/Users/dell/Downloads/Time.mp4',
    'to': 'c:/Users/dell/Downloads/To.mp4',
    'type': 'c:/Users/dell/Downloads/Type.mp4',
    'us': 'c:/Users/dell/Downloads/Us.mp4',
    'walk': 'c:/Users/dell/Downloads/Walk.mp4',
    'wash': 'c:/Users/dell/Downloads/Wash.mp4',
    'way': 'c:/Users/dell/Downloads/Way.mp4',
    'we': 'c:/Users/dell/Downloads/We.mp4',
    'welcome': 'c:/Users/dell/Downloads/Welcome.mp4',
    'what': 'c:/Users/dell/Downloads/What.mp4',
    'when': 'c:/Users/dell/Downloads/When.mp4',
    'where': 'c:/Users/dell/Downloads/Where.mp4',
    'which': 'c:/Users/dell/Downloads/Which.mp4',
    'who': 'c:/Users/dell/Downloads/Who.mp4',
    'whole': 'c:/Users/dell/Downloads/Whole.mp4',
    'whose': 'c:/Users/dell/Downloads/Whose.mp4',
    'why': 'c:/Users/dell/Downloads/Why.mp4',
    'will': 'c:/Users/dell/Downloads/Will.mp4',
    'with': 'c:/Users/dell/Downloads/With.mp4',
    'without': 'c:/Users/dell/Downloads/Without.mp4',
    'words': 'c:/Users/dell/Downloads/Words.mp4',
    'work': 'c:/Users/dell/Downloads/Work.mp4',
    'world': 'c:/Users/dell/Downloads/World.mp4',
    'wrong': 'c:/Users/dell/Downloads/Wrong.mp4',
    'you': 'c:/Users/dell/Downloads/You.mp4',
    'your': 'c:/Users/dell/Downloads/Your.mp4',
    'yourself': 'c:/Users/dell/Downloads/Yourself.mp4',
    # Добавьте свои слова и соответствующие видео
}

# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Send me a link to a YouTube video to convert to WAV format.")

def add_subtitles_to_video(original_video_path, text, output_dir, subtitle_speed=1.5, fps=24):
     try:
        # Load the original video
        original_clip = VideoFileClip(original_video_path)

        # Split the text into lists of 5 words
        words = text.split()
        chunks_of_5_words = [words[i:i + 5] for i in range(0, len(words), 5)]

        # Initialize a list to store paths to temporary video clips
        temp_video_clips = []

        # Create temporary video clips for each list of words
        for i, chunk in enumerate(chunks_of_5_words):
            temp_text = ' '.join(chunk)
            temp_video_clip = create_temp_video(original_clip.size, temp_text, output_dir, f"temp_video_{i}", fps)
            temp_video_clips.append(temp_video_clip)

        # Concatenate the subtitle clips
        subtitles_clip = concatenate_videoclips(temp_video_clips, method="compose")

        # Set the fps of the subtitles clip to be the same as the original video
        subtitles_clip = subtitles_clip.set_fps(fps)

        # Adjust the speed of the subtitles clip
        subtitles_clip = subtitles_clip.fx(vfx.speedx, subtitle_speed)

        # Overlay the subtitles on the original video
        final_clip = CompositeVideoClip([original_clip.set_duration(subtitles_clip.duration), subtitles_clip])

        # Set the fps of the final clip
        final_clip.fps = fps

        # Create a unique name for the output video file
        filename = f"output_video_{uuid.uuid4()}.mp4"
        final_video_path = os.path.join(output_dir, filename)

        # Write the final video file
        final_clip.write_videofile(final_video_path, codec='libx264', audio=False, fps=fps, remove_temp=True)

        return final_video_path

     except Exception as e:
        print(f"Error adding subtitles to video: {str(e)}")
        raise

def create_temp_video(video_size, text, output_dir, filename, fps):
    temp_video_path = os.path.join(output_dir, f"{filename}.mp4")

    # Создаем текстовый слой (субтитры) для каждого списка слов
    txt_clip = TextClip(text, fontsize=15, color='black', size=(video_size[0], 80))
    txt_clip = txt_clip.set_pos(('center', 'bottom')).set_duration(5)  # Устанавливаем длительность 5 секунд

    # Создаем видеоклип с текстовым слоем
    video_clip = CompositeVideoClip([txt_clip], size=video_size)

    # Записываем временный видеофайл
    video_clip.write_videofile(temp_video_path, codec='libx264', audio=False, fps=fps)

    return video_clip  # Return the video clip instead of the file path

# Обработчик текстовых сообщений
def process_video(update: Update, context: CallbackContext) -> None:
    try:
        youtube_url = update.message.text

        # Сообщение о начале обработки
        update.message.reply_text("Please be a little patient, text and video are being processed...")

        # Создаем временную директорию для сохранения видеофайла
        temp_video_dir = os.path.join(os.getcwd(), 'temp_video')
        os.makedirs(temp_video_dir, exist_ok=True)

        # Создаем временную директорию для сохранения изображений
        temp_images_dir = os.path.join(os.getcwd(), 'temp_images')
        os.makedirs(temp_images_dir, exist_ok=True)

        # Загружаем, конвертируем в WAV и сохраняем аудиофайл в буфер BytesIO
        output_buffer = BytesIO()
        download_and_convert(youtube_url, output_buffer, temp_video_dir)

        # Переводим позицию указателя в начало буфера для чтения
        output_buffer.seek(0)

        # Обрабатываем аудио
        result = audio_to_text(output_buffer)
        result = result.replace(',', ' ').replace("'", ' ')
        print("#" * 10)
        print(result)

        # Отправляем текст
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Recognized text: {result}")

        # Создаем оригинальное видео и видео с языком жестов
        original_video_path = download_original_video(youtube_url, temp_video_dir)
        sign_language_video_paths = []

        for word in result.lower().split():
            # Попробуем получить видео для слова из пользовательских слов
            word_video = user_defined_words.get(word)

            if not word_video:
                # Если видео для слова не найдено, пропускаем это слово
                continue

            # Видео для слова найдено в пользовательских словах
            print("@" * 20)
            print(word)
            sign_language_video_paths.append(create_video_from_mp4(word_video, temp_video_dir))

        final_video_path = create_video_from_videos(original_video_path, sign_language_video_paths, temp_video_dir)

        # Добавить субтитры к видео с языком жестов
        result_text = " ".join(result.lower().split())  # Правильное форматирование текста
        final_video_path_with_subtitles = add_subtitles_to_video(final_video_path, result_text, temp_video_dir)

        # Отправляем видео с субтитрами
        with open(final_video_path_with_subtitles, 'rb') as video_file:
            context.bot.send_video(chat_id=update.effective_chat.id, video=video_file, caption="")

        update.message.reply_text("Thank you for using our bot and being patient, have a nice day!")

    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {str(e)}")
    finally:
        # Удаляем временные директории и файлы
        if os.path.exists(temp_video_dir):
            shutil.rmtree(temp_video_dir)
        if os.path.exists(temp_images_dir):
            shutil.rmtree(temp_images_dir)

# Функция для создания видео из нескольких видеофайлов
def create_video_from_videos(original_video_path, sign_language_video_paths, output_dir):
    final_video_path = os.path.join(output_dir, "output_video.mp4")

    # Load the original video
    original_clip = VideoFileClip(original_video_path)

    # Load sign language videos and resize them to fit a corner of the original video
    sign_language_clips = []
    for sign_language_path in sign_language_video_paths:
        sign_language_clip = VideoFileClip(sign_language_path)
        sign_language_clip = sign_language_clip.resize(height=100)
        sign_language_clip = sign_language_clip.fx(vfx.speedx, 3)  # Ускоряем видео со скоростью 2
        sign_language_clips.append(sign_language_clip)

    # Calculate the total duration of sign language videos
    total_duration = sum(clip.duration for clip in sign_language_clips)

    # Concatenate sign language videos
    concatenated_clips = concatenate_videoclips(sign_language_clips, method="compose")

    # Set the duration of the concatenated clips to match the original video
    concatenated_clips = concatenated_clips.set_duration(total_duration)

    # Position sign language video in the bottom right corner
    w, h = original_clip.size
    w_sign, h_sign = concatenated_clips.size
    position = (w - w_sign, h - h_sign)

    # Create a CompositeVideoClip with the original video and concatenated sign language videos
    final_clip = CompositeVideoClip([original_clip.set_position('center'), concatenated_clips.set_position(position)],
                                    size=original_clip.size)

    # Write the final video file
    final_clip.write_videofile(final_video_path, codec='libx264', audio=False)

    return final_video_path

# Функция для создания видео из MP4 файла
def create_video_from_mp4(mp4_path, output_dir, speed=0.9):
    video_clip = VideoFileClip(mp4_path)
    video_clip = video_clip.fx(vfx.speedx, speed)
    
    video_path = os.path.join(output_dir, f"{uuid.uuid4()}.mp4")
    video_clip.write_videofile(video_path, codec='libx264', audio=False, threads=4)
    
    return video_path

# Функция для загрузки оригинального видео с YouTube
def download_original_video(youtube_url, output_dir):
    try:
        # Загружаем видео с YouTube
        yt = YouTube(youtube_url)
        video_stream = yt.streams.filter(file_extension='mp4').first()

        # Загружаем видео
        original_video_path = os.path.join(output_dir, f"original_video_{uuid.uuid4()}.mp4")
        video_stream.download(output_path=output_dir, filename=os.path.basename(original_video_path))

        return original_video_path

    except Exception as e:
        print(f"Error downloading original video: {str(e)}")
        raise

# Функция для загрузки и конвертации видео в аудиоформат
def download_and_convert(youtube_url, output_buffer, temp_video_dir):
    video_path = None
    try:
        # Загружаем видео с YouTube
        yt = YouTube(youtube_url)
        video_stream = yt.streams.filter(only_audio=True).first()

        # Загружаем видео
        video_path = os.path.join(temp_video_dir, f"{uuid.uuid4()}.mp4")
        video_stream.download(output_path=temp_video_dir, filename=os.path.basename(video_path))

        # Конвертируем видео в аудио с использованием pydub
        audio = AudioSegment.from_file(video_path)
        audio = audio.set_frame_rate(16000)  # Устанавливаем частоту кадров в 16000 Гц
        audio = audio.set_channels(1)  # Устанавливаем моно-канал

        # Экспортируем аудио в WAV
        audio.export(output_buffer, format='wav', codec='pcm_s16le')  # Указываем кодек

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Удаляем временные файлы
        if video_path and os.path.exists(video_path):
            os.remove(video_path)

# Функция для преобразования аудио в текст с использованием Google Speech Recognition
def audio_to_text(audio_buffer):
    recognizer = sr.Recognizer()

    # Получаем аудиоданные из буфера BytesIO
    audio_data = AudioSegment.from_file(audio_buffer, format='wav')
    audio_data = audio_data.set_channels(1)  # Устанавливаем моно-канал
    audio_data = audio_data.set_sample_width(2)  # Устанавливаем 16-битную глубину дискретизации

    # Сохраняем временный файл WAV
    temp_wav_path = 'temp_audio.wav'
    audio_data.export(temp_wav_path, format='wav', codec='pcm_s16le')  # Указываем кодек

    with sr.AudioFile(temp_wav_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language='en-US')
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition couldn't recognize the audio."
    except sr.RequestError as e:
        return f"Error contacting Google Speech Recognition service: {e}"
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)

# Функция main для запуска бота
def main() -> None:
    dp = updater.dispatcher

    # Добавляем обработчики
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process_video))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
