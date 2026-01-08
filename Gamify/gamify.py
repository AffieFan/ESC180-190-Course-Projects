def initialize ():
    global activity
    global tired
    global cur_health
    global cur_hedons
    global last_time
    global offered_star
    global cur_time
    global last_completed_run_time
    global last_completed_textbook_time
    global star_time_1, star_time_2,star_time_3
    global bored
    global last_activity
    global last_activity_duration
    global run_time_total
    global health_points_added

    cur_health = 0
    cur_hedons = 0
    last_time = 0
    offered_star = "deactivated"
    cur_time = 0
    last_completed_run_time = -1000
    last_completed_textbook_time = -1000
    star_time_1 = -120
    star_time_2 = -120
    star_time_3 = -120
    last_activity = ""
    last_activity_duration = 0
    run_time_total = 0
    health_points_added = 0
    bored = False
    tired = False


def perform_activity (activity, duration):
    global cur_health
    global cur_hedons
    global cur_time
    global last_completed_run_time
    global last_completed_textbook_time
    global offered_star
    global tired
    global last_activity
    global last_activity_duration
    global run_time_total
    global health_points_added



    #tired
    if last_activity == "running" and activity =="running" and run_time_total < 180:
        tired = False
    elif last_activity == "running" and activity == "running" and run_time_total > 180:
        tired = True
    elif (cur_time - last_completed_run_time <= 120) or (cur_time - last_completed_textbook_time <= 120):
        tired = True
    else:
        tired = False


    #Star check
    if offered_star == activity and bored == False:
        use_star = True
    else:
        use_star = False

    offered_star = "deactivated"

   #Health Points
    if activity == "running":
        if last_activity == "running":
            if run_time_total == 0:
                run_time_total = last_activity_duration + duration
            else:
                run_time_total += duration

            if run_time_total > 180:
                cur_health += (180 * 3 + (run_time_total - 180 * 1)) - health_points_added
                health_points_added += (180 * 3 + (run_time_total - 180 * 1)) - health_points_added
            else:
                cur_health += (run_time_total * 3) - health_points_added
                health_points_added += (run_time_total * 3) - health_points_added

        else:
            run_time_total = 0
            health_points_added = 0

            if duration <= 180:
                cur_health += duration * 3
                health_points_added = duration * 3
            elif duration > 180:
                cur_health  += (180 * 3) + (duration - 180) * 1
                health_points_added = (180 * 3) + (duration - 180) * 1


    elif activity == "textbooks":
        cur_health += duration * 2
    elif activity == "resting":
        cur_health += 0


    #Hedons
    if tired == True and (activity == "textbooks" or activity == "running"):
        cur_hedons += duration * -2
    elif tired == False and activity == "running" and last_activity != "running":
        if duration <= 10:
            cur_hedons += duration * 2
        else:
            cur_hedons += (2 * 10) + (duration - 10) * -2
    elif tired == False and activity == "running" and last_activity == "running":
        if duration <= 10:
            cur_hedons += duration * 2
        else:
            cur_hedons += duration * -2
    elif tired == False and activity == "textbooks":
        if duration <= 20:
            cur_hedons += duration * 1
        else:
            cur_hedons += 20 * 1 + (duration - 20) * -1
    elif activity == "resting":
        cur_hedons += 0


    if use_star == True:
        if duration <= 10:
            cur_hedons += duration * 3
        else:
            cur_hedons += 10 * 3



    cur_time += duration

    if activity == "running":
        last_completed_run_time = cur_time
    elif activity == "textbooks":
        last_completed_textbook_time = cur_time

    last_activity = activity
    last_activity_duration = duration



def get_cur_health ():
    return cur_health

def get_cur_hedons ():
    return cur_hedons

def offer_star (activity):
    global offered_star
    global star_time_1
    global star_time_2
    global star_time_3
    global bored

    offered_star = activity
    star_time_1 = star_time_2
    star_time_2 = star_time_3
    star_time_3 = cur_time

    if star_time_3 - star_time_1 < 120:
        bored = True

def star_can_be_taken (activity):
    if offered_star == activity and bored == False:
        return True
    else:
        return False

def most_fun_activity_minute ( ):
    if (cur_time - last_completed_run_time <= 120) or (cur_time - last_completed_textbook_time <= 120):
        tired_test = True
    else:
        tired_test = False

    if offered_star == "running":
        return "running"
    if offered_star == "textbooks":
        return "textbooks"
    elif tired_test == True:
        return "resting"
    elif tired_test == False:
        return "running"


if __name__ == '__main__':

    initialize ()



