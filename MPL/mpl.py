import pygame
import random
import time
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cricket Game Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)

# Fonts
font_small = pygame.font.SysFont('Arial', 20)
font_medium = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 32)
font_xl = pygame.font.SysFont('Arial', 40)

# Load team images (these will be provided by the user)
def load_image(filename, size=(150, 150)):
    try:
        image = pygame.image.load(filename)
        return pygame.transform.scale(image, size)
    except:
        # Create a placeholder if image not found
        surf = pygame.Surface(size)
        surf.fill(ORANGE if "csk" in filename.lower() else BLUE)
        text = font_medium.render(filename.split('.')[0].upper(), True, WHITE)
        surf.blit(text, (size[0]//2 - text.get_width()//2, size[1]//2 - text.get_height()//2))
        return surf

# Team data
class Team:
    def __init__(self, name, players, bowlers, logo_file):
        self.name = name
        self.players = players  # List of (name, runs, balls faced, lives)
        self.bowlers = bowlers  # List of (name, overs, wickets, runs conceded)
        self.logo = load_image(logo_file)
        self.score = 0
        self.wickets = 0
        self.overs = 0
        self.balls = 0
        self.current_batsmen = [0, 1]  # Indices of current batsmen
        self.current_bowler = [0]   # Index of current bowler
        self.used_bowlers = []  # Track which bowlers have been used
        self.batting_history = []  # To store over-by-over runs for each player
        self.innings_completed = False
        self.final_scoreboard = []  # To store final batting scorecard
        self.final_bowling_figures = []  # To store final bowling figures

    def update_score(self, runs):
        self.score += runs
        if runs in [1, 3]:
            # Switch batsmen for odd runs
            self.current_batsmen[0], self.current_batsmen[1] = self.current_batsmen[1], self.current_batsmen[0]

    def add_ball(self, is_legal_delivery):
        if is_legal_delivery:
            self.balls += 1
            print(f"Team {self.name}: Ball {self.balls} of over {self.overs}")
            if self.balls == 6:
                print(f"End of over {self.overs} for team {self.name}")
                self.overs += 1
                self.balls = 0
                # Switch batsmen at end of over
                old_batsmen = self.current_batsmen.copy()
                self.current_batsmen[0], self.current_batsmen[1] = self.current_batsmen[1], self.current_batsmen[0]
                print(f"Switched batsmen from {old_batsmen} to {self.current_batsmen}")
                # Change bowler at end of over
                old_bowler = self.current_bowler[0]
                self.select_new_bowler()
                print(f"Changed bowler from {old_bowler} to {self.current_bowler[0]}")

    def select_new_bowler(self):
     print(f"Current bowler: {self.current_bowler[0]}, Used bowlers: {self.used_bowlers}")
    
     # Add current bowler to used bowlers if not already there
     if self.current_bowler[0] not in self.used_bowlers:
        self.used_bowlers.append(self.current_bowler[0])
    
     # Find the next available bowler
     next_bowler = None
     for i in range(len(self.bowlers)):
        if i not in self.used_bowlers:
            next_bowler = i
            break
    
     # If no new bowler available, reset used_bowlers and start over
     if next_bowler is None:
        # Keep the last bowler in used_bowlers to avoid selecting them again
        last_bowler = self.current_bowler[0]
        self.used_bowlers = [last_bowler]
        
        # Find the first available bowler that isn't the last one
        for i in range(len(self.bowlers)):
            if i != last_bowler:
                next_bowler = i
                break
    
     # If we still don't have a next bowler (unlikely), just pick the first one
     if next_bowler is None and len(self.bowlers) > 0:
        next_bowler = 0
    
     # Update current bowler
     if next_bowler is not None:
        print(f"Changing bowler from {self.current_bowler[0]} to {next_bowler}")
        self.current_bowler = [next_bowler]
     else:
        print("Warning: Could not select a new bowler!")

    def wicket_falls(self):
        self.wickets += 1
        # Store the out batsman in final scoreboard if not already there
        out_batsman_idx = self.current_batsmen[0]
        self.add_to_final_scoreboard(out_batsman_idx)
        
        # Replace batsman with next in line
        next_batsman_idx = max(self.current_batsmen) + 1
        if next_batsman_idx < len(self.players) and self.wickets < 10:
            self.current_batsmen[0] = next_batsman_idx
        else:
            # All out or no more batsmen
            self.innings_completed = True
            # Add remaining batsman to scoreboard
            self.add_to_final_scoreboard(self.current_batsmen[1])
            return False
        return True

    def get_current_batsmen_names(self):
        return [self.players[i][0] for i in self.current_batsmen]

    def get_current_batsmen_scores(self):
        return [(self.players[i][1], self.players[i][2]) for i in self.current_batsmen]

    def update_batsman_score(self, runs, is_ball_faced=True):
        batsman = self.players[self.current_batsmen[0]]
        batsman_name, batsman_runs, batsman_balls, lives = batsman
        batsman_runs += runs
        if is_ball_faced:
            batsman_balls += 1
        self.players[self.current_batsmen[0]] = (batsman_name, batsman_runs, batsman_balls, lives)

    def update_bowler_stats(self, runs=0, wicket=False, is_legal_delivery=True):
        bowler = self.bowlers[self.current_bowler[0]]
        print("bowling",self.current_bowler[0])
        name, overs, wickets, runs_conceded = bowler
        if is_legal_delivery:
            # Update overs (in format X.Y where Y is balls)
            balls = int(str(overs).split('.')[-1]) if '.' in str(overs) else 0
            balls += 1
            if balls == 6:
                overs = int(overs) + 1 if '.' not in str(overs) else int(str(overs).split('.')[0]) + 1
                
                #if self.current_bowler[0] != 4:
                    
                print("bruh", self.current_bowler[0])
                balls = 0
            else:
                overs = int(overs) if '.' not in str(overs) else int(str(overs).split('.')[0])
                overs = f"{overs}.{balls}"
        
        if wicket:
            wickets += 1
        
        runs_conceded += runs
        
        self.bowlers[self.current_bowler[0]] = (name, overs, wickets, runs_conceded)
        if is_legal_delivery == True:
            if balls == 0:
               self.current_bowler[0] += 1 

    def get_current_bowler(self):
        i = self.current_bowler[0]
        if i == 5:
            i = 0
        return self.bowlers[i]

    def reduce_life(self):
        batsman = self.players[self.current_batsmen[0]]
        batsman_name, batsman_runs, batsman_balls, lives = batsman
        lives -= 1
        self.players[self.current_batsmen[0]] = (batsman_name, batsman_runs, batsman_balls, lives)
        return lives

    def record_over_history(self, player_idx, runs):
        while len(self.batting_history) <= player_idx:
            self.batting_history.append([])
        
        over_idx = self.overs
        if self.balls == 0 and over_idx > 0:
            over_idx -= 1
        
        while len(self.batting_history[player_idx]) <= over_idx:
            self.batting_history[player_idx].append('')  # 'w' for no ball faced in this over
        
        if self.batting_history[player_idx][over_idx] == '':
            self.batting_history[player_idx][over_idx] = runs
        else:
            # Convert to string if it was a number
            current = str(self.batting_history[player_idx][over_idx])
            self.batting_history[player_idx][over_idx] = current + str(runs)

    def add_to_final_scoreboard(self, player_idx):
        # Check if player is already in final scoreboard
        for p in self.final_scoreboard:
            if p[0] == self.players[player_idx][0]:
                return
                
        # Add player to final scoreboard
        self.final_scoreboard.append(self.players[player_idx])

    def complete_innings(self):
        self.innings_completed = True
        # Add all current batsmen to the final scoreboard
        for idx in self.current_batsmen:
            self.add_to_final_scoreboard(idx)
        # Add all bowlers to the final bowling figures
        self.final_bowling_figures = list(self.bowlers)

# Create teams
csk_players = [
    ("Ruturaj Gaikwad", 0, 0, 1),
    ("Devon Conway", 0, 0, 1),
    ("Rahul Tripathi", 0, 0, 1),
    ("Shivam Dube", 0, 0, 1),
    ("Deepak Hooda", 0, 0, 1),
    ("Sam Curran", 0, 0, 1),
    ("Ravindra Jadeja", 0, 0, 1),
    ("MS Dhoni", 0, 0, 1),
    ("Ravichandran Ashwin", 0, 0, 1),
    ("Noor Ahmed", 0, 0, 1),
    ("Matheesa Pathirana", 0, 0, 1)
]

csk_bowlers = [
    ("Sam Curran", 0, 0, 0),
    ("Ravindra Jadeja", 0, 0, 0),
    ("Noor Ahmed", 0, 0, 0),
    ("Matheesa Pathirana", 0, 0, 0),
    ("Y.Dayal", 0, 0, 0)  # Extra bowler for 5 overs
]

rcb_players = [
    ("Virat Kohli", 0, 0, 1),
    ("Phil Salt", 0, 0, 1),
    ("Liam Livingstone", 0, 0, 1),
    ("Rajat Patidar", 0, 0, 1),
    ("Krunal Pandya", 0, 0, 1),
    ("Jitesh Sharma", 0, 0, 1),
    ("Tim David", 0, 0, 1),
    ("Swapnil Singh", 0, 0, 1),
    ("Bhuvneshwar Kumar", 0, 0, 1),
    ("Josh Hazlewood", 0, 0, 1),
    ("Yash Dayal", 0, 0, 1)
]

rcb_bowlers = [
    ("Liam Livingstone", 0, 0, 0),
    ("J.Sharma", 0, 0, 0),
    ("Swapnil Singh", 0, 0, 0),
    ("Bhuvneshwar Kumar", 0, 0, 0),
    ("N.Ahmed", 0, 0, 0)  # Extra bowler for 5 overs
]

team1 = Team("CSK", csk_players, csk_bowlers, "csk.png")  # Note: team1 uses team2's bowlers
team2 = Team("RCB", rcb_players, rcb_bowlers, "rcb.png")  # team2 uses team1's bowlers

# Game state variables
current_batting_team = team1
current_bowling_team = team2
game_over = False
total_overs = 5
ball_interval = 1  # seconds between balls
last_ball_time = time.time()
ball_in_progress = False
event_text = "Game Starting..."
last_runs = None
required_runs = None
result_text = None
show_final_scorecard = False

# Draw scoreboard
def draw_scoreboard():
    screen.fill(BLACK)
    
    if show_final_scorecard:
        draw_final_scorecard()
        return
    
    # Draw team logos and names
    screen.blit(team1.logo, (50, 50))
    screen.blit(team2.logo, (WIDTH - 200, 50))
    
    # Draw main score
    score_text = f"{team1.score}/{team1.wickets}"
    font_score = font_xl.render(score_text, True, WHITE)
    screen.blit(font_score, (300, 70))
    
    # Draw overs
    overs_text = f"{team1.overs}.{team1.balls}"
    font_overs = font_medium.render(overs_text, True, WHITE)
    screen.blit(font_overs, (300, 120))
    
    # If second innings
    if team2.score > 0 or team2.wickets > 0 or team2.balls > 0 or team2.overs > 0:
        score_text2 = f"{team2.score}/{team2.wickets}"
        font_score2 = font_xl.render(score_text2, True, WHITE)
        screen.blit(font_score2, (WIDTH - 350, 70))
        
        overs_text2 = f"{team2.overs}.{team2.balls}"
        font_overs2 = font_medium.render(overs_text2, True, WHITE)
        screen.blit(font_overs2, (WIDTH - 350, 120))
        
        if current_batting_team == team2:
            if required_runs is not None:
                req_text = f"Need {required_runs} runs"
                font_req = font_medium.render(req_text, True, WHITE)
                screen.blit(font_req, (WIDTH//2 - font_req.get_width()//2, 150))
    
    # Current batsmen
    if not game_over:
        batsmen_names = current_batting_team.get_current_batsmen_names()
        batsmen_scores = current_batting_team.get_current_batsmen_scores()
        
        # First batsman
        y_pos = 200
        name_text = font_medium.render(f"{batsmen_names[0]}*", True, WHITE)
        score_text = font_medium.render(f"{batsmen_scores[0][0]}({batsmen_scores[0][1]})", True, WHITE)
        screen.blit(name_text, (50, y_pos))
        screen.blit(score_text, (300, y_pos))
        
        # Second batsman
        y_pos = 230
        name_text = font_medium.render(f"{batsmen_names[1]}", True, WHITE)
        score_text = font_medium.render(f"{batsmen_scores[1][0]}({batsmen_scores[1][1]})", True, WHITE)
        screen.blit(name_text, (50, y_pos))
        screen.blit(score_text, (300, y_pos))
        
        # Current bowler
        bowler = current_bowling_team.get_current_bowler()
        bowler_text = font_medium.render(f"Bowling: {bowler[0]}", True, WHITE)
        stats_text = font_medium.render(f"{bowler[1]} - {bowler[3]}/{bowler[2]}", True, WHITE)
        screen.blit(bowler_text, (WIDTH - 350, 200))
        screen.blit(stats_text, (WIDTH - 350, 230))
    
    # Event text
    event_surf = font_medium.render(event_text, True, GOLD)
    screen.blit(event_surf, (WIDTH//2 - event_surf.get_width()//2, 300))
    
    # Result text
    if result_text:
        result_surf = font_large.render(result_text, True, GOLD)
        screen.blit(result_surf, (WIDTH//2 - result_surf.get_width()//2, 350))
        
        # Show prompt to view final scorecard
        if game_over:
            prompt_text = "Press 'S' to view final scorecard"
            prompt_surf = font_medium.render(prompt_text, True, GOLD)
            screen.blit(prompt_surf, (WIDTH//2 - prompt_surf.get_width()//2, 400))
    
    # Draw batting history
    draw_batting_history(team1, 50, 400)
    if team2.overs > 0 or team2.balls > 0:
        draw_batting_history(team2, WIDTH//2 + 50, 400)

def draw_batting_history(team, x, y):
    # Display for up to 5 batsmen
    for i, player_idx in enumerate(range(min(11, len(team.batting_history)))):
        if player_idx < len(team.players):
            name = team.players[player_idx][0].split()[-1]  # Just the last name
            run = team.players[player_idx][1]
            ball = team.players[player_idx][2]
            name_text = font_small.render(f"{i+1}. {name}", True, WHITE)
            run_text = font_small.render(f" {run}({ball})", True, WHITE)
            screen.blit(name_text, (x, y + i*30 - 70))
            screen.blit(run_text, (x + 150, y + i*30 - 70))
            
            # Draw the over-by-over history
            if player_idx < len(team.batting_history):
                history = team.batting_history[player_idx]
                for j, over_result in enumerate(history):
                    if j < 7:  # Show only first 7 overs
                        result_text = font_small.render(str(over_result), True, WHITE)
                        #screen.blit(result_text, (x + 150 + j*30, y + i*30))

def draw_final_scorecard():
    title_text = font_large.render("FINAL SCORECARD", True, GOLD)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
    
    # Draw team1 scorecard
    team1_text = font_medium.render(f"{team1.name}: {team1.score}/{team1.wickets} ({team1.overs}.{team1.balls} overs)", True, WHITE)
    screen.blit(team1_text, (WIDTH//4 - team1_text.get_width()//2, 100))
    
    # Draw team1 batsmen
    header_text = font_small.render("Batsman           Runs (Balls)", True, WHITE)
    screen.blit(header_text, (50, 140))
    
    y_pos = 170
    for player in team1.final_scoreboard:
        name, runs, balls, _ = player
        player_text = font_small.render(f"{name:<20} {runs:<3} ({balls})", True, WHITE)
        screen.blit(player_text, (50, y_pos))
        y_pos += 25
    
    # Draw team1 bowlers
    bowling_header = font_small.render("Bowler            O    W    R", True, WHITE)
    screen.blit(bowling_header, (50, y_pos + 20))
    y_pos += 50
    
    for bowler in team2.final_bowling_figures:  # Use team2's bowlers for team1's innings
        name, overs, wickets, runs = bowler
        bowler_text = font_small.render(f"{name:<20} {overs:<4} {wickets:<4} {runs}", True, WHITE)
        screen.blit(bowler_text, (50, y_pos))
        y_pos += 25
    
    # Draw team2 scorecard if innings completed
    if team2.innings_completed or team2.overs > 0 or team2.balls > 0:
        team2_text = font_medium.render(f"{team2.name}: {team2.score}/{team2.wickets} ({team2.overs}.{team2.balls} overs)", True, WHITE)
        screen.blit(team2_text, (3*WIDTH//4 - team2_text.get_width()//2, 100))
        
        # Draw team2 batsmen
        header_text = font_small.render("Batsman           Runs (Balls)", True, WHITE)
        screen.blit(header_text, (WIDTH//2 + 50, 140))
        
        y_pos = 170
        for player in team2.final_scoreboard:
            name, runs, balls, _ = player
            player_text = font_small.render(f"{name:<20} {runs:<3} ({balls})", True, WHITE)
            screen.blit(player_text, (WIDTH//2 + 50, y_pos))
            y_pos += 25
        
        # Draw team2 bowlers
        bowling_header = font_small.render("Bowler            O    W    R", True, WHITE)
        screen.blit(bowling_header, (WIDTH//2 + 50, y_pos + 20))
        y_pos += 50
        
        for bowler in team1.final_bowling_figures:  # Use team1's bowlers for team2's innings
            name, overs, wickets, runs = bowler
            bowler_text = font_small.render(f"{name:<20} {overs:<4} {wickets:<4} {runs}", True, WHITE)
            screen.blit(bowler_text, (WIDTH//2 + 50, y_pos))
            y_pos += 25
    
    # Draw match result
    if result_text:
        result_surf = font_large.render(result_text, True, GOLD)
        screen.blit(result_surf, (WIDTH//2 - result_surf.get_width()//2, 500))
    
    # Show prompt to return to main screen
    prompt_text = "Press 'M' to return to main screen"
    prompt_surf = font_medium.render(prompt_text, True, GOLD)
    screen.blit(prompt_surf, (WIDTH//2 - prompt_surf.get_width()//2, 550))

# Game logic
def play_ball():
    global event_text, last_runs, required_runs, result_text, game_over, current_batting_team, current_bowling_team
    
    if game_over:
        return
    
    # Check if innings is over
    if current_batting_team.overs >= total_overs or current_batting_team.wickets >= 10:
        # Complete the innings and update final scoreboard
        current_batting_team.complete_innings()
        current_bowling_team.complete_innings()
        
        # Switch innings or end game
        if current_batting_team == team1:
            current_batting_team = team2
            current_bowling_team = team1
            required_runs = team1.score + 1
            event_text = f"{team2.name} needs {required_runs} runs to win"
        else:
            game_over = True
            if team2.score > team1.score:
                result_text = f"{team2.name} wins by {10 - team2.wickets} wickets"
            elif team1.score > team2.score:
                result_text = f"{team1.name} wins by {team1.score - team2.score} runs"
            else:
                result_text = "It's a tie!"
            return
    
    # Determine run scored
    is_last_over = current_batting_team.overs == total_overs - 1
    max_rand = 8 if is_last_over else 7  # 0-7 normally, 0-8 in last over for extras
    
    # First randomization
    outcome = random.randint(0, max_rand - 1)
    
    # Handle extras in last over
    if is_last_over and outcome == 7:
        extra_type = random.randint(1, 2)  # 1: wide, 2: no ball
        if extra_type == 1:
            event_text = "Wide ball! +1 run"
            current_batting_team.update_score(1)
            current_bowling_team.update_bowler_stats(runs=1, is_legal_delivery=False)
            last_runs = "w"
            current_batting_team.record_over_history(current_batting_team.current_batsmen[0], "w")
            return
        else:
            event_text = "No ball! +1 run and free hit"
            current_batting_team.update_score(1)
            current_bowling_team.update_bowler_stats(runs=1, is_legal_delivery=False)
            last_runs = "nb"
            current_batting_team.record_over_history(current_batting_team.current_batsmen[0], "nb")
            # No ball doesn't count as a legal delivery
            return
    
    # Handle regular outcomes
    if outcome in [0, 1, 2, 3]:
        # Second randomization for runs 0-3
        second_outcome = random.randint(0, 3)
        if second_outcome in [0, 1, 2, 3]:
            event_text = f"{second_outcome} runs"
            current_batting_team.update_batsman_score(second_outcome)
            current_batting_team.add_ball(True)
            current_batting_team.update_score(second_outcome)
            current_bowling_team.update_bowler_stats(runs=second_outcome)
            last_runs = second_outcome
            current_batting_team.record_over_history(current_batting_team.current_batsmen[0], second_outcome)
        else:
            # Try again
            play_ball()
            return
    elif outcome == 4:
        event_text = "FOUR!"
        current_batting_team.update_score(4)
        current_batting_team.update_batsman_score(4)
        current_batting_team.add_ball(True)
        current_bowling_team.update_bowler_stats(runs=4)
        last_runs = 4
        current_batting_team.record_over_history(current_batting_team.current_batsmen[0], 4)
    elif outcome == 5:
        # Wicket
        lives = current_batting_team.reduce_life()
        if lives <= 0:
            event_text = f"OUT! {current_batting_team.get_current_batsmen_names()[0]} is dismissed!"
            current_batting_team.add_ball(True)
            current_bowling_team.update_bowler_stats(wicket=True)
            last_runs = "W"
            current_batting_team.record_over_history(current_batting_team.current_batsmen[0], "W")
            game_continues = current_batting_team.wicket_falls()
            if not game_continues:
                if current_batting_team == team1:
                    current_batting_team = team2
                    current_bowling_team = team1
                    required_runs = team1.score + 1
                    event_text = f"{team2.name} needs {required_runs} runs to win"
                else:
                    game_over = True
                    if team2.score > team1.score:
                        result_text = f"{team2.name} wins by {10 - team2.wickets} wickets"
                    elif team1.score > team2.score:
                        result_text = f"{team1.name} wins by {team1.score - team2.score} runs"
                    else:
                        result_text = "It's a tie!"
        else:
            event_text = "Close call! Batsman survives."
            # Repeat the ball
            play_ball()
            return
    elif outcome == 6:
        event_text = "SIX!"
        current_batting_team.update_score(6)
        current_batting_team.update_batsman_score(6)
        current_batting_team.add_ball(True)
        current_bowling_team.update_bowler_stats(runs=6)
        last_runs = 6
        current_batting_team.record_over_history(current_batting_team.current_batsmen[0], 6)
    
    # Update required runs in second innings
    if current_batting_team == team2:
        required_runs = team1.score + 1 - team2.score
        if required_runs <= 0:
            game_over = True
            result_text = f"{team2.name} wins by {10 - team2.wickets} wickets"
            current_batting_team.complete_innings()
            current_bowling_team.complete_innings()

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    current_time = time.time()
    
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not ball_in_progress and not game_over and not show_final_scorecard:
                    play_ball()
                    ball_in_progress = True
                    last_ball_time = current_time
            elif event.key == pygame.K_s:
                if game_over:
                    show_final_scorecard = True
            elif event.key == pygame.K_m:
                if show_final_scorecard:
                    show_final_scorecard = False
    
    # Automatic ball playing every 5 seconds
    if not ball_in_progress and not game_over and current_time - last_ball_time >= ball_interval and not show_final_scorecard:
        play_ball()
        ball_in_progress = True
        last_ball_time = current_time
    
    # Reset ball_in_progress after 2 seconds
    if ball_in_progress and current_time - last_ball_time >= 2:
        ball_in_progress = False
    
    # Draw everything
    draw_scoreboard()
    
    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()