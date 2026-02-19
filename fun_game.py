# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         VERONIKA REZNICHENKO,SOFIA LOPEZ, ANABEL ROSADO, SHEILAH RAMIEREZ-MONTOYA
# Section:      462/562
# Assignment:   LAB 13: FUN GAME
# Date:         11/25/2025

import pygame
import random
import sys
import string

pygame.init()
# --- Wild West Music Setup ---
pygame.mixer.init()

try:
    pygame.mixer.music.load("country-boy-with-his-banjo-199639.mp3")  # or .wav
    pygame.mixer.music.set_volume(0.65)  # cowboy vibes
    pygame.mixer.music.play(-1)          # loop forever
    print("Wild West music loaded successfully!")
except:
    print("Could not load Wild West music. Check the filename.")

#   def display_function():
#setting up the window
width, height = 900, 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Extreme Hangman")
tan = (210,180,140)
black = (0,0,0)
white = (255,255,255)

wood = (139,69,19)
outline = (90,45,10)
grain = (160, 82, 45)
headc=(180,210,240)
buttonc=(230,230,230)
buttonh=(245,245,245)
red = (200,40,40)

clock = pygame.time.Clock()

wordfont=pygame.font.SysFont(None,56)
lettfont=pygame.font.SysFont(None,30)
jailfont=pygame.font.SysFont(None,24)
bigfont=pygame.font.SysFont(None,64)
medfont=pygame.font.SysFont(None,35)

insults = [
    'That sucked',
    "That's rough",
    'My grandma could do\nbetter than that',
    'You must go to t.u.',
    'That was a guess?',
    'Yikes...',
    'Is this mic on?',
    'Are you even passing\nyour classes?',
    'dumb or dumber?\nthat is the question',
   ]

#theme files

#drawing extra background decor
def draw_decor(surface,x,y):
    cactus = (34,110,30)
    dark = (20,70,20)

    #trunk
    pygame.draw.rect(surface,cactus,(x,y,30,90))
    pygame.draw.rect(surface, dark, (x,y,30,90),3)

    #arm
    pygame.draw.rect(surface,cactus,(x-20,y+25,20,50))
    pygame.draw.rect(surface,dark,(x-20,y+25,20,50),2)

    #arm
    pygame.draw.rect(surface,cactus,(x+30,y+25,20,50))
    pygame.draw.rect(surface,dark,(x+30,y+25,20,50),2)

#drawing the platform
def draw_platform(surface):
    #platform
    pygame.draw.rect(surface,wood,(150,330,550,40))
    pygame.draw.rect(surface,outline,(150,330,550,40),4)

    pygame.draw.line(surface,grain,(240,350),(350,348),3)
    pygame.draw.line(surface,grain,(300,365),(480,360),2)
    pygame.draw.line(surface,grain,(400,345),(700,348),3)
    #pole
    pygame.draw.line(surface,black,(153,80),(153,330),6)
    pygame.draw.line(surface,black,(153,80),(300,80),6)
    pygame.draw.line(surface, black,(300,80),(300,130),3)

def draw_hangman(surface,wrong):
    #one wrong,head
    if wrong >= 1:
        pygame.draw.circle(surface,headc,(300,160),30)
        pygame.draw.circle(surface,black,(300,160),30,2)
    #two,body
    if wrong >= 2:
        pygame.draw.line(surface,black,(300,190),(300,250),2)
    #three,left arm
    if wrong >= 3:
        pygame.draw.line(surface,black,(300,225),(280,185),2)
    #four,right arm
    if wrong >= 4:
        pygame.draw.line(surface,black,(300,225),(320,185),2)
    #five, left leg
    if wrong >= 5:
        pygame.draw.line(surface,black,(300,250),(280,290),2)
    #six, right leg
    if wrong >= 6:
        pygame.draw.line(surface,black,(300,250),(320,290),2)
    if wrong >= 7:
        pygame.draw.circle(surface,black,(290,150),4)
        pygame.draw.circle(surface,black,(310,150),4)
        pygame.draw.line(surface,black,(290,172),(310,172),2)
        pygame.draw.line(surface,black,(300,160),(300,165),2)
    if wrong >= 8:
        #hat
        pygame.draw.arc(surface,red,(276,117,50,50),0,3.14,3)
    if wrong>= 9:
        #x for eyes and tongue out
        pygame.draw.line(surface,black,(285,145),(295,155),3)
        pygame.draw.line(surface,black,(295,145),(285,155),3)
        pygame.draw.line(surface,black,(305,145),(315,155),3)
        pygame.draw.line(surface,black,(315,145),(305,155),3)
        pygame.draw.arc(surface,red,(300,169,10,10),3.14,0,3)
    
