def validate_race(race):
    """ 
    Validate whether or not a race is a valid race within the game.
  
    Parameters: 
    race (string): race being input
      
    Returns: 
    string: full race name (e.g. "Terran"), raises an error if invalid race
    """    
    if (race == "Terran" or race == "Protoss" or race == "Zerg"):
        return race
    else:
        raise ValueError("Invalid parameter: " + race)

def get_matchup_from_races(player_race,enemy_race):
    """ 
    Returns the abbreviated matchup from a set of races
  
    Parameters: 
    player_race (string): race the player is playing as
    enemy_race (string): race the enemy is playing as
      
    Returns: 
    string: race vs race matchup (XvY)
    """
    return get_letter_from_race(player_race) + "v" + get_letter_from_race(enemy_race)
       
def get_letter_from_race(race):
    """ 
    Gets letter from a race
  
    Parameters: 
    race (string): string of the race being played
      
    Returns: 
    char: letter of race being played
    """
    if (race == "Terran" or race == "terran"):
        return "T"
    elif (race == 'Protoss' or race == 'protoss'):
        return "P"
    elif(race == 'Zerg' or race == 'zerg'):
        return "Z"
    else:
        raise ValueError("Invalid race: " + race)

def get_race_from_letter(matchup):
    """ 
    Gets race from a letter
  
    Parameters: 
    matchup (char): letter of the race being played
      
    Returns: 
    string: full race name (e.g. "Terran") 
    """
    if (matchup == 'T' or matchup == 't'):
        return "Terran"
    elif (matchup == 'P' or matchup == 'p'):
        return "Protoss"
    elif(matchup == 'Z' or matchup == 'z'):
        return "Zerg"
    else:
        raise ValueError("Invalid race: " + matchup)
    
def get_race_from_matchup(player,matchup):
    """ 
    Gets race from a player in a matchup.
  
    Parameters: 
    player (string): Anything not "player" or "enemy" will return an error
    matchup (string): Matchup playing assumes "XvY" formatting 
      
    Returns: 
    string: full race name (e.g. "Terran") 
    """
    matchup_num = 0
    if (player == "player"):
        matchup_num = 0
    elif(player == "enemy"):    
        matchup_num = 2
    else:
        raise ValueError("Invalid player")
    return get_race_from_letter(matchup[matchup_num])