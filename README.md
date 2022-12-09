# BluePot

<p align="center">
<img src="https://raw.githubusercontent.com/j4n7/bluepot/master/src/img/potion.png?raw=true" alt="LOLFF15 Logo" width="32" height="32">
</p>

<p align="center">
<i>Regenerates 3.33 mana every 0.5 seconds over 15 seconds, restoring a total of 100 mana.</i>
</p>
<br>

BluePot is an **unofficial framework** written in Python which is meant to extract data from **League of Legends**. It allows you to retrieve information that is not normaly available using the official Riot API.

It accomplishes this by passively **reading memory** from the League of Legends process. This is a process that currently falls into a **gray area** because Riot doesn't have an explicit and clear developer policy regarding this issue. We only have this [old Tweet](https://twitter.com/gchorba/status/1350180195051794432) by an ex-Riot employee.

Its possibilities are unlimited but it is currently **under development** and only some basic features are available.

Information about its use via Python scripting is scarce and you would have to dig into the code if you want have a better understanding about how everything works. In the future I would like to implement more user friendly classes and methods that are also accompanied by better documentation.

Currently BluePot is released as a **Windows Exectuable** that implements an overlay that features a **jungle path chronometer**. You can get the last release [here](https://github.com/j4n7/bluepot/releases).



## Who is this tool for

- Data analysts who want to get more quality data about the game
- Third-party app developers that need a base to build their applications
- Thech savvy LOL players that want to know more about how the game works internally
- LOL players that want to see more tools implemented that can help them improve in the game
- The LOL community in general, that needs to be able to access some functionalities that are only available by using third-party applications with obscure policies



## Jungle Path Chronometer

BluePot Windows Exectuable provides an **overlay that features a jungle path chronometer**.

You can get the last release from **[here](https://github.com/j4n7/bluepot/releases)** (EXE version).

<p align="center">
<img src="https://i.ibb.co/55pdhWg/chrono-overlay-example.png" alt="chrono-overlay-example" border="0">
</p>

<p align="center">
<img src="https://i.ibb.co/ZzrSs36/Blue-Pot-Tray-Icon.png" alt="Blue-Pot-Tray-Icon" border="0">
</p>

This allows measuring the time it takes to clear each camp individually and also the time it takes moving between them. Thus, this information can help you improving your jungle pathing by knowing in what stages you could perform better.

It automatically detects when you start and finish your jungle path and is very easy to reset a certain stage or stages so you can train that specific part to get your desire time.

This saves you the tedious task of having to fully start from the beginning.

You can easily save this information for tracking your own progress but also for sharing it with other players.

***Take into account that it only registers 6 camps at maximum and crabs, drakes, herald and baron are excluded.***

<p align="center">
<iframe width="560" height="315" src="https://www.youtube.com/embed/7N-pLBgOYVw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</p>



## How to use the Jungle Path Chronometer

**This Jungle Path Chronometer is only meant to be used in the Practice Tool.**

Please, first be sure that inside the "Video tab" from the LOL ingame settings you have **"Window mode"** selected as "Borderless" (default) or "Windowed".

Whenever you want to use BluePot, just double click the program icon and it will automatically appear on your Windows System Tray.

If you want to exit from the application, just double click the system tray icon or right click it and select the appropriate option.

The moment you start attacking or interacting with a jungle monster the chronometer will automatically start.

You can reset it at any moment by clicking the button **Reset** at the right top corner.

You can also export your current times by clicking the buttton **Export** at the top. It will pop up a save dialog where you can choose the name and location of the **.txt file**. This file will could be furtherly edited to store some more useful information such as Smite locations or other comments. Here is an example of such file:

```
-----------------------------
Created by BluePot
Player name: <fill>
-----------------------------
LOL version: 12.23
Champion name: Nocturne
-----------------------------
Starting side: <fill>
Number of camps: 6
-----------------------------


---------------------------------------------------------
CAMPS     COLOR     START     END       TOTAL     SMITE  
---------------------------------------------------------
Blue      Blue      0:00.00   0:25.61   0:25.61
---------------------------------------------------------
M1                  0:25.61   0:28.24   0:02.63
---------------------------------------------------------
Gromp     Blue      0:28.24   0:46.72   0:18.48
---------------------------------------------------------
M2                  0:46.72   0:53.07   0:06.35
---------------------------------------------------------
Wolves    Blue      0:53.07   1:06.72   0:13.65
---------------------------------------------------------
M3                  1:06.72   1:18.94   0:12.22
---------------------------------------------------------
Raptors   Blue      1:18.94   1:31.16   0:12.22
---------------------------------------------------------
M4                  1:31.16   1:34.87   0:03.71
---------------------------------------------------------
Red       Blue      1:34.87   1:53.67   0:18.80
---------------------------------------------------------
M5                  1:53.67   1:58.60   0:04.93
---------------------------------------------------------
Krugs     Blue      1:58.60   2:08.22   0:09.62   Yes
---------------------------------------------------------
TOTAL                         2:08.22   3:38.22*
---------------------------------------------------------

* Starting at 1:30
```



## Advantages of the Jungle Path Chronometer

- No bloatware

- No ads

- Completely free

- Open source

- Minimal weight (17 MB)

- Self-executable (no need to install it)



## Will my LOL account get banned for using BluePot?

As I have previously mentioned in the beginning, reading memory from the League of Legends process falls in a gray area.

BluePot doesn't inject information directly into the League of Legends process neither uses any kinds of hooks. It doesn't execute internal game functions or methods. 

This means it doesn't directly interfere with League of Legends, and as far as I know, no one should be able to tell you wether you decide or not to listen to the processes that are taking place in your private computer memory.

Take all this with a grain of salt, as I'm not a lawyer nor an expert in this kind of topics.

What I for sure know is that there are plenty of other third-party apps that are using more invasive techniques to interact with the League of Legends process. For example, it cames into my mind all the apps that create timer olverlays for jungle camps. I'm takling about Blitz.gg, u.gg, op.gg and many other applications that belong to the Overwolf ecosystem.

Needless to say, BluePot, as it is distributed, doesn't provide any means to cheat or gain an unfair advatange over other players.

***TL;DR version:*** BluePot has not yet being approved by Riot but **its banning potential should be minimal**, anyways use it at your own risk. Use it only in Practice Tool to minimize risks. And if you want to be super safe, don't use it on your main account. I do not take any responsibilities for the consequences that its use may cause.



## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

It would be amazing to see this project grow with more people and new exciting ideas.

Also, if you are a Riot employee and you took the effort to read all of this and by any remote chance you have a nice job to offer I am more than willing to listen. Specially in the area of data player behaviour analysis. Peace and love <3



## License

[MIT](https://choosealicense.com/licenses/mit/)