def draw_jailor(surface,wrong):
    x,y = 650,205
    pygame.draw.circle(surface,headc,(x,y),30)
    pygame.draw.circle(surface,black,(x,y),30,2)

    pygame.draw.line(surface,black,(x,y+30),(x,y+90),2)
    pygame.draw.line(surface,black,(x,y+50),(x+40,y+30),2)
    pygame.draw.line(surface,black,(x,y+50),(x-40,y+30),2)
    pygame.draw.line(surface,black,(x,y+90),(x-20,y+125),2)
    pygame.draw.line(surface,black,(x,y+90),(x+20,y+125),2)
    pygame.draw.arc(surface,red,(625,162,50,50),0,3.14,3)
    pygame.draw.arc(surface,black,(645,212,15,15),3.14,0,4)

    #face
    pygame.draw.circle(surface,black,(640,200),4)
    pygame.draw.circle(surface,black,(660,200),4)
    pygame.draw.line(surface,black,(645,217),(655,217),2)
    pygame.draw.line(surface,black,(650,214),(650,209),2)
    #hat and sheriff star?
    if wrong > 0:
        idx=min(wrong-1, len(insults)-1)
        text = jailfont.render(insults[idx],True, black)
        surface.blit(text,(x+40,y-10))

#word underscores
def draw_word(surface,word,guessed):
    display =''
    for ch in word:
        if ch.isalpha():
            if ch.lower() in guessed:
                display += ch.lower() + ' '
            else:
                display += '_ '
        else:
            display += ch + ' '
    text=wordfont.render(display.strip(),True,black)
    rect=text.get_rect(center=(width//2,420))
    surface.blit(text,rect)

#alphabet buttons
def create_alpha():
    buttons = []
    x_start = 260
    y_start = 475
    spacing = 30
    for i, letter in enumerate(string.ascii_lowercase):
        x = x_start + (i%13) *spacing
        y= y_start + (i//13) * 40
        rect = pygame.Rect(x,y,26,32)
        buttons.append({'letter':letter, "rect":rect, "used": False})
    return buttons

def draw_alpha(surface,buttons):
    mouse = pygame.mouse.get_pos()
    for b in buttons:
        rect=b['rect']
        color = buttonh if rect.collidepoint(mouse) else buttonc
        if b['used']:
            color = (180,180,180)
        
        pygame.draw.rect(surface,color,rect)
        pygame.draw.rect(surface,black,rect,1)

        text = lettfont.render(b['letter'], True, black)
        surface.blit(text, text.get_rect(center=rect.center))

def alpha_click(event, buttons):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse = pygame.mouse.get_pos()

        for b in buttons:
            if b['rect'].collidepoint(mouse) and not b['used']:
                b['used'] = True
                return b['letter']
    return None

def check_progress(word, guessed_letters):#come back to
    """Check if all letters in word have been guessed."""
    for ch in word:
        if ch.isalpha() and ch.lower() not in guessed_letters:
            return False
    return True

# Turning file into list
def make_list(file_name):
    """Reads the appropriate file and takes every line/word and combines them into a list, each word being it's own index."""
    word_list = []
    with open(file_name) as theme:
        for w in theme:
            word = w.strip()
            word_list.append(word)

    return word_list

def choosing_file(theme):
    """Chooses the correct file containing themed words based on user input."""
    if theme.lower() == 'food':
        try:
            item_list = make_list("food_words.txt")
        except FileNotFoundError:
            exit() 
    elif theme.lower() == 'animals':
        try:
            item_list = make_list("animal_words.txt")
        except FileNotFoundError:
            exit() 
    elif theme.lower() == 'sports':
        try:
            item_list = make_list("sports_words.txt")
        except FileNotFoundError:
            exit() 
    elif theme.lower() == 'tamu':
        try:
            item_list = make_list("aggies_words.txt")
        except FileNotFoundError:
            exit() 
    return item_list

def introduction():
    """ The introduction before playing Extreme Hangman"""
    def select_theme():
        #shows instructions and picks theme
            valid_themes = ["animals", "sports", "food", "tamu"]
            button = []
            wbtn, hbtn = 200,60
            spacing = 20
            total_width = 4 * wbtn + 3*spacing
            startx = (22)
            y=425
            for i, name in enumerate(valid_themes):
                rect = pygame.Rect(startx + i * (wbtn+spacing) , y, wbtn, hbtn)
                button.append((name,rect))
            selecting = True
            while selecting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                        for name, rect in button:
                            if rect.collidepoint((mx,my)):
                                return name #this is the theme
                screen.fill(tan)
                title = bigfont.render('Extreme Hangman',True,black)
                title_rect = title.get_rect(center=(width//2,120))
                screen.blit(title, title_rect)
                rules_lines = [
                    "Howdy and Welcome to the game of Extreme Hangman!",
                    'The rules are as follows:',
                    "-You have 9 tries to guess as many words as you can",
                    'before your man is hung',
                    "-You will then click the letter you believe is in the word.",
                    "Good Luck!",
                    "Choose your theme to begin: ",]
                for i, line in enumerate(rules_lines):
                    t = medfont.render(line, True, black)
                    screen.blit(t, (100,145 + i*35))
                mouse = pygame.mouse.get_pos()
                for name, rect in button:
                    color = buttonh if rect.collidepoint(mouse) else buttonc
                    pygame.draw.rect(screen,color,rect)
                    pygame.draw.rect(screen,black,rect,2)
                    text = lettfont.render(name.upper(), True, black)
                    screen.blit(text, text.get_rect(center=rect.center))
                pygame.display.update()
                clock.tick(60)
    theme = select_theme()
    return theme

def get_max(file_name):
    with open(file_name) as r:
        data = [int(i) for i in r.readlines()]
    return max(data)

def end_screen(message, detail, final_user_score, scores_file= "scores.txt"):
    """
    Show final message (Game Over or You Won) until user presses a key or clicks.
    """
    high_score = get_max("Scores.txt")
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        screen.fill(tan)

        msg = bigfont.render(message, True, black)
        msg_rect = msg.get_rect(center=(width // 2, 230))
        screen.blit(msg, msg_rect)

        det = medfont.render(detail, True, black)
        det_rect = det.get_rect(center=(width // 2, 300))
        screen.blit(det, det_rect)

        score_text = medfont.render(f"Your Score: {final_user_score}", True, black)
        score_rect = score_text.get_rect(center=(width //2,350))
        screen.blit(score_text, score_rect)

        y_offset = 360
        prev_title = lettfont.render(f"Overall High Scores: {high_score}", True, black)
        prev_title_rect = prev_title.get_rect(center=(width// 2, 400))
        screen.blit(prev_title, prev_title_rect)

        #if msg == "You Won":
            #congrats = medfont.render(f"Congrats on a new high score!",True,red)
            #congrats_rect = congrats.get_rects(center = (width // 2, 430))
            #screen.blit(congrats,congrats_rect)
        #else:
            #boohoo = medfont.render(f"You suck...Try better next time",True,red)
            #boohoo_rect = boohoo.get_rects(center = (width // 2, 430))
            #screen.blit(boohoo,boohoo_rect)
        det = medfont.render(detail, True, black)
        det_rect = det.get_rect(center=(width // 2, 300))
        screen.blit(det, det_rect)
        instr = lettfont.render("Press any key or click to quit.", True, black)
        screen.blit(instr, (width // 2-145,430))

        pygame.display.update()
        clock.tick(60)

def play_game():
    """
    Main Extreme Hangman loop in Pygame.
    - Player chooses a theme.
    - Words loaded from file.
    - Wrong guesses carry across words (max 9).
    - Click letters to guess.
    """
    max_mistakes = 9

    # 1. Theme selection screen
    theme = introduction()
    word_list = choosing_file(theme)
    if not word_list:
        end_screen("Error", "No words found for that theme.")
        return

    random.shuffle(word_list)

    wrong_guesses = 0
    correct_words = 0

    # 2. Loop over each word in the list
    for index, secret_word in enumerate(word_list):
        guessed_letters = set()
        alpha_but = create_alpha()
        word_solved = False

        # Inner loop: guess this word until solved or mistakes used up
        while not word_solved and wrong_guesses < max_mistakes:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                clicked = alpha_click(event, alpha_but)
                if clicked:
                    # only handle new letters
                    if clicked not in guessed_letters:
                        guessed_letters.add(clicked)
                        if clicked not in secret_word.lower():
                            wrong_guesses += 1

            # Check if word solved
            word_solved = check_progress(secret_word, guessed_letters)

            # Draw everything
            screen.fill(tan)
            draw_decor(screen, 55, 300)
            draw_decor(screen, 785, 300)
            draw_platform(screen)
            draw_hangman(screen, min(wrong_guesses, 9))
            draw_jailor(screen, wrong_guesses)
            draw_word(screen, secret_word, guessed_letters)
            draw_alpha(screen, alpha_but)

            # Status text
            status = f"Theme: {theme.upper()}   Word {index+1}/{len(word_list)}"
            stat_text = lettfont.render(status, True, black)
            screen.blit(stat_text, (20, 20))

            mistakes_text = f"Mistakes: {wrong_guesses}/{max_mistakes}"
            color = red if wrong_guesses >= max_mistakes - 2 else black
            mis_text = lettfont.render(mistakes_text, True, color)
            screen.blit(mis_text, (20, 50))

            pygame.display.update()
            clock.tick(60)

            if wrong_guesses >= max_mistakes:
                pygame.time.wait(500)
                break

        if word_solved:
            correct_words += 1

        if wrong_guesses >= max_mistakes:
            break

    # 3. End-of-game summary (similar idea to your print at the end)
    
        
    # New file with the overall scores of everyone who has played
    new_file = 'Scores.txt'
    scores = []
    with open("Scores.txt",'a') as f:
        score_total = 0
        #5 points per letter meaing bigger words more points
        for i in secret_word:
            if i in "abcdefghijklmnopqrstuvwxyz":
                score_total += 5
            else:
                continue
        user_score = wrong_guesses * 5 #Need to look at this when wanting to make out changes
        final_user_score = abs(score_total - user_score)
        f.write(str(final_user_score) + '\n')

    with open("Scores.txt", "r") as f:
        for line in f:
            try:
                scores.append(int(line.strip()))
            except:
                pass
   
        
    if wrong_guesses >= max_mistakes:
        msg = "Game Over!"
        det = f"You solved {correct_words} words. Final word: {secret_word}"
        score_text = f"Your final score is {final_user_score}"
        prev_title = f"The overall high score is: {max(scores)}"
    else:
        msg = "You Won!"
        det = f"You solved all {correct_words} words!"
        score_text = f"Your final score is {final_user_score}"
        prev_title = f"The overall high score is: {max(scores)}"
        '''
        if final_user_score > max(scores):
            congrats = 'Congrats! You are the hangman master!'
        else:
            boohoo = 'Whomp...... Whomps.....'
            '''

    end_screen(msg, det, final_user_score, scores)


# ------------- Run Everything -------------

if __name__ == "__main__":
    play_game()
    pygame.quit()
    sys.exit()
def main():
    theme = introduction()
    play_game(theme)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()