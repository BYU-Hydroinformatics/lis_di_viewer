import os


def get_di_dates(dir):

    dir = os.path.join(dir,"")

    dates = []
    for file in sorted(os.listdir(dir)):
        date = file.split('.')[0]
        dates.append(date)

    return dates