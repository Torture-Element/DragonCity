# DragonCity龍城

[English](https://github.com/JingShing/DragonCity/blob/main/README.md) | 繁體中文

你可以在 itch.io 取得這個遊戲 : https://jingshing.itch.io/dragoncastle

## Update更新

### ver 1.0:

- 包含 5 個武器 和 2 個魔法。 5 種怪物。 和 讀取地圖的系統。
- 血條、魔力條、和升級系統。

```
方向鍵移動
Q 切換武器
E 切換魔法
空格 使用武器
左_ctrl 使用魔法
M 打開升級選單
P 暫停遊戲
```

### ver1.1:

- 新增新方法 : resource_path(path)
- 將資源一起打包到exe中

### ver 1.2:

- 玩家死亡會重置場景
- 玩家生成會自帶無敵時間，自身會閃爍。
- 玩家死亡會掉落一半的經驗值
- 新增體力系統和虛脫標誌
- 死亡不再損失能力值
- 修復並優化體力系統 : 在體力為負時會變為最大值的問題修復
- 新增翻滾 ： 按 shift 翻滾

### ver 1.3:

- 新增 npc 和 召喚物

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
