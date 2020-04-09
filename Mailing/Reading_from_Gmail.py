import imaplib
import email

import base64
import os
import importlib.util

import socket

from .GMAIL_PWD import MAIN_EMAIL, GMAIL_PWD, FROM_WHO
#MAIN_EMAIL = "pinchukandreyurevich76@gmail.com"
#GMAIL_PWD = ""
#FROM_WHO = "Prapor"


class Mailing:
    def __init__(self):
        """

        """
        self.__Body = None

    mail_body = property(lambda self: self.__Body)
    """
    """

    def read_unseen_mail(self):
        """

        :return:
        """
        host = "imap.gmail.com"
        port = 993
        user = MAIN_EMAIL
        password = GMAIL_PWD
        sender = MAIN_EMAIL

        connection = imaplib.IMAP4_SSL(host=host, port=port)
        connection.login(user=user, password=password)

        status, msgs = connection.select('INBOX')
        assert status == 'OK'

        typ, data = connection.search(None, '(UNSEEN)') # , 'FROM', '"%s"' % sender)
        try:
            for num in data[0].split():
                typ, message_data = connection.fetch(num, '(RFC822)')
                mail = email.message_from_bytes(message_data[0][1])
                for part in mail.walk():
                    self.__Body = part.get_payload(decode=True)
        finally:
            try:
                connection.close()
            except:
                pass
            connection.logout()


def read_gmail():
    host = "imap.gmail.com"
    port = 993
    user = MAIN_EMAIL
    password = GMAIL_PWD
    sender = MAIN_EMAIL

    connection = imaplib.IMAP4_SSL(host=host, port=port)
    connection.login(user=user, password=password)

    status, msgs = connection.select('INBOX')
    assert status == 'OK'

    typ, data = connection.search(None, '(UNSEEN)', 'FROM', '"%s"' % sender)
    body = ''
    try:
        print(data)
        for num in data[0].split():
            typ, message_data = connection.fetch(num, '(RFC822)')
            # print(data)
            print('Message %s\n%s\n' % (num, message_data[0][1]))
            mail = email.message_from_bytes(message_data[0][1])
            print("Mail" ,mail)
            for part in mail.walk():
                content_type = part.get_content_type()
                print(content_type)
                play_load = part.get_payload()
                print(play_load)
                print(part["Date"])
                print(part["Subject"])
                print(part["From"])
                print(part["To"])
                print(part["Content-Transfer-Encoding"])    #base64
                print(part["Received"])
                filename = part.get_filename()
                if filename:
                    print(filename)
                    # Нам плохого не надо, в письме может быть всякое барахло
                    with open(part.get_filename(), 'wb') as new_file:
                        new_file.write(part.get_payload(decode=True))

                # Первый способ декодтроавания тела сообщения
                if part["Content-Transfer-Encoding"] == "base64":
                    print("Variant 1:   ", base64.b64decode(play_load).decode("UTF-8"))

                # Второй способ декодирования ела сообщения (Более правильный)
                body = part.get_payload(decode=True)
                print("Variant 2:   ", part.get_payload(decode=True))

                # with open(str(num), 'wb') as new_file:
                #    new_file.write(part.get_payload(decode=True))

    finally:
        try:
            connection.close()
        except:
            pass
        connection.logout()
        return body


if __name__ == '__main__':

    mail = Mailing()
    flag = mail.is_online()
    print(flag)
    #mail.read_unseen_mail()
    #body = mail.mail_body
    #print(body)
