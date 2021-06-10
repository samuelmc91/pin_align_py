import os
import re
import pin_align_config_amx
root = os.getcwd()
config_file_path = os.path.join(root, 'pin_align_config_amx.py')

def change_config_file(config_file_path, line_text, new_value):
    lines = open(config_file_path, 'r').readlines()
    line_num = [num for num, f in enumerate(lines, 0) if re.findall(line_text, f)][0]
    lines[line_num] = line_text + ' = ' + str(new_value) + '\n'
    out = open(config_file_path, 'w')
    out.writelines(lines)
    out.close()

print(pin_align_config_amx.DEFAULT_ROI_Y1)
pin_align_config_amx.DEFAULT_ROI_Y2.replace(634)