import re
import rsa

def get_key(file_name):
    f_r = open(file_name, "r")

    c = f_r.readlines()

    for each_line in c:
        if "PublicKey" in each_line:
            pb_list_str = re.findall('\d+', each_line)
            pb_list = list(map(int, pb_list_str))

        if "PrivateKey" in each_line:
            pr_list_str = re.findall('\d+', each_line)
            pr_list = list(map(int, pr_list_str))


    pbk = rsa.PublicKey(pb_list[0],pb_list[1])
    prk = rsa.PrivateKey(pr_list[0],pr_list[1],pr_list[2],pr_list[3],pr_list[4])

    return [pbk,prk]

# get_key("A.txt")
