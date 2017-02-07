from django.shortcuts import render
from name_game.models import Person, BlockID, ScoreKeeper


def home(request):
    context = dict()
    context['app_name'] = 'Name Game Application'
    context['created_by'] = 'Eric Borrow, Elena Giralt, Mike Russo'
    context['block_num'] = BlockID.objects.all()
    return render(request, 'home.html', context)


def game_start(request):
    # initialize score

    which_clicked = ''
    try:
        request.GET['practice']
        which_clicked = 'practice'
    except:
        pass
    if which_clicked == 'practice':
        return practice(request)

    from random import randrange
    context = dict()
    try:
        max_people = request.GET['max_people']
    except:
        max_people = None
    #print("Init max_people:",max_people)
    user_name = request.GET['user_name']
    block_sel = request.GET['block_pick']
    user_list = BlockID.objects.get(long_name=block_sel).person_set.all().order_by('f_name')

    if user_name == '':
        user_name = 'Anonymous'

    try:
        difficulty = request.GET['difficulty']
    except:
        difficulty = 'Normal'

    try:
        c = ScoreKeeper.objects.get(username=user_name)
        c.active_score = 0
        c.save()
    except:
        c = ScoreKeeper(username=user_name, active_score=0, high_score=0)
        c.save()

    gen_list = list()
    for sel_name in user_list:
        gen_list.append(sel_name.p_id)
        # print(sel_name.p_id)

    random_index = randrange(0, len(gen_list))
    start_place = gen_list[random_index]
    #print("Start Place on start:",start_place)
    guessed = dict()
    #Pass contextual variables
    context['block_sel'] = block_sel
    context['score'] = ScoreKeeper.objects.get(username=user_name).active_score
    context['hscore'] = ScoreKeeper.objects.get(username=user_name).high_score
    context['pop_list'] = user_list
    context['start_pic'] = "name_game/" + start_place + ".jpg"
    context['right_answer'] = Person.objects.get(p_id=start_place)
    context['guessed'] = guessed
    context['user_person'] = user_name
    context['outcome'] = "Begin the game!"
    context['difficulty'] = difficulty
    context['max_people'] = max_people
    if difficulty == "Easy":
        # Multiple choice options for easy mode
        choices = get_multiple_choices(gen_list, Person.objects.get(p_id=start_place))
        pos = 1
        for choice in choices:
            key_choice = 'option' + str(pos)
            context[key_choice] = choice
            pos += 1
        return render(request, 'game_easy.html', context)
    elif difficulty == "Normal":
        return render(request, 'game_normal.html', context)
    elif difficulty == "Hard":
        return render(request, 'game_hard.html', context)


