import re

f = r'C:\vic_movie_misc\pickers\halvar_facial_mel\001\halvar_original_facialpicker.mel'

sourceHandle  = open(f,'r')
sourceContent = sourceHandle.readlines()
sourceHandle.close()

lines = []

for l in sourceContent:
    res = re.search(r'\b%s\b' % (re.escape("Main")), l)
        
    if res:
        print(l)
        if '"Main"' in l:
            l = l.replace('"Main"', '"loc_ctrl"')
        
        if '"Main:"' in l:
            l = l.replace('"Main:"', '"loc_ctrl:"')
        
        if '"Main\\' in l:
            l = l.replace('"Main\\', '"loc_ctrl\\')
        
        if '"*Main"' in l:
            l = l.replace('"*Main"', '"*loc_ctrl"')
            
        if '"*Main.*"' in l:
            l = l.replace("*Main.*", "*loc_ctrl.*")
        
        if '":Main"' in l:
            l = l.replace(":Main", ":loc_ctrl")
        
        if '"Main.' in l:
            l = l.replace('"Main.', '"loc_ctrl.')
        
        print(l)
    
    lines.append(l)

destHandle = open(f.replace(".mel","_fixe.mel"),'w')
destHandle.writelines(lines)
destHandle.close()