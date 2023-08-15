import os
here = os.path.dirname(os.path.realpath(__file__))
subdir = "user_data"
def get_rolling(uid:float):
    try:
        with open(os.path.join(here, subdir,f"{uid}_rolling"),"r") as uid_file:
            content = uid_file.read()
            rolling = float(content)
            return rolling
    except FileNotFoundError:
        with open(os.path.join(here, subdir,f"{uid}_rolling"),"w") as uid_file:
            uid_file.write("0")
        print("rolling")
        return 0
def write_rolling(uid:float,rolling:float):
    try:
        with open(os.path.join(here, subdir,f"{uid}_rolling"),"w") as uid_file:
            uid_file.write(f"{rolling}")
    except FileNotFoundError:
        with open(os.path.join(here, subdir,f"{uid}_rolling"),"w") as uid_file:
            uid_file.write(f"{rolling}")
        return 0
def get_bet(uid:float):
    try:
        with open(os.path.join(here, subdir,f"{uid}_bet"),"r") as uid_file:
            content = uid_file.read()
            try:
                bet_money = float(content)
                return bet_money
            except ValueError:
                with open(os.path.join(here, subdir,f"{uid}_bet"),"w") as uid_file1:
                    uid_file1.write("0")
                    print("bet")
                    return 0
    except FileNotFoundError:
        with open(os.path.join(here, subdir,f"{uid}_bet"),"w") as uid_file:
            uid_file.write("0")
        print("bet")
        return 0
def write_bet(uid:float,bet_money:float):
    try:
        with open(os.path.join(here, subdir,f"{uid}_bet"),"w") as uid_file:
            uid_file.write(f"{bet_money}")
    except FileNotFoundError:
        with open(os.path.join(here, subdir,f"{uid}_bet"),"w") as uid_file:
            uid_file.write(f"{bet_money}")
        return 0
def add_bet(uid:float,bet_money:float):
    amount = get_bet(uid)
    write_bet(uid,bet_money + amount)
def get_chung(uid:float):
    try:
        with open(os.path.join(here, subdir,f"{uid}_chung"),"r") as uid_file:
            content = uid_file.read()
            try:
                bet_money = float(content)
                return bet_money
            except ValueError:
                with open(os.path.join(here, subdir,f"{uid}_chung"),"w") as uid_file1:
                    uid_file1.write("0")
                    print("bet")
                    return 0
    except FileNotFoundError:
        with open(os.path.join(here, subdir,f"{uid}_chung"),"w") as uid_file:
            uid_file.write("0")
        print("chung")
        return 0
def add_chung1(uid:float,chung:float):
    try:
        with open(os.path.join(here, subdir,f"{uid}_chung"),"w") as uid_file:
            amount = get_chung(uid)
            uid_file.write(f"{amount + chung}")
    except FileNotFoundError:
        with open(os.path.join(here, subdir,f"{uid}_chung"),"w") as uid_file:
            uid_file.write(f"{chung}")
        return 0   
def write_chung(uid:float,chung:float):
    try:
        with open(os.path.join(here, subdir,f"{uid}_chung"),"w") as uid_file:
            uid_file.write(f"{chung}")
    except FileNotFoundError:
        with open(os.path.join(here, subdir,f"{uid}_chung"),"w") as uid_file:
            uid_file.write(f"{chung}")
        return 0
def calculate_rolling(uid:float):
    rolling_per = get_rolling(uid)
    bet_money = get_bet(uid)
    chung_money = get_chung(uid)
    try:
        return [bet_money,bet_money/chung_money*100]
    except ZeroDivisionError:
        return [bet_money,0]

