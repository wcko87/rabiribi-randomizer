<meta content="article" property="og:type">
<meta content="https://user-images.githubusercontent.com/27341392/29525297-bc4087d8-86c4-11e7-8c1a-235de711994d.gif" property="og:image">

# Rabi-Ribi Randomizer V2

![Rabi-Ribi Randomizer](https://user-images.githubusercontent.com/27341392/29525297-bc4087d8-86c4-11e7-8c1a-235de711994d.gif)

A Randomizer for [Rabi-Ribi](http://store.steampowered.com/app/400910/RabiRibi/). Brought to you by the [Rabi-Ribi Speedrunning Community](http://www.speedrun.com/rabiribi)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://discord.gg/dDfpNAr"><img src="https://discordapp.com/assets/f8389ca1a741a115313bede9ac02e2c0.svg" height="20">Rabi-Ribi Speedrunning Discord</a>

This program shuffles item and egg locations (among other things) around in Rabi-Ribi in such a way that all the required items are always reachable. Also optionally randomizes other things like music and backgrounds.

What the randomizer can currently randomize:
* Item and egg locations
* Map transitions
* Random Obstacles (constraint randomization)
* Music triggers
* Backgrounds

### Updates

* V2 is released! The Rabi-Ribi Randomizer V2 uses a completely new algorithm for verification. Now, the entire world of Rabi-Ribi is represented as a network of nodes (a graph), so more complicated seeds can be generated! This allows for new features like shuffling map transitions and constraint randomization.

## Who made this?

The Randomizer is not the work of one person. It is a collaborative effort of the Rabi-Ribi speedrunning community.
- [How the Randomizer came about](https://wcko87.github.io/acknowledgements/)

## Download
The following download links are automatically updated with the latest changes to the randomizer.
* [**Download** *(Randomizer with UI)*](https://ci.appveyor.com/project/wcko87/rabiribi-randomizer-ui-rc94b/build/artifacts)
   - **randomizer-ui.zip** is the stable version of the randomizer.
   - **randomizer-ui-dev.zip** is the development version of the randomizer and may contain new untested features. Use at your own risk.
* [**Download** *(command line tool, main branch)*](https://ci.appveyor.com/project/wcko87/revised-rabi-ribi-randomizer/build/artifacts?branch=master)
* [**Download** *(command line tool, development branch)*](https://ci.appveyor.com/project/wcko87/revised-rabi-ribi-randomizer/build/artifacts?branch=dev)


The randomizer is written in Python, the UI is written in C#/WPF.
* [**Source code** *(randomizer)*](https://github.com/wcko87/revised-rabi-ribi-randomizer)
* [**Source code** *(randomizer UI)*](https://github.com/AzureHakua/rabiribi-randomizer-ui)

## How to Use the Randomizer (Instructions)

These instructions will be for the Randomizer UI.
1. Download the randomizer UI and extract the files to any location you wish.
2. Find the directory which stores your Rabi-Ribi game data. Copy the map files `area0.map` to `area9.map` from `Rabi-Ribi\data\area\` into the `original_maps` folder in the randomizer.
    * Usually the Rabi-Ribi game data can be found at `C:\Program Files (x86)\Steam\SteamApps\common\Rabi-Ribi`.
3. Run the Randomizer to generate a set of modified maps. By default, the generated maps will be placed in the `generated_maps` folder. You can also configure your own output location for the modified maps.
4. Create a new folder (e.g. `randomizer`) in the `Rabi-Ribi\custom\`  directory. Copy the generated map files into that directory (`Rabi-Ribi\custom\randomizer\`).
5. Start Rabi-Ribi, press F5, and select `randomizer` (or whatever you decided to name the folder).
6. Start a new game, preferably in Speedrun Mode.

Note: This should be played on Rabi-Ribi 1.85 and above. Randomizer should be played from the custom maps option, and not by replacing the default maps.

## Randomizer Gameplay

The Randomizer has a lot of different options. The Randomizer can be used in any way you want, but there are a few common modes that are often played by the speedrunning community.

### Egg Goals Mode

In Egg Goals mode, hard-to-reach items will be easter eggs. By default, 5 eggs will be chosen to be hard-to-reach. All other eggs will be removed from the map.

* Use the "Extra Eggs" option to add in X number of randomly-placed extra eggs back into the map.
* The total number of hard to reach eggs + extra eggs cannot be made more than the number of eggs included in the shuffle.

* Usually, we play with 5 hard to reach eggs, and 2 extra eggs, for a total of 7 eggs. The goal is to obtain 5 eggs to win.

### Hard to Reach Items Mode

If Egg Goals mode is turned off, the randomizer will mark some items (default: 5) as hard-to-reach. The objective is to obtain these hard-to-reach items.


### Complete the Game

Note that because the entire game is completable on 0%, completing the game on randomized maps isn't much of a challenge.

However, if constraint randomization or map transition shuffle are turned on, it is possible that the game may end up uncompletable (either by having too many unreachable bosses or by having rabi rabi town unreachable). Having a mode that ensures the game is always completable will be supported in the near future.


## Randomizer Options

#### Item Randomization
Item randomization is always on by default. Only items in the `to_shuffle` list in the config will be shuffled. See the section on `config.txt` for more information.

#### Shuffle Map Transitions
* `--shuffle-map-transitions`

This mode shuffles the 13 map transition in Rabi-Ribi. For example, walking left from starting forest may cause you to end up in the right side of natural aquarium.

Shuffling map transitions can sometimes make entire areas unreachable (including Rabi Rabi Town).

#### Constraint Randomization
* `--constraint-changes 15`

This option introduces random obstacles, which can obstruct entire areas of the world, until you have specific movement items to get around these obstructions.

Constraint randomization can sometimes make entire areas unreachable (including Rabi Rabi Town).

Note: Setting constraint changes to 15, for example, does not mean there will always be 15 constraint changes. The actual number will be random, but will be 15 on average.

Additional Information:
* Generally, randomized constraints will block off areas, not open up new paths.
* Randomized constraints usually block off entire areas rather than specific item locations
* The block type of generated blocks will always be obvious. Hammer blocks are made of wood, bomb blocks are similar to those after cocoa1, fire orb blocks will be ice blocks, and collapsible blocks will be those seen in ravine. All other block types are walls.


#### Shuffle Gift Items
* `--shuffle-gift-items`

This option shuffles the two items given to you by Miriam (Speed Boost, Bunny Strike), and the item given to you by Mr. Tako (P.Hairpin).

Speed Boost's and Bunny Strike's locations will be in a room behind Miriam's shop (Bunny Strike requires Sliding Powder), while P. Hairpin's location will be visible from Mr. Tako's room in Plurkwood (you can only pick it up after defeating Keke Bunny).


#### Music Shuffle
* `--shuffle-music`

Shuffles the music triggers in the map. Does not actually affect gameplay.


#### Background Shuffle
* `--shuffle-backgrounds`

Shuffles backgrounds in the map, making Rabi Rabi Island look crazy. Also shuffles minimap colors. Does not affect gameplay (in theory).

Note: Some backgrounds can make the game significantly more difficult. A few examples:
* The spectral cave background makes all tiles invisible (other than layer 2 and 6 tiles). This means you may have to navigate invisible maps.
* The library background can make areas difficult to see, as the tiles periodically phase out.
* The evernight dark passageway background turns all tiles black, which makes things difficult to see. 
* The background with water in the foreground can sometimes obscure items.

The **No Difficult Backgrounds** (`--no-difficult-backgrounds`) option can be used to disable backgrounds that obstruct visibility or otherwise makes things more difficult.

The **No Laggy Backgrounds** (`--no-laggy-backgounrds`) option can be used to disable backgrounds that can cause lag (for example, seana's disco party arena and spectral cave)


#### Super/Hyper Attack Mode
* `--super-attack-mode`, `--hyper-attack-mode`

Super attack mode starts you with 20 attack ups. Hyper attack mode starts you with 30 attack ups.

This gives you a lot more damage, which is especially useful because you often don't get the hammer early in randomizer games. (Ribbon does about 20 damage per shot in super attack mode)


#### Open Mode
* `--open-mode`

Normally, Rabi-Ribi blocks off many areas during Prologue using prologue triggers which prevent you from going further. Open mode removes these prologue triggers, so that you can go anywhere you want, even in prologue.

Note that:
* Chapter 1 is still required to open up Cocoa Cave, spawn the Cicini spring, and spawn Chocolate.
* Chapter 2 and Cicini are still required to enter the Exotic Laboratory.
* Chapter 3 is still required to enter System Interior.


## Difficulty Configuration (config.txt)

In addition to the options offered in the UI, the randomization can be further configured by modifying the `config.txt` file.
* Note that `//` denotes a comment. Anything after the `//` will be ignored.


### Difficulty and Knowledge

* `ADVANCED_TRICKS_REQUIRED`: There are many tricks in the game that requires advanced knowledge of how the game works to perform. Turning off this flag removes the need for some of the more advanced tricks to obtain all the required items.
  * `STUPID_HARD_TRICKS`: There are some tricks that we consider ridiculous, even for speedrunners. Keeping this flag off removes the need for any of these tricks to be performed. We recommend keeping this off to preserve sanity.


### Settings

* The first part of the `config.txt` file looks like this:
  ```
  // Configure generation flags here
  "settings": {
      "DARKNESS_WITHOUT_LIGHT_ORB": true,
      "ZIP_REQUIRED": true,
      "SEMISOLID_CLIPS_REQUIRED": true,
      "BLOCK_CLIPS_REQUIRED": true,
      "PLURKWOOD_REACHABLE": true,
      "POST_GAME_ALLOWED": false,
      "POST_IRISU_ALLOWED": false,
      "HALLOWEEN_REACHABLE": false,
      "WARP_DESTINATION_REACHABLE": false,
      "EVENT_WARPS_REQUIRED": true,
  },
  ```
  In here, you can set the flags used by the item shuffle.

  ##### DARKNESS_WITHOUT_LIGHT_ORB
  If this flag is true, the game might expect you to go into dark areas, even if you don't have the Light Orb.

  ##### ZIPS_REQUIRED
  Zips are glitches that allow you to clip through terrain. The main types of zips are slide zips and hammer roll zips. If this flag is turned on, reaching some of the items may require zips to be performed. If turned off, all the required items can be obtained without the need for zips.

  ##### SEMISOLID_CLIPS_REQUIRED
  Semisolid Clips refers to clipping through semisolid (one-way) platforms via a specific glitch. If this flag is turned on, reaching some of the items may require semisolid clips to be performed. If turned off, all the required items can be obtained without the need for semisolid clips.

  ##### BLOCK_CLIPS_REQUIRED
  Block clips are performed by quick-dropping onto the top of a one-tile block to obtain the item inside the block. Turning off this flag removes the need for block clips.

  ##### PLURKWOOD_REACHABLE, POST_GAME_ALLOWED, POST_IRISU_ALLOWED, HALLOWEEN_REACHABLE, WARP_DESTINATION_REACHABLE
  These flags determine whether it is required to enter these areas/chapters to obtain all the required items. For example, turning `POST_GAME_ALLOWED` off means that there is no need to enter post-game to obtain the requried items.

  ##### EVENT_WARPS_REQUIRED
  Some events in the game warp you to other locations. This gives you access to new areas. See the event warps section below for more information. Turning on this flag means you might be required to use these warps to obtain the required items.

### Addtional Items List

* The next part of the config file is the `additional_items` list.
  ```
  "additional_items": [
      "SPEED_BOOST",
      "SOUL_HEART",
      ...
      "COCOA_BOMB",
  ],
  ```
  These additional items will be added into the item shuffle (and replace eggs). These usually means that there are two ways to obtain these items - by picking them up or by their original method (e.g. you can either pick up a cocoa bomb, or buy one from Cocoa).


### To Shuffle List

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

### Must be Reachable List

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

## Map Changes to Prevent Getting Permanently Trapped

Minor changes have been made to prevent the player from being permanently stuck. Note that you are only permanently stuck if you have been autosaved in a location which you cannot exit from. If you are able to quick-reload to escape, you are not stuck.

These map changes can be turned off by the "No Fixes" (--no-fixes) option.

### Removal of Autosaves
* At the entrace to Cocoa1, the save point has been removed, and the autosave point has been moved to the top of the ledge.
* The save point at the sliding powder location in exotic laboratory has been removed.
* Warp Stones are active from the start, instead of only after viewing the cutscene one room after the ribbon fight.
  * This means that you no longer need to walk right after fighting ribbon, and can go straight back to the warp.
  * This prevents a softlock when Rabi Slippers or Air Jump is picked up before the cutscene, disabling the cutscene and leaving you stuck in Spectral Cave without the ability to warp out.


### Event Warps
Some events in the game warp you to other locations. This gives you access to new areas. These are the useful event warps in the game:

1. Defeating starting forest UPRPRC sends you to Rabi Rabi Beach.
2. Defeating Cicini sends you to Rabi Rabi Ravine.
3. Going to town after clearing Chapter 1 and recruiting Cicini sends you to Golden Riverbank.
4. Defeating Keke Bunny and using Mr. Tako's computer sends you to Rabi Rabi Town.

While these are not really useful in the base game, with map transition shuffle and constraint randomization, these event warps may be the only way to enter these areas. If EVENT_WARPS_REQUIRED is on, you may be required to use these event warps to reach your goals.

However, for event warps 1, 2 and 3 above, you can only use it once per playthrough. Therefore, you can potentially be locked out of the warps. (Note: you can use the computer in Plurkwood to warp to town as many times as you want).

To fix this, we make some changes to the maps to allow you to repeat these event warps as many times as you like. The following changes are made:
1. There is a door in starting forest. Using that door sends you to a room where you can re-fight the forest UPRPRC battle if you have already met the pre-conditions (Ribbon) for it. This sends you to beach again.
2. After beating Cicini, you can enter a hidden room behind her boss arena, which has a warp to ravine.
3. There is a strange door in town that can be used to manually trigger the cutscene that warps you to riverbank (if you have already met the pre-conditions for the cutscene).


## Rabi-Ribi Platforming Tricks Tutorial
For those interested in learning some of the more advanced tricks used in Randomizer / Speedruns, there is a tutorial map showcasing most of the platforming tricks we use.
* More information can be found here: [Platforming Tricks Tutorial](https://wcko87.github.io/rabi-ribi-maps/maps/platforming_tricks_tutorial/)
