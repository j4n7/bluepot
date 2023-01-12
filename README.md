
# BluePot


![LOL Patch](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fj4n7%2Fbluepot%2Fdevelop%2Fdata%2Fbadge.json)


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

You may check it out in this **[YouTube video](https://www.youtube.com/watch?v=eNIXUO_p6cw)**.

You can get the last release from **[here](https://github.com/j4n7/bluepot/releases)** (EXE version).

<p align="center">
<img src="https://i.ibb.co/55pdhWg/chrono-overlay-example.png" alt="chrono-overlay-example" border="0">
</p>

<p align="center">
<img src="https://i.ibb.co/ZzrSs36/Blue-Pot-Tray-Icon.png" alt="Blue-Pot-Tray-Icon" border="0">
</p>



## Why use the Jungle Path Chronometer?

- Compare your clears in real time with the ones made by pro-players and see where you are not being efficient. New champions and clear times will be added in the future.

- Measure the time it takes to clear each camp individually and also the time it takes moving between them. This information can help you improve your jungle pathing by knowing in what stages you could perform better.

- You can manually spawn jungle monsters inside the Practice Tool before their default spawning time and the Jungle Path Chronometer will adjust the time for you. This way you won't need to wait any time before you can start practicing your desired jungle clear.

- Everytime you restart the game, the Jungle Path Chronometer will automatically reset and it will track time relatively to the new clear. By default, the Practice Tool doesn't reset the game clock so it can be hard to calculate your times. This tool solves this problem.

- You can easily save this information for tracking your own progress but also for sharing it with other players.

***Take into account that it only registers 6 camps at maximum and crabs, drakes, herald and baron are excluded.***



## How to use the Jungle Path Chronometer

**This Jungle Path Chronometer is only meant to be used in the Practice Tool.**

Please, first be sure that inside the "Video tab" from the LOL ingame settings you have **"Window mode"** selected as "Borderless" (default) or "Windowed".

Whenever you want to use BluePot, just double click the program icon and it will automatically appear on your Windows System Tray.

If you want to exit from the application, just double click the system tray icon or right click it and select the appropriate option.

The moment you start attacking or interacting with a jungle monster the chronometer will automatically start.

You can reset it at any moment by clicking the button **Reset** at the right top corner.

You can also export your current times by clicking the buttton **Export** at the top. This will create a file called **Clears.csv** or append new rows to it. This way you can track your current times for each camp. and compare between clears. Before saving you can **click the names** of the camps to mark the ones you have smited.



## Hotkeys for the Jungle Path Chronometer

**Stop** [Pause key]: this manually stops the camp timer. This can be useful, for example if you want to time the last hit of a monster before it dies.

**Reset** [Backspace key]: this restarts the chronometer, erasing all the stored information. Can be useful to start a new run. There is also a button at the top of the overlay.

BluePot comes along with a **hotkeys_settings.txt file**. You can modify its contents (e.g. Windows Notepad) to assign different hotkeys for these functions. This file has to be in the same directory as the Executable file, otherwise changes won't apply.



## Other advantages of the Jungle Path Chronometer

- No bloatware

- No ads

- Completely free

- Open source

- Minimal weight (~20 MB)

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



---
BluePot isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc.