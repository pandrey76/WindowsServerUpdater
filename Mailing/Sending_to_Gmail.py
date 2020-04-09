
from email.mime.text import MIMEText
# from datetime import datetime
from GMAIL_PWD import GMAIL_PWD, MAIN_EMAIL, FROM_WHO


import smtplib                                              # Импортируем библиотеку по работе с SMTP
import os                                                   # Функции для работы с операционной системой, не зависящие от используемой операционной системы

# Добавляем необходимые подклассы - MIME-типы
import mimetypes                                            # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders                                  # Импортируем энкодер
from email.mime.base import MIMEBase                        # Общий тип
from email.mime.text import MIMEText                        # Текст/HTML
from email.mime.image import MIMEImage                      # Изображения
from email.mime.audio import MIMEAudio                      # Аудио
from email.mime.multipart import MIMEMultipart              # Многокомпонентный объект


def send_email(addr_to, msg_subj, msg_text, files):
    addr_from = "my_addr@server.ru"                         # Отправитель
    password  = "password"                                  # Пароль

    msg = MIMEMultipart()                                   # Создаем сообщение
    msg['From']    = addr_from                              # Адресат
    msg['To']      = addr_to                                # Получатель
    msg['Subject'] = msg_subj                               # Тема сообщения

    body = msg_text                                         # Текст сообщения
    msg.attach(MIMEText(body, 'plain'))                     # Добавляем в сообщение текст

    process_attachement(msg, files)

    #======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
    server = smtplib.SMTP_SSL('smtp.server.ru', 465)        # Создаем объект SMTP
    #server.starttls()                                      # Начинаем шифрованный обмен по TLS
    #server.set_debuglevel(True)                            # Включаем режим отладки, если не нужен - можно закомментировать
    server.login(addr_from, password)                       # Получаем доступ
    server.send_message(msg)                                # Отправляем сообщение
    server.quit()                                           # Выходим
    #==========================================================================================================================

def process_attachement(msg, files):                        # Функция по обработке списка, добавляемых к сообщению файлов
    for f in files:
        if os.path.isfile(f):                               # Если файл существует
            attach_file(msg,f)                              # Добавляем файл к сообщению
        elif os.path.exists(f):                             # Если путь не файл и существует, значит - папка
            dir = os.listdir(f)                             # Получаем список файлов в папке
            for file in dir:                                # Перебираем все файлы и...
                attach_file(msg,f+"/"+file)                 # ...добавляем каждый файл к сообщению

def attach_file(msg, filepath):                             # Функция по добавлению конкретного файла к сообщению
    filename = os.path.basename(filepath)                   # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)        # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:               # Если тип файла не определяется
        ctype = 'application/octet-stream'                  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)                 # Получаем тип и подтип
    if maintype == 'text':                                  # Если текстовый файл
        with open(filepath) as fp:                          # Открываем файл для чтения
            file = MIMEText(fp.read(), _subtype=subtype)    # Используем тип MIMEText
            fp.close()                                      # После использования файл обязательно нужно закрыть
    elif maintype == 'image':                               # Если изображение
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':                               # Если аудио
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:                                                   # Неизвестный тип файла
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
            file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()
            encoders.encode_base64(file)                    # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки
    msg.attach(file)                                        # Присоединяем файл к сообщению



# Использование функции send_email()
addr_to   = "xxxx@server.ru"                                # Получатель
files = ["file1_path",                                      # Список файлов, если вложений нет, то files=[]
         "file2_path",
         "dir1_path"]                                       # Если нужно отправить все файлы из заданной папки, нужно указать её

send_email(addr_to, "Тема сообщения", "Текст сообщения", files)
class Post:
    """

    """
    def __init__(self):
        """

        """


def send_gmail(post_sender_address,  msg_str):
    msg = MIMEText(msg_str, 'plain')

    msg['Subject'] = FROM_WHO
    msg['From'] = MAIN_EMAIL
    msg['To'] = MAIN_EMAIL

    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.ehlo()  # Extended Hello
    server.starttls()  # Put the SMTP connection in TLS (Transport Layer Security) mode.
    server.ehlo()  # All SMTP comands that follow will be encrypted.
    # server.login('pintchukandrey76@gmail.com', GMAIL_PWD)
    server.login(MAIN_EMAIL, GMAIL_PWD)
    msg["Received:"] = "from Windows 10 Pro ([200.200.200.200])"
    server.sendmail(MAIN_EMAIL, [post_sender_address], msg)
    # server.send_message(msg)

    # server.mail("pinchukandreyurevich76@gmail.com", messages)
    server.close()


# def take_email()
# ===========================================
if __name__ == '__main__':
    #send_gmail("BAN")
    send_gmail("pandrey76@yandex.ru", "LOGOFF")
