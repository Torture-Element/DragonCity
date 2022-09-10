# DragonCity龍城

You can get this game on itch.io : https://jingshing.itch.io/dragoncastle

## Update

### ver 1.0:

- completed 5 weapon & 2 magic. 5 monsters. and load map method.
- UI has hp and mp bar. and upgrade menu system.

```
arrow key to move.
q to change weapon.
e to cheange magic.
space to use weapon.
L_ctrl to use magic.
M to open upgrade_menu.
P to paused game.
```

### ver1.1:

- with new import method : resource_path(path)
- now the game can be pack all assets and script into one exe.

### ver 1.2:

- player died will reset the scene.
- player spawn with invincible time. with flicker.
- player died will drop half exp
- add stamina system and tired flag
- dead will not drop stats
- fix and improve stamina system : somehow you reduce stamina to negative it will change to maxinum.
- add roll system: press shift to roll

### ver 1.3:

- add npcs and minions

- minion is in magic and has cat type.
- improve collision : monster has collison with monster,  minion has collison with minion, big collision object has no collsion with same type object
- fixed : recover method error -> full bar turn to empty
- fixed : big monster push little monster out boarder
- improved: menu & title screen -> with alpha changed and button works
- improved: every ui bar-> hp, mp, stamina with dark souls style
- set new icon and new caption
- now player has dead screen as menu

### ver 1.4:

- improved camera:

- w, a, s, d to control camera and alse mouse can control camera move

\# mouse control camera isn't put in game ver
-, + to use scale. also can use mouse wheel.
esc to quit game

### ver 1.4.1

- removed scale map feature. since some camera feature too lag.

- if need more camera feature plz use 1.4

### ver 1.4.2:

- back to 1.4.

- find the lag reason: scale module. internal_surface_size need to be limited in 2000 X 2000
- now the fps is normal back to around 60

### ver 1.5:

- save and load system basic : player info

- add load and save menu button
- fixed: player refresh function error. it makes health and mp bar animtaion failed.
- improved: walk no longer cost stamina.
- improved: idle will recover more energy. but walk recover slower than usual.
- improved: esc became menu key. and n key got removed.
- add npc. if npc can talk it will apear bubble icon.
- add npc dialog box. player now can talk to npc.
  -> player use t to talk. use enter to continue dialog. can pressed enter to skip dialog.
- improved: text box can go multiple line

### ver 1.5.1:

fixed dialog box multi-line bug.

### ver 1.5.2:

- add text outline function.
- add press 'T' to talk hint. hint will change if start a dialog box.
   -> press 'enter' to continue
- change u to upgrade.
- change z to attack.
- change m to mute music.
- add fullscreen function -> press f to fullscreen

release first version  DragonCastle152

### ver 1.5.3:

- add dialog npc icon.
- add two language select: chinese and english
- add npc speak sound

### ver 1.5.5:

- add full screen back
- add shader change
- add multiple window feature

### ver 1.5.6

* Fixed chinese font bug.
