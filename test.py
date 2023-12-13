
import os

print(len(os.listdir('G:/programms/Loginov_check_file/first_programm/folder_with_files')))
print(len(os.listdir('G:/programms/Loginov_check_file/first_programm/folder_for_diode')))

if os.listdir('G:/programms/Loginov_check_file/first_programm/folder_with_files'):
    print('hello')