import os

IND = "--"

IGN = [".png", ".txt"]

def show_dir(dir, level):

    ctr = 0

    for f in os.listdir(dir):
        if f[-4:] not in IGN: print(level*IND+f)

        if os.path.isfile(dir+"/"+f) == False:
            ctr += show_dir(dir+"/"+f, level + 1)
        else:
            ctr += 1

    print(f"{level * IND}] TOTAL: {str(ctr)}\n")
    return ctr

if __name__ == "__main__":
    show_dir(".", 0)