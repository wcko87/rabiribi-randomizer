[![Build status](https://ci.appveyor.com/api/projects/status/wv15wfiegbymmyg3/branch/dev?svg=true)](https://ci.appveyor.com/project/wcko87/rabiribi-randomizer/branch/dev)

<a href="https://discord.gg/dDfpNAr"><img src="https://discordapp.com/assets/f8389ca1a741a115313bede9ac02e2c0.svg" height="30">Rabi-Ribi Speedrunning Discord Server</a>

# Rabi-Ribi Randomizer
Randomizes items in Rabi-Ribi maps.
* Refer to the [Rabi-Ribi Randomizer Website](https://wcko87.github.io/rabiribi-randomizer/) for more information.

This page is for the command-line tool. A [UI for the randomizer](https://github.com/AzureHakua/rabiribi-randomizer-ui) has also been developed.
* [Download (Randomizer UI)](https://ci.appveyor.com/project/wcko87/rabiribi-randomizer-ui-rc94b/build/artifacts)
* [Download (command line tool)](https://ci.appveyor.com/project/wcko87/rabiribi-randomizer/build/artifacts?branch=dev) [branch: dev]

### How to use
Here's a 1-minute guide to how to run the randomizer. I probably won't make a proper guide for this since we have a UI now. Go check out the UI instead. If you want command line, you can try `RabiRibiRandomizer.bat --help` or `bin\itemrandomizer.exe --help` for help.

1. download randomizer from above link
2. put original maps into original_maps folder
3. create folder called generated_maps (next to the original maps folder)
4. run RabiRibiRandomizer.bat

The randomized maps can now be found in the generated_maps folder.

You can modify `config.txt` to choose which items you want to shuffle (along with some other settings)