def next_page(request):
    from random import randrange
    import ast
    which_clicked = ''
    # Validate that one option has been selected on easy or text has been entered or a name selected
    difficulty = request.GET['difficulty']
    guessed = ast.literal_eval(request.GET['guessed']) #Tracks entries that have already been shown and whether guess was right or wrong
    #print("Original Guessed:",guessed)
    try:
        max_people = float(request.GET['max_people'])
        if max_people <= 0:
            max_people = None
    except:
        max_people = None
    try:
        request.GET['start_over']
        which_clicked = 'startover'
    except:
        pass
    try:
        request.GET['game']
        which_clicked = 'next'
    except:
        pass

    if which_clicked == 'startover':
        return home(request)
    elif which_clicked == 'next':
        context = dict()

        try:
            user_sel = request.GET['name_guess']
        except:
            user_sel = ''

        rght_answer = request.GET['right_answer']
        user_name = request.GET['user_namer']
        block_sel = request.GET['blocker']
        user_list = BlockID.objects.get(long_name=block_sel).person_set.all().order_by('f_name')
        gen_list = list()
        usernames = dict()
        for user in user_list:
            gen_list.append(user.p_id)
            usernames[user.__str__()] = user.p_id
        #print("On next:",user_list)
        c = ScoreKeeper.objects.get(username=user_name)
        if check_guess(user_sel, rght_answer): #If guess was correct
            guessed[rght_answer] = True
            c.active_score = sum(guessed.values())
            if c.active_score > c.high_score:
                c.high_score = c.active_score
            c.save()
            context['outcome'] = "Correct!"
        else:
            guessed[rght_answer] = False
            #In future would be cool to see what wrong guess was for a particular person to see if anyone is often confused with them
            context['outcome'] = "Wrong!  That was " + rght_answer
            #Scrape for additional content here and display as a link with the person's name
        #print("Guessed (after):", guessed)
        #if there are any names left unguessed
        random_index = randrange(0, len(user_list))
        finished = False
        #print("Previously Appeared:",guessed)
        #print("Who we're looking for:",user_list[random_index])
        #print("Search Result:",guessed.get(user_list[random_index]))
        while guessed.get(str(user_list[random_index])) is not None:
            if len(guessed) >= len(user_list): #Should prevent hangups once every choice has been cycled through
                finished = True
                break
            random_index = randrange(0, len(user_list))

        #print("Number of guesses so far:",len(guessed))
        #print("Max people:", max_people)
        if max_people is not None and len(guessed) == max_people:
            finished = True

        if finished: #If exhuasted all people in selected group
            num_correct = sum(guessed.values())
            num_total = len(guessed)
            final_context = dict()
            final_round_user = request.GET['user_namer']
            final_context['final_user'] = final_round_user
            final_context['final_round_score'] = ScoreKeeper.objects.get(username=final_round_user).active_score
            final_context['final_round_hscore'] = ScoreKeeper.objects.get(username=final_round_user).high_score
            final_context['percent'] =  "{0:.2f}%".format(num_correct / num_total * 100)
            final_context['correct'] = num_correct
            final_context['total'] = num_total
            wrong = list()
            if num_correct == num_total: #If all guesses were correct
                final_context['wrong'] = ''
            else:
                for key in guessed:
                    if guessed[key] == False:
                        wrong.append((key,"name_game/" + usernames[key] + ".jpg",profile_url(key)))
                final_context['wrong'] = wrong
            return render(request, 'continue_game.html', final_context)

        start_place = user_list[random_index].p_id
        high_score = ScoreKeeper.objects.get(username=user_name).high_score
        active_score = ScoreKeeper.objects.get(username=user_name).active_score

        #Pass contextual variables
        context['block_sel'] = block_sel
        context['score'] = active_score
        context['hscore'] = high_score
        context['pop_list'] = user_list
        context['start_pic'] = "name_game/" + start_place + ".jpg"
        #print("pid:",Person.objects.get(p_id=start_place))
        context['right_answer'] = Person.objects.get(p_id=start_place)
        context['guessed'] = guessed
        context['start_place'] = start_place
        context['user_person'] = user_name
        context['difficulty'] = difficulty
        context['max_people'] = max_people

        if difficulty == "Easy":
            # Multiple choice options for easy mode
            choices = get_multiple_choices(gen_list, Person.objects.get(p_id=start_place))
            pos = 1
            for choice in choices:
                key_choice = 'option' + str(pos)
                context[key_choice] = choice
                pos += 1
            return render(request, 'game_easy.html', context)
        elif difficulty == "Normal":
            return render(request, 'game_normal.html', context)
        elif difficulty == "Hard":
            return render(request, 'game_hard.html', context)

def practice(request):
    context = dict()
    pictures = list()
    block_sel = request.GET['block_pick']
    user_list = BlockID.objects.get(long_name=block_sel).person_set.all().order_by('f_name')

    for user in user_list:
        pictures.append((str(user),"name_game/" + user.p_id + ".jpg"))
    context['pictures'] = pictures
    return render(request, 'practice.html', context)

def leaderboard(request):
    from operator import itemgetter
    context = dict()
    top_ten = list()
    scoreboard = list()
    scores = ScoreKeeper.objects.all()
    # Gets the total list of scores
    for score in scores:
        if score.username == '':
            top_ten.append(("Anonymous", score.high_score))
        else:
            top_ten.append((score.username, score.high_score))
    # Sorts the list and then takes top 10 scores
    top_ten.sort(key=itemgetter(1), reverse=True)
    top_ten = top_ten[:10]
    # Iterates the top ten and builds the strings to display on the page
    for score in top_ten:
        scoreboard.append(score[0] + ": " + str(score[1]))
    context['scoreboard'] = scoreboard
    return render(request, 'leaderboard.html', context)

def profile_url(name):
    # from bs4 import BeautifulSoup
    # import requests
    # base_url = "https://google.com/#q="
    # data = BeautifulSoup(requests.get(base_url).content,'lxml')
    name = name.replace(' ', '+')
    info = "stern+linkedin"
    return "http://google.com/#q=%s+%s" % (name,info)

def check_guess(user_sel, rght_answer):

    # print("Correct answer:", rght_answer)
    # print("User guessed:", user_sel)
    #print("Looking for First Name:",rght_answer.split(' ',1)[0])
    #print("Entered First Name:",user_sel.split(' ',1)[0])

    #Checks for either exact match or match on first name
    if user_sel == rght_answer or user_sel.split(' ',1)[0] == rght_answer.split(' ',1)[0]:
        return True
    else:
        return False

def get_multiple_choices(gen_list, answer, max_choices=4):
    from random import randrange
    import random
    num_choices = 1

    if len(gen_list) >= max_choices:
        choices = list()
        choices.append(answer)
        while (num_choices < max_choices):
            random_index = randrange(0, len(gen_list))
            option = Person.objects.get(p_id=gen_list[random_index])
            while option in choices:
                random_index = randrange(0, len(gen_list))
                option = Person.objects.get(p_id=gen_list[random_index])
            choices.append(option)
            num_choices += 1
    else:
        choices = gen_list

    random.shuffle(choices)
    return choices