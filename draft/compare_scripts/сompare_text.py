# from itertools import zip_longest
#
# # Превратим файлы в список строк, убрав символы \n в конце строки
# l1 = map(lambda x: x.strip(), list(open('test1.txt')))
# l2 = map(lambda x: x.strip(), list(open('test2.txt')))
#
# # превратим два списка в один, где каждый елемент первого соответсвует елементу второго.
# # Если в одном из спсиков нет соответсвующей строки - будет None
# diff_list = zip_longest(l1, l2)
#
# for diff in diff_list:
#     print(
#     '%s %s %s' % (
#         diff[0] or '',
#         '==' if diff[0] == diff[1] else '!=',
#         diff[1] or '',
#     ))
#



# with open("compare_image.py", "rb") as file:
#     content: bytes = file.read()
#
# binary: str = "".join(map("{:08b}".format, content))
# print(binary)


file1 = r"test1.txt"
file2 = r"test2.txt"

with open(file1, 'br') as of1, open(file2, 'br') as of2:
    l1 = of1.read()
    l2 = of2.read()
    print(len(set(enumerate(l1))))
    f1_f2 = set(enumerate(l1)) - set(enumerate(l2))
    f2_f1 = set(enumerate(l2)) - set(enumerate(l1))

    for offset, char in sorted(f1_f2, key=lambda x: x[0]):
        print("offset: {}\tchar: {:X}".format(offset, char))

    print()

    for offset, char in sorted(f2_f1, key=lambda x: x[0]):
        print("offset: {}\tchar: {:X}".format(offset, char))
