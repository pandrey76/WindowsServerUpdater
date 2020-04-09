import os
import codecs

#from chardet.universaldetector import UniversalDetector


class RunPowerShellScript:
    """

    """

    def __init__(self):
        """

        """
        self.__PowerShell = "powershell.exe"

    def run_script(self, full_script_path):
        """

        :param full_script_path:
        :return:
        """
        space = ' '
        run_string = self.__PowerShell
        run_string += space

        run_string += '"'

        run_string += full_script_path

        run_string += '"'

        os.system(run_string)


if __name__ == "__main__":
    run_script = RunPowerShellScript()
    run_script.run_script("..//PS//RecoverUserFromBan.ps1")
    #run_script.run_script("..//PS//BanUser.ps1")
    run_script.run_script("..//PS//LogoffUser.ps1")

    #print(os.path.expanduser(os.getenv('USERPROFILE')))
    #print(get_calculater_appid())
