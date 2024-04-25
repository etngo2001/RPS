import random

# HELPER FUNCTIONS BELOW

def get_comp_choice():
  return random.choice(['rock', 'paper', 'scissors'])

def get_user_choice(results):
  choice = []
  words = results.replace(',', '').split()

  for word in words:
    if word in ('rock', 'paper', 'scissors'):
      choice.append(word)

  return choice

def find_winner(user, comp):
  rps = {
        'rock': 1,
        'paper': 2,
        'scissors': 3
  }

  result = rps[user] - rps[comp]

  if result == 0:
      return 0 # Tie
  if result in (1,-2):
      return -1 # Player wins
  return 1 # Computer wins

'''
TO-DO
Scoreboard
User choice detection
'''