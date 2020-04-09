import os.path
import importlib.util

from .Mailing.Reading_from_Gmail import Mailing


class Engine:
    """

    """
    def __init__(self, scheduler_seconds_delay):
        """

        """
        self.__Scheduler_Delay = scheduler_seconds_delay

    scheduler_seconds_delay = property(lambda self: self.__Scheduler_Delay)
    """
    """

    @property
    def current_time(self):
        """

        :return:
        """
        return self.__CurrentTime

    @current_time.setter
    def current_time(self, param):
        """

        :param param:
        :return:
        """
        self.__CurrentTime = param

    @property
    def current_user(self):
        """

        :return:
        """
        return self.__CurrentUser

    @current_user.setter
    def current_user(self, param):
        """

        :param param:
        :return:
        """
        self.__CurrentUser = param

    def remove_ban_file(self):
        """

        :return:
        """
        os.remove(self.__ban_file_path)

    def run(self):
        """

        :return:
        """
        user_name = "Ogurchuk"
        mail = self.__reeading_from_gmail.Mailing()
        tp = self.__time_performance.TimePerformance()

        self.current_time = tp.get_utc()
        db = self.__db_performance.DBPerformance(self.__DB_Path)
        # lim_user = self.__limiting_user.LimitingUser(db)

        self.current_user = self.__user.User.get_user(db, user_name)
        if self.current_user is None:
            self.current_user = self.__user.User(
                                        name=user_name,
                                        blocked_state=False,
                                        offline_permission=True,
                                        work_seconds_delay=300,# 7200
                                        start_session_time=self.current_time,
                                        current_time=self.current_time
                                    )
            self.__user.User.create_user(db, self.current_user)
            return
        if self.current_user.blocked_state is False:
            if self.current_user.offline_permission is False:
                if mail.is_online() is False:
                    self.do_ban()

            main_ban_inspector = self.__main_ban_inspector.MainBanInspector(self.current_user, self.current_time)
            if main_ban_inspector.is_triggered():
                self.ban_user()

        mail.read_unseen_mail()
        body = mail.mail_body
        if body is None:
            return
        else:
            if str(body).find("BAN") != -1:
                self.ban_user()
            elif str(body).find("RECOVER") != -1:
                self.recover_user()
            else:
                return

    def do_ban(self):
        """

        :return:
        """
        num = 0
        try:
            with open(self.__ban_file_path, 'rt') as fh:
                num = int(fh.read())
            if num > self.__ban_timeout:
                # limit_user = self.__limiting_user.LimitingUser()
                # limit_user.baning_user("Ogurchuk")
                self.ban_user()
                self.remove_ban_file()
                return
        except IOError:
            with open(self.__ban_file_path, 'wt') as fh:
                fh.write('1')
                return
        num += 1
        with open(self.__ban_file_path, 'wt') as fh:
            fh.write(str(num))
            return

    def ban_user(self):
        """

        :return:
        """
        self.__LimitingUser.baning_user(self.current_user.name)
        self.current_user.start_session_time = self.current_time
        self.current_user.current_time = self.current_time
        self.current_user.blocked_state = True
        db = self.__db_performance.DBPerformance(self.__DB_Path)
        self.__user.User.update_user(db, self.current_user)
        db.close()

    def recover_user(self):
        """

        :return:
        """
        self.__LimitingUser.recover_user(self.current_user.name)
        self.current_user.start_session_time = self.current_time
        self.current_user.current_time = self.current_time
        self.current_user.blocked_state = False
        db = self.__db_performance.DBPerformance(self.__DB_Path)
        self.__user.User.update_user(db, self.current_user)
        db.close()


if __name__ == "__main__":
    limit_user = Engine(60)
    limit_user.run()
