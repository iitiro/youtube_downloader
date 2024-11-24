import os
import subprocess

# Шлях до файлу з URL відео
url_file = 'video.txt'  # Назва файлу з URL
output_folder = '!video_downloader'  # Папка для збереження відео

# Перевірка наявності файлу з URL
if not os.path.exists(url_file):
    print(f"Файл {url_file} не знайдено.")
    exit()

# Перевірка наявності папки для збереження відео, якщо її немає - створюємо
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Запит користувача щодо формату
format_choice = input("Оберіть формат для збереження: 'avi' для відео або 'mp3' для аудіо: ").strip().lower()

# Перевірка вибору формату
if format_choice == 'avi':
    output_format = 'avi'
    command_template = f"yt-dlp -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best -o '{output_folder}/%(title)s.%(ext)s' --merge-output-format avi -a {url_file}"
elif format_choice == 'mp3':
    output_format = 'mp3'
    command_template = f"yt-dlp -x --audio-format mp3 -o '{output_folder}/%(title)s.%(ext)s' -a {url_file}"
else:
    print("Неправильний вибір. Спробуйте ще раз.")
    exit()

# Запуск команди для завантаження відео або аудіо
print(f"Завантаження відео у форматі {output_format}...")
subprocess.run(command_template, shell=True)
print("Завантаження завершено!")

# Питання про конвертацію у формат mov
convert_to_mov = input("Чи потрібно конвертувати файли у формат .mov? (y/n): ").strip().lower()

if convert_to_mov == 'y':
    # Проходимо по всіх файлах у папці і конвертуємо їх у формат mov
    for file_name in os.listdir(output_folder):
        if file_name.endswith(f".{output_format}"):  # Перевіряємо розширення файлу
            input_file = os.path.join(output_folder, file_name)
            output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + ".mov")

            # Використання ffmpeg для конвертації у формат .mov
            convert_command = f"ffmpeg -i '{input_file}' -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 128k '{output_file}'"
            print(f"Конвертація {file_name} у формат .mov...")
            subprocess.run(convert_command, shell=True)
            print(f"Файл {output_file} збережено.")

print("Усі завдання виконано!")