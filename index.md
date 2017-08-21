# Rabi-Ribi Randomizer

![Rabi-Ribi Randomizer](https://user-images.githubusercontent.com/27341392/29525297-bc4087d8-86c4-11e7-8c1a-235de711994d.gif)

A Randomizer for [Rabi-Ribi](http://store.steampowered.com/app/400910/RabiRibi/). Brought to you by the [Rabi-Ribi Speedrunning Community](http://www.speedrun.com/rabiribi)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://discord.gg/dDfpNAr"><img src="https://discordapp.com/assets/f8389ca1a741a115313bede9ac02e2c0.svg" height="20">Rabi-Ribi Speedrunning Discord</a>

What the randomizer can currently randomize:
* Item and egg locations
* Music triggers
* Backgrounds

## Download
The following download links are automatically updated with the latest changes to the randomizer.
* [**Download** *(Randomizer with UI)*](https://ci.appveyor.com/project/wcko87/rabiribi-randomizer-ui-rc94b/build/artifacts)
   - **randomizer-ui.zip** is the stable version of the randomizer.
   - **randomizer-ui-dev.zip** is the development version of the randomizer and may contain new untested features. Use at your own risk.
* [**Download** *(command line tool, main branch)*](https://ci.appveyor.com/project/wcko87/rabiribi-randomizer/build/artifacts?branch=master)
* [**Download** *(command line tool, development branch)*](https://ci.appveyor.com/project/wcko87/rabiribi-randomizer/build/artifacts?branch=dev)


The randomizer is written in Python, the UI is written in C#/WPF.
* [**Source code** *(randomizer)*](https://github.com/wcko87/rabiribi-randomizer)
* [**Source code** *(randomizer UI)*](https://github.com/AzureHakua/rabiribi-randomizer-ui)

## Basic Instructions

These instructions will be for the Randomizer UI.
1. Download the randomizer UI and extract the files to any location you wish.
2. Find the directory which stores your Rabi-Ribi game data. Copy the map files `area0.map` to `area9.map` from `Rabi-Ribi\data\area\` into the `original_maps` folder in the randomizer.
    * Usually the Rabi-Ribi game data can be found at `C:\Program Files (x86)\Steam\SteamApps\common\Rabi-Ribi`.
3. Run the Randomizer to generate a set of modified maps. By default, the generated maps will be placed in the `generated_maps` folder. You can also configure your own output location for the modified maps.
4. Copy the generated map files back into the `Rabi-Ribi\data\area\` directory.
5. Start Rabi-Ribi normally to play on the randomized maps.

Note: We recommend playing on Rabi-Ribi Version 1.8. This is because of one change to the Fire Orb item location. The exit from the Fire Orb room now requires the Fire Orb, instead of bombs. The Randomizer's item shuffle makes use of this.

## Item Shuffle

* The main feature of the Rabi-Ribi randomizer is the item shuffle. Item (and egg) locations are shuffled in such a way that all items specified in the config will be reachable.
* The difficulty rating shown is an indicator of how difficult it is to find the marked hard-to-reach items.

The challenge is to obtain the items marked as "Hard-to-Reach" by the randomizer.
* Most of the time, getting all these items requires knowledge of advanced tricks. Getting these items will test your knowledge of the game's many tricks and glitches.
* Advanced tricks and glitches can be turned off via the `config.txt` file, which is explained below.

Of course, you can do whatever you want with the randomized maps instead. Note that because the entire game is completable on 0%, completing the game on randomized maps isn't much of a challenge.

### Egg Goals Mode

The randomizer features an alternate mode, named Egg Goals.

In Egg Goals mode, instead of having hard-to-reach items, the hard-to-reach items will be easter eggs. Up to 5 eggs will be chosen to be hard-to-reach items. All other eggs will be removed from the map.

* Use the "Extra Eggs" option to add in X number of randomly-placed extra eggs back into the map.
* The total number of hard to reach eggs + extra eggs cannot be made more than the number of eggs included in the shuffle.

### config.txt

In addition to the options offered in the UI, the item randomization can be further configured by modifying the `config.txt` file.
* Note that `//` denotes a comment. Anything after the `//` will be ignored.

* The first part of the `config.txt` file looks like this:
  ```
  // Configure generation flags here
  "settings": {
      "ZIP_REQUIRED": false,
      "ADVANCED_TRICKS_REQUIRED": true,
      "BLOCK_CLIPS_REQUIRED": true,
      "POST_GAME_ALLOWED": false,
      "STUPID_HARD_TRICKS": false,
      "POST_IRISU_ALLOWED": false,
      "HALLOWEEN_REACHABLE": false,
      "WARP_DESTINATION_REACHABLE": false,
  },
  ```
  In here, you can set the flags used by the item shuffle.
  * `ZIPS_REQUIRED`: Zips are glitches that allow you to clip through terrain. The main types of zips are slide zips, hammer roll zips and semisolid clips. If this flag is turned on, reaching some of the items may require zips to be performed. If turned off, all the required items can be obtained without the need for zips.
  * `ADVANCED_TRICKS_REQUIRED`: There are many tricks in the game that requires advanced knowledge of how the game works to perform. Turning off this flag removes the need for some of the more advanced tricks to obtain all the required items.
  * `BLOCK_CLIPS_REQUIRED`: Block clips are performed by quick-dropping onto the top of a one-tile block to obtain the item inside the block. Turning off this flag removes the need for block clips.
  * `STUPID_HARD_TRICKS`: There are some tricks that we consider ridiculous, even for speedrunners. Keeping this flag off removes the need for any of these tricks to be performed. We recommend keeping this off to preserve sanity.
  * `POST_GAME_ALLOWED`/`POST_IRISU_ALLOWED`/`HALLOWEEN_REACHABLE`/`WARP_DESTINATION_REACHABLE`: These flags determine whether it is required to enter these areas/chapters to obtain all the required items. For example, turning `POST_GAME_ALLOWED` off means that there is no need to enter post-game to obtain the requried items.

* The next part of the config file is the `to_shuffle` list.
  ```
  // Only these items will be shuffled
  "to_shuffle": [
      "AIR_DASH",
      "AIR_JUMP",
      ...
      "EGG_VOLCANIC_NE",
  ]
  ```
  Only the items listed in this list will be shuffled. All other items will remain in their original locations.

* The next part of the config file is the `must_be_reachable` list.
  ```
  // All these items must be reachable
  "must_be_reachable": [
      "AIR_DASH",
      "AIR_JUMP",
      ...
      "WATER_ORB",
  ]
  ```
  Earlier on, the term "required items" was mentioned multiple times. Required items refers to the `must_be_reachable` list. The randomizer will always generate a randomization that ensures that all the items in this list will be reachable.
  * Note that if the `POST_GAME_ALLOWED` flag is turned off, the randomizer will treat any item reachable only in post game as "unreachable", and will report it as such. This also applies to the other flags which remove areas/chapters from the randomization requirements.

### Map Changes to Prevent Getting Permanently Trapped
Minor changes have been made to prevent the player from being permanently stuck. Note that you are only permanently stuck if you have been autosaved in a location which you cannot exit from. If you are able to quick-reload to escape, you are not stuck.
* At the entrace to Cocoa1, the save point has been removed, and the autosave point has been moved to the top of the ledge.
* The save point at the sliding powder location in exotic laboratory has been removed.
* Warp Stones are active from the start, instead of only after viewing the cutscene one room after the ribbon fight.
  * This means that you no longer need to walk right after fighting ribbon, and can go straight back to the warp.
  * This prevents a softlock when Rabi Slippers or Air Jump is picked up before the cutscene, disabling the cutscene and leaving you stuck in Spectral Cave without the ability to warp out.

