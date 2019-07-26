from s2protocol import versions
from os import listdir,path,rename
import mpyq
import json
from sc2_race_analyzer import get_matchup_from_races

def load_settings():
    """ 
    Loads the user data from the settings file.

    Returns: 
    Dictionary with the player ID and replay folder
    """    
    with open("settings.RBRT","r") as settings_file:
        settings = {}
        for line in settings_file:
            contents = line.split("=")
            contents[1] = contents[1].replace("\n","")
            if(contents[0] == "[player_id]"):
                settings["[player_id]"] = int(contents[1])
            elif(contents[0] == "[replay_folder]"):
                settings["[replay_folder]"] = contents[1]
    return settings

def rename_file(filename,settings):
    if (path.splitext(filename)[1] == '.SC2Replay'): 
        archive = mpyq.MPQArchive(filename)
        print(archive.header)
        contents = str(archive.header['user_data_header']['content'])         
        #figure out build version of replay
        header = versions.latest().decode_replay_header(contents)
        baseBuild = header['m_version']['m_baseBuild']
        protocol = versions.build(baseBuild)
        contents = archive.read_file('replay.details')
        details = protocol.decode_replay_details(contents)
        metadata = json.loads(archive.read_file('replay.gamemetadata.json'))
        contents = archive.read_file('replay.initData')
        initData = protocol.decode_replay_initdata(contents)
        #data only matters if it's a 1v1
        if (initData['m_syncLobbyState']['m_gameDescription']['m_gameOptions']['m_competitive'] and initData['m_syncLobbyState']['m_gameDescription']['m_maxPlayers'] == 2):
            game_duration = metadata["Duration"]/84
            player_race = ""
            enemy_name = ""
            enemy_race = ""
            enemy_mmr = ""
            result = ""
            for player in details['m_playerList']:
                if (player['m_toon']['m_id'] == settings["[player_id]"]):
                    player_race = player['m_race']
                    for meta_player in metadata['Players']:
                        if meta_player['PlayerID'] == player['m_workingSetSlotId'] + 1:
                            result = meta_player["Result"]
                        else:
                            #player might not have MMR if in placements
                            try:
                                enemy_mmr = meta_player["MMR"]
                            except:
                                enemy_mmr = "" 
                else:
                    enemy_race = player['m_race']
                    enemy_name = player['m_name']  
            matchup = get_matchup_from_races(player_race,enemy_race)
            
            #force cleanup on archive to allow file to be renamed
            del archive
            formatted_enemy_name = unicode(enemy_name,"utf-8")
            formatted_enemy_name = formatted_enemy_name.replace("&lt;","(")
            formatted_enemy_name = formatted_enemy_name.replace("&gt;",")")
            formatted_enemy_name = formatted_enemy_name.replace("<sp/>","")
            name = matchup + " - " + result + " - " +  str(game_duration) + " min - "+ "[" + formatted_enemy_name + ("" if enemy_mmr == "" else " ") + str(enemy_mmr) + "] - "  + metadata["Title"]
            attempt = 0
            passed = False
            while (not passed):
                try: 
                    if attempt == 0:
                        rename(filename,path.join(path.dirname(filename),name+".SC2Replay"))
                    else:
                        rename(filename,path.join(path.dirname(filename),name+" ("+str(attempt)+").SC2Replay"))
                    passed = True
                except:
                    attempt +=1

if __name__ == '__main__':   
    settings = load_settings()
    for files in listdir(unicode(settings["[replay_folder]"])):
        rename_file(path.join(settings["[replay_folder]"], files),settings)