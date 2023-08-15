def roulette_image(number):
    if number == 36:
        return "1026379148274446407/30_.png"
    elif number == 8:
        return "1026379684063215706/35_.png"
    elif number == 0:
        return "1026367323667439676/0_.png"
    elif number == 1:
        return "1026367604371226664/1_.png"
    elif number == 2:
        return "1026370361547305020/12_.png"
    elif number == 3:
        return "1026378064084607027/23_.png"
    elif number == 4:
        return "1026379266100838430/31_.png"
    elif number == 5:
        return "1026379386422820944/32_.png"
    elif number == 6:
        return "1026379484150116362/33_.png"
    elif number == 7:
        return "1026379580715569203/34_.png"
    elif number == 17:
        return "1026369826211516506/9_.png"
    elif number == 9:
        return "1026379776023339008/36_.png"
    elif number == 10:
        return "1026367815294398564/2_.png"
    elif number == 11:
        return "1026368108962791484/3_.png"
    elif number == 12:
        return "1026368494452875274/4_.png"
    elif number == 13:
        return "1026368591542636634/5_.png"
    elif number == 14:
        return "1026368591542636634/6_.png"
    elif number == 15:
        return "1026369480399528036/IMG_6841.jpg"
    elif number == 16:
        return "1026369658384809994/8_.png"
    elif number == 26:
        return "1026377579978039316/19_.png"
    elif number == 18:
        return "1026369952359391272/10_.png"
    elif number == 19:
        return "1026370184216322168/image.png"
    elif number == 20:
        return "1026370500538138654/13_.png"
    elif number == 21:
        return "1026376950681436201/14_.png"
    elif number == 22:
        return "1026377102431375390/15_.png"
    elif number == 23:
        return "1026377228021399572/16_.png"
    elif number == 24:
        return "1026377357361156147/17_.png"
    elif number == 25:
        return "1026377460620742716/18_.png"
    elif number == 28:
        return "1026377815655993344/21_.png"
    elif number == 29:
        return "1026377966512517150/22_.png"
    elif number == 30:
        return "1026378173413335122/24_.png"
    elif number == 31:
        return "1026378339314843728/25_.png"
    elif number == 32:
        return "1026378565203284099/IMG_6844.jpg"
    elif number == 33:
        return "1026378733701042176/27_.png"
    elif number == 34:
        return "1026378877574058075/28_.png"
    elif number == 35:
        return "1026379038111047710/29_.png"
    elif number == 27:
        return "1026377699125628998/20_.png"

def roulette_color(number):
    red = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]

    if number == 0:
        return "green"
    elif number in red:
        return "red"
    elif not number in red and number != 0:
        return "black"
