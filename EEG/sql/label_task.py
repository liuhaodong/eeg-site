import csv
import sys
from datetime import datetime
from datetime import timedelta

# python label_task.py . positive

data_path = sys.argv[1]
label = sys.argv[2]

header = ['machine', 'subject', 'stim', 'block', 'start_time', 'end_time', 'cond', 'rooting', 'possessing', 'attacking', 'goaling', 'winning', 'counterattack', 'goal']

header = header + ['ball_x', 'ball_y', 'ball_d']

header = header + ['paddle0_red0_x', 'paddle0_red0_y', 'paddle1_red1_x', 'paddle1_red1_y', 'paddle2_blue0_x', 'paddle2_blue0_y', 'paddle3_red2_x', 'paddle3_red2_y', 'paddle4_blue1_x', 'paddle4_blue1_y', 'paddle5_red3_x', 'paddle5_red3_y', 'paddle6_blue2_x', 'paddle6_blue2_y', 'paddle7_blue3_x', 'paddle7_blue3_y', 'paddle8_blue4_x', 'paddle8_blue4_y', 'paddle9_red4_x', 'paddle9_red4_y']

with open(data_path + '/pong.xls', 'rb') as f, open(data_path + '/task.xls', 'wb') as f2:
    reader = csv.reader(f, delimiter='\t')
    writer = csv.writer(f2, delimiter='\t')

    reader.next()
    writer.writerow(header)

    blue_score0, red_score0 = 0, 0
    ball_x0, ball_y0 = 0, 0
    ball_d0 = cmp(0, 0)

    for row in reader:

        # event

        machine = row[0]
        subject = row[1]
        #stim = row[2]
        #block = row[3]
        #start_time = row[4]
        #end_time = row[5]
        #cond = row[6]
        event = row[7].split('\\t')

        time = event[0]

        time = datetime.strftime( datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=4), '%Y-%m-%d %H:%M:%S.%f')[:-3]

        ball_x, ball_y, blue_score, red_score = float(event[1]), float(event[2]), int(event[3]), int(event[4])

        ball_d = cmp(ball_x - ball_x0, 0)

        paddle0_red0_x, paddle0_red0_y, paddle1_red1_x, paddle1_red1_y, paddle2_blue0_x, paddle2_blue0_y, paddle3_red2_x, paddle3_red2_y, paddle4_blue1_x, paddle4_blue1_y, paddle5_red3_x, paddle5_red3_y, paddle6_blue2_x, paddle6_blue2_y, paddle7_blue3_x, paddle7_blue3_y, paddle8_blue4_x, paddle8_blue4_y, paddle9_red4_x, paddle9_red4_y = float(event[5]), float(event[6]), float(event[7]), float(event[8]), float(event[9]), float(event[10]), float(event[11]), float(event[12]), float(event[13]), float(event[14]), float(event[15]), float(event[16]), float(event[17]), float(event[18]), float(event[19]), float(event[20]), float(event[21]), float(event[22]), float(event[23]), float(event[24])

        # label

        if subject == 'kkchang':
            rooting = 'blue'
        elif subject == 'yuerany':
            rooting = 'red'
        else:
            rooting = 'neutral'

        if ball_x > 0:
            possessing = 'blue'
        elif ball_x < 0:
            possessing = 'red'
        else:
            possessing = 'neutral'

        if ball_d > 0:
            attacking = 'blue'
        elif ball_d < 0:
            attacking = 'red'
        else:
            attacking = 'neutral'

        if (ball_x < paddle8_blue4_x or paddle9_red4_x < ball_x) and paddle8_blue4_x != 'n/a' and paddle9_red4_x != 'n/a':
            goaling = True
        else:
            goaling = False

        if blue_score > red_score:
            winning = 'blue'
        elif blue_score < red_score:
            winning = 'red'
        else:
            winning = 'tie'

        if ball_d != ball_d0 and ball_d0 != 0 and ball_d != 0:
            counterattack = True
        else:
            counterattack = False

        if blue_score > blue_score0 or red_score > red_score0:
            goal = True
        else:
            goal = False

        # cond

        if label == 'possessing':
            if possessing == 'neutral':
                cond = 0
            else:
                cond = 2 if possessing == rooting else 1
        elif label == 'attacking':
            if attacking == 'neutral':
                cond = 0
            else:
                cond = 2 if attacking == rooting else 1
        elif label == 'goaling':
            if goaling == False:
                cond = 0
            else:
                cond = 2 if attacking == rooting else 1
        elif label == 'winning':
            if winning == 'tie':
                cond = 0
            else:
                cond = 2 if winning == rooting else 1
        elif label == 'counterattack':
            if counterattack == False:
                cond = 0
            else:
                cond = 2 if attacking == rooting else 1
        elif label == 'goal':
            if goal == False:
                cond = 0
            else:
                cond = 2 if attacking == rooting else 1
        elif label == 'positive':
            if counterattack == False and goal == False:
                cond = 0
            else:
                cond = 2 if attacking == rooting else 1

        # entry

        entry = list(header)
        entry[ header.index('machine') ] = machine
        entry[ header.index('subject') ] = subject
        entry[ header.index('stim') ] = 'round' + str(blue_score + red_score + 1) + ' (' + str(blue_score) + ',' + str(red_score) + ')'
        entry[ header.index('block') ] = 'round' + str(blue_score + red_score + 1)
        entry[ header.index('start_time') ] = datetime.strftime( datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')                           , '%Y-%m-%d %H:%M:%S.%f')[:-3]
        entry[ header.index('end_time') ]   = datetime.strftime( datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f') + timedelta(seconds=1.000), '%Y-%m-%d %H:%M:%S.%f')[:-3]
        entry[ header.index('cond') ] = cond
        entry[ header.index('rooting') ] = rooting
        entry[ header.index('possessing') ] = possessing
        entry[ header.index('attacking') ] = attacking
        entry[ header.index('goaling') ] = goaling
        entry[ header.index('winning') ] = winning
        entry[ header.index('counterattack') ] = counterattack
        entry[ header.index('goal') ] = goal

        entry[ header.index('ball_x') ] = ball_x
        entry[ header.index('ball_y') ] = ball_y
        entry[ header.index('ball_d') ] = ball_d

        entry[ header.index('paddle0_red0_x') ] = paddle0_red0_x
        entry[ header.index('paddle0_red0_y') ] = paddle0_red0_y
        entry[ header.index('paddle1_red1_x') ] = paddle1_red1_x
        entry[ header.index('paddle1_red1_y') ] = paddle1_red1_y
        entry[ header.index('paddle2_blue0_x') ] = paddle2_blue0_x
        entry[ header.index('paddle2_blue0_y') ] = paddle2_blue0_y
        entry[ header.index('paddle3_red2_x') ] = paddle3_red2_x
        entry[ header.index('paddle3_red2_y') ] = paddle3_red2_y
        entry[ header.index('paddle4_blue1_x') ] = paddle4_blue1_x
        entry[ header.index('paddle4_blue1_y') ] = paddle4_blue1_y
        entry[ header.index('paddle5_red3_x') ] = paddle5_red3_x
        entry[ header.index('paddle5_red3_y') ] = paddle5_red3_y
        entry[ header.index('paddle6_blue2_x') ] = paddle6_blue2_x
        entry[ header.index('paddle6_blue2_y') ] = paddle6_blue2_y
        entry[ header.index('paddle7_blue3_x') ] = paddle7_blue3_x
        entry[ header.index('paddle7_blue3_y') ] = paddle7_blue3_y
        entry[ header.index('paddle8_blue4_x') ] = paddle8_blue4_x
        entry[ header.index('paddle8_blue4_y') ] = paddle8_blue4_y
        entry[ header.index('paddle9_red4_x') ] = paddle9_red4_x
        entry[ header.index('paddle9_red4_y') ] = paddle9_red4_y

        writer.writerow(entry)

        blue_score0, red_score0 = blue_score, red_score
        ball_x0, ball_y0 = ball_x, ball_y
        ball_d0 = ball_d
