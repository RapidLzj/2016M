# SAGE Sky Survey
# Pipeline (Version 2016M)

*Jie Zheng* [_jiezheng(a)nao.cas.cn_]

*Start this plan from 2016M, 
at Steward Observatory, UofA, Tucson, AZ*

## Program Structure

|Directory  |Content|
|:----------|:------|
|`./`       |Root of system.Caller code for debug and execute.|
|`./pb_*.py`|Pipeline caller for Bok.|
|`./px_*.py`|Pipeline caller for NOWT.|
|`./args.py`|Functions for commandline arguments process.|
|`./bok`    |Pipeline code for bok. Use `import bok` to import.|
|`./xao`    |Pipeline code for xao. Use `import xao` to import.|
|`./common` |Common part of pipeline, can be used by all telescopes.|

In each telescope directory, we have:

|File          |Task|
|:-------------|:---|
|`__init__`    |Package initializer, make the irectory into a package|
|`rm_os`       |Overscan corrector, a function called|
|`biasflat`    |Bias merger and flat merger, two functions in one file|
|`rm_biasflat` |Bias and flat correction, and split into section files|
|`photometry`  |Photometry extractor|
|`astrometry`  |Astrometry regress|
|`magcalibrate`|Mag calibration|
|`report`      |Report generation|

If a function is common for all telescopes, we will put it into package `common`, else into telescope package.

## Data File Structure

All data in directory `/data/`.

### Raw data

`/data/raw/` is root for raw data. For security reason, this is writable only for `raw` account, readonly for others. We use `~` to present it in this section.

#### Bok data

+ `~/bok/`
    Bok telescope directory. Bok has different structure from others.
+ `~/bok/band/`
    For bok data, we orginize by different band (filter), we now have *u* and *v*, SAGE v will be placed in *sv*
+ `~/bok/b/run/`
    Run directory, currently run name is yyyymmX format, if we have more runs in one month, a postfix A, B, and etc will be used.
+ `~/bok/b/run/Jxxxx/`
    Day directory.
+ `~/bok/b/run/yyyymmdd/`
    Alias of day directory, a symbolic link.
+ `~/bok/b/run/Jxxxx/bias/`
    Directory contains bias files. Since bias files are shared among different filters, so we keep it in a sepcial band `o`. This is a virtual band, contains only bias.
+ `~/bok/b/run/Jxxxx/flat/`
    Directory for flat files
+ `~/bok/b/run/Jxxxx/good/`
    Directory for good survey files. Objects of survey files are survey fields, their names are whole digital.
+ `~/bok/b/run/Jxxxx/other/`
    Directory for other good files. They have objects with non-whole digital names, for eg `M67`.
+ `~/bok/b/run/Jxxxx/bad/`
    Directory for bad files. For eg, fits with wrong operation.
+ `dxxxx.xxxx.fits`
    Observed fits files. First xxxx is last 4-digit of mjd, and next is serial number in this night.

#### NOWT data

+ `~/xao/` Base directory of NOWT. NOWT data will not be divided into different filter, just keep their original structure from server.
+ `~/xao/run/`
    Run directory of NOWT. Run name rule is same as bok.
+ `~/xao/run/yyyymmdd/`
    Day directory.
+ `~/xao/run/yyyymmdd/BIAS/`
    Bias data.
+ `~/xao/run/yyyymmdd/FLAT/`
    Flat data. Twilight flats, if weather is not good, this may be empty.
+ `~/xao/run/yyyymmdd/uvby_survey/`
    Survey data.
+ `~/xao/run/yyyymmdd/uvby_survey/object/`
    Survey object dir. NOWT data is orgnized in objects.
+ `object_filter_utctime_expt_sn.fits`
    File name rule at NOWT. Valid filter codes are `u`, `v`, `b`, `y`, `Hw`, `Hn`, `g`, `r` and `i`. For bias, filter may be omitted. UTC time format is yyyymmddhhmmss. Exposure time in format like 30s. Sn is serial number in this night.

#### INT and MAO data

INT data is only for some special topic, so will not be discussed here.

MAO data file structure and file name rule are still unknown.

### Reduced data

`/data/red/` is root of reduced data. Structure of all telescope is same, so we take bok as example.

+ `~/bok/` Telescope root.
+ `~/bok/u/` Band (filter) directory.
+ `~/bok/u/passx/` xth pass of reduction.
+ `~/bok/u/pass1/run/` Run directory.
+ `~/bok/u/pass1/run/Jxxxx/` Day directory.
+ `~/bok/u/pass1/run/Jxxxx/list/` Dir for list files, there are bias.lst, flat.lst, good.lst, other.lst, and bad.lst inside. All list files have 2 columns, 1st is directory of file, and 2nd is bare filename without extension name `.fits`.
+ `~/bok/u/pass1/run/Jxxxx/bias.fits` Merged bias file. In band `o` is real file, and in other filters are links to `o`.
+ `~/bok/u/pass1/run/Jxxxx/flat.fits` Merged flat files. For bok, this is dome-flat, for nowt, this is twilight flat. If no twilight, this file is not present, we need to apply flat from other night. If we have superflat, it will be another name.
+ `~/bok/u/pass1/run/Jxxxx/good/` Good or other, for different type of files.
+ `~/bok/u/pass1/run/Jxxxx/good/xxxx` Directory for raw file xxxx, use its original bare name.

In reduced dir, we have a set of files come from different steps.

Reduced file name rule: `xxxx[.version].content.ext`

+ `xxxx`: File bare name.
+ `version`: Reduction version, if version is default (none), the point is also omitted.
+ `ext`: File type extensions, standard or our self-defined.
    - `txt`, `jpg`, `png`, `fits`, `eps`, `pdf`: standard types
    - `ldac`: Fits file containing LDAC catalog table. In most cases,.
    - `cat`: Text format catalog file.
    - `sav`: Only in old IDL version code, saved variables.
    - `log`: Text format report for reduction process. This is a copy of verbose mode output (debug=8). Even if the output is silent, this file will still be generated.
    - *In most cases, ldac and cat format catalog will both be provided, and when eps is presented, png is also there for quick preview.*
+ `content`: file content, in some case, same content we will have different format.
    + *From bfcorrect*
    - `01.fits`: Bias and flat corrected and splitted file of different amplifier. We have 01-16 for bok and 1-4 for NOWT.
    + *From photometry*
    - `01.ldac`: Output of Source Extractor.
    - `phot.ldac|cat`: The catalog merged from slice data, rotated and added with their offset. If aper and psf photometry is performed, result will be in extra columns.
    + *From astrometry*
    - `wcs.ldac|cat`: Main output of astrometry. Every star will have a guessed coord (RA/Dec) from original observation pointings. If wcs successes, the real coordination (J2000, FK5) will replace original guess, and new wcs parameter will cover obs version. Original wcs parameter will be saved in another name.
    - `wcs.txt`: Wcs parameters, same as in header, here is a quick view copy.
    - `wcsref.ldac`: WCS reference catalog, save for future use and check. NOTE: this file do NOT nave version control, it will be created when first needed, and then used in all versions.
    - `recenter.txt` Report about recenter, correction of each step.
    - `grid.png`: Grid of xy to sky, reference stars and x/y directions are marked.
    - `resid.eps|png|txt`: Residual of wcs, use it for check and papers. Text format contains list of all matched stars.
    + *From magcalibrate*
    - `mag.ldac|cat`: Main output of magcalibrate. Corrected mag will fill corresponding fields of star info. If fail, those fields will be kept empty.
    - `magdiff.eps|png|txt`: Magnitude difference between instrument mag and reference mag.
    + *From report*
    - `db.txt` Final report, machine readable version, space seperated values. All invalid values will be transformed to a special value. A serias of db file can be stacked up as a dayly or monthly report.
    - `report.txt` Final report, human readable. It contains values with explains, easy to read and understand, but not good for machine read.


## Main Part of Pipeline

### Global Objects

##### Variables
`debug` This is used in all kinds of functions, it tells the debug level, from silence to verbose. It should be a integer number, we have following levels:

- `-2` complete silent mode, nothing will be displayed, even if error encoutered. 
- `-1` silent mode, only display start and finish of task, and display critical error before quiting.
- `0` normal mode, display basic running info.
- `1` normal mode, but a little more.
- `2` display detailed process info.
- `3-6` same as 2.
- `7` debug mode, display only top level function info.
- `8` debug mode, display top and median level function info.
- `9` debug mode, all debug info from all level.

In every function, we should test the existance of global variable `debug`, it not, then default level 0 will be applied.

In most case, this is set by caller, as a global variable, or from commandline.

### Remove overscan
##### Mission
Substract overscan from image.

##### Location & Level
`bok.rm_os.rm_os` Base Level Routine.

##### Argument and return
+ `dat`: original 2-d data array,, including image and overscan
+ `no_fit`: if set, column median will be polyfitted, else use the original median. Due to previous error, fitting is now not recommended.
+ `RETURN`: image array with overscan substracted.

##### Algorithm
1. transfer image into float32 array.
2. get median of overscan by each row.
3. if fitting is specified, do order 3 polyfit on median of overscan.
4. substract image with overscan.

### Bias Merge
##### Mission
Merge multi bias images into a final bias image. For each pixel, use median from all images. Images must be taken from the same night, usually 5 or 10 before observation and 5 or 10 after.

##### Location & Level
`bok.biasflat.merge_bias` Top Level Task

##### Arguments & Return
+ `bias_list`: bias file list or list file.
+ `out_bias_file`: output filename.
+ `basedir`: path added to files in list.

For first argument `xxxx_list`, we can provide string as filename of list of files, or we can directly provide a enumeratable object, a list, a tuple, or an ndarray. Function `list_expand` will check the argument and expand it into real filenames.

Last argument `basedir`, is a dir string added to files in the list, The list may contain a relative or partial path, use this argument to complete it. This argument will appear in some other cases.

##### Algorithm
1. create a data cube.
2. read bias fits one by one, remove overscan, and then store in cube.
3. get median value of each pixel.
4. write to output file.

### Flat Merge
##### Mission
Merge multi flat images into a final flat image. For each pixel, use median from normalized all images. Images must be taken from the same night, usually 5 or 10 before observation and 5 or 10 after. Twilight flat is suggested, and dome flat is secondly suggested. Night-sky light super flat is used only for compare and double check.

##### Location & Level
`bok.biasflat.merge_flat` Top Level Task

##### Arguments & Return
+ `flat_list`: flat file list or list file
+ `bias_file`: bias fits file
+ `out_flat_file`: output filename
+ `basedir`: path added to files in list

##### Algorithm
1. create a data cube.
2. read flat fits one by one, do these: remove overscan, remove bias, find median of whole frames, normalize by dividing by median. Finilly, store in cube.
3. get median value of each pixel.
4. write to output file.

--

### Bias and Flat Correction
##### Mission
Correct image with bias and flat. If necessary, mark bad pixels with NaN of Inf. And original fits will be divided into small pieces for each amplifier.

##### Location & Level
`bok.bfcorrect.bfcorrect` Top Level Task

##### Arguments & Return
+ `raw_path`: raw data path.
+ `red_path`: output path of reduced data.
+ `bare_fits`: bare filename, without path and extension.
+ `bias_file`: bias filename, full name with path. Default is `bias.fits` at parent dir of red_path.
+ `flat_file`: flat filename, full name with path. Default is `flat.fits` at parent dir of red_path.
+ `ver_to`: version of output
+ `RETURN`: error code, 1 for normal, negative for error.

`raw_path` and `red_path` are two common arguments about path, raw is at original place, and red is target place. For the first step (bfcorrect and photometry), we need raw fits file, but for following steps, input and output are all inside red.

`bare_fits` is bare name of fits, not including path and extension, will be sub-dir name of reduced data.

`ver_from` and `ver_to`, are reduced version of reduction. For each step, we can tell it to use data from a specified version, and save data as another version. Version name is a string, will be added between bare filename and appendix. For bfcorrect, no input version, it must read original fits. For report, no output version, it takes the last output version as its input version and make the same output. Default version is empty, this is a standard version.

##### Algorithm
1. Load original observation file.
2. Remove overscan, correct bias and flat.
3. Save to seperated file, sliced by amplifier.

### Photometry Source Extract
##### Mission
Find out all source from corrected image. Here we use Source Extractor to find objects and do basic photon count. Then we will do aperture photometry and psf photometry. Final result will merge into a unity catalog.

##### Location & Level
`bok.photomerey.photomerey` Top Level Task

##### Arguments & Return
+ `raw_path`: raw data path.
+ `red_path`: output path of reduced data.
+ `bare_fits`: bare filename, without path and extension.
+ `keep`: if set to false, sliced fits will be removed after photometry to save diskspace.
+ `sex_cmd`: command of Source Extractor, in Mac and some Linux, it is `sex`, if installed by apt-get, it is `sextractor`.
+ `aper_rad`: radius of aper photometry. Setting to 0 means no aper. Using default as None means will apply default radii.
+ `do_psf`: bool, do psf photometry or not, currently default is false.
+ `ver_from`: version of input
+ `ver_to`: version of output
+ `RETURN`: negative for error, 0 for fail, and if OK, returns total number of stars detected.

About aper_rad, this is an array (or list, or tuple), each item is a 3-item list or tuple, they are respectively the aperture radius, the sky inner radius, the sky outer radius. If radius given positive values, that means times of fwhm, if negative, means pixels. By default, radii are 2.5, 3, and 5 times of fwhm.

##### Algorithm
1. Load header from raw fits. Correct and normalize header info in it. (Especially for fits of NOWT)
2. For each amplifier:
3. &nbsp; &nbsp;  Load amplifier fits
4. &nbsp; &nbsp; Call Source Extractor to find stars and their basic parameters
5. &nbsp; &nbsp; Get background (sky) parameters
6. &nbsp; &nbsp; Do aperture photometry on stars found, if required
7. &nbsp; &nbsp; Do psf profile extractor and photometry, if required
8. &nbsp; &nbsp; Merge catalog from seperated files.
9. Save to catalog file of LDAC format.

This is the last step needs the raw file, this step still need header info from raw fits. From the next step, it will read header from output ldac of previous step.

### Astrometry Calibration
##### Mission
Do astrometry by matching image stars and reference stars. We will use USNO-B1.0 catalog as main reference, and APASS catalog is the secondly reference. The advantage of APASS is that it can do mag calibration at the same time for Sloan $g$, $r$, $i$ band.

##### Location & Level
`bok.astrometry.astrometry` Top Level Task

##### Arguments & Return
+ `red_path`: output path of reduced data.
+ `bare_fits`: bare filename, without path and extension.
+ `wcs_catalog`: reference catalog of wcs
+ `match_distan`: distance limit for matching, default 0.002 deg, 7.2 arcsec
+ `recenter`: if is true, use grid method to find real center, for bok, default is false, but for nowt, default is true
+ `ver_from`: version of input
+ `ver_to`: version of output
+ `RETURN`: error code, 1 for normal, negative for error.

##### Algorithm
1. Load photometry output ldac file.
2. Rotate image to north up direction, rotate only result catalog. This is the main difference between different telescope. For bok, the rotation is fixed, but for nowt, it depends on the rotate keyword in header.
3. Get reference catalog from specified source, call specified functions to get it. From this step, operations are same for different telescopes.
3. If recenter is true, do a 4-level approaching grid to find real center of image. This is important if real center drift too much from given.
4. 

### Astrometry Reallocate Center
##### Location & Level
`bok.astrometry.recenter` Median Level Task

##### Arguments & Return
+ `red_path`: output path of reduced data.
+ `bare_fits`: bare filename, without path and extension.
+ `wcs_catalog`: reference catalog of wcs
+ `match_distan`: distance limit for matching, default 0.002 deg, 7.2 arcsec
+ `recenter`: if is true, use grid method to find real center, for bok, default is false, but for nowt, default is true
+ `ver_from`: version of input
+ `ver_to`: version of output
+ `RETURN`: error code, 1 for normal, negative for error.

##### Algorithm
1. Load photometry output ldac file.
2. Rotate image to north up direction, rotate only result catalog. This is the main difference between different telescope. For bok, the rotation is fixed, but for nowt, it depends on the rotate keyword in header.
3. Get reference catalog from specified source, call specified functions to get it. From this step, operations are same for different telescopes.
3. If recenter is true, do a 4-level approaching grid to find real center of image. This is important if real center drift too much from given.
4. 

### Flux Calibration
##### Mission
Calibrate star flux or magnitude by matching image stars with reference stars. Different band we have different reference catalog. For Sloan $g'$, $r'$, and $i'$, we use SDSS DR12 (if capable) or APASS, for Stromgren $u$ and SAGE $v$, we use extented APASS.

##### Location & Level
`bok.magcalibrate.magcalibrate` Top Level Task

##### Arguments & Return
+ `red_path`: output path of reduced data.
+ `bare_fits`: bare filename, without path and extension.
+ `mag_catalog`: use which magnitude catalog
+ `match_mode`: mode of choose matched star, default 1 for auto, 0 for manual, 2 for all in 3 $\sigma$, 3 for all matched.
+ `match_distan`: distance limit for matching, default 0.002 deg, 7.2 arcsec
+ `ver_from`: version of input
+ `ver_to`: version of output
+ `RETURN`: error code, 1 for normal, negative for error.

##### Algorithm
1. Load original observation file.

### Report Generation
##### Mission
Generate a final report about the processing This is a part cannot be bypassed. It will generage both `db.txt` and `report.txt`, the former is machine readable and the latter is human readable.

##### Location & Level
`bok.report.report` Top Level Task

##### Arguments & Return
+ `red_path`: output path of reduced data.
+ `bare_fits`: bare filename, without path and extension.
+ `ver_from`: version of input
+ `RETURN`: error code, 1 for normal, negative for error.

##### Algorithm
1. Load original observation file.

## Common Utility

### Expand a file list
`common.util.list_expand` If given a list filename, expand ths name to its content.

+ `alist` list or list filename
+ `basedir` base directory added to filelist
+ `RETURN` a tuple, first item is filenames, second is length

### Check file list existence
`common.util.is_list_exists` Check existance of files in list.

+ `alist` list or list filename
+ `basedir` base directory added to filelist
+ `RETURN` if all files exist, return true. If any is missing, return false.

### Output to both screen and log
`common.logger` Class. Provide a two way output, to both screen and log file.

##### \_\_init\_\_
Init the object, open file for output.

This will send a start message to screen with the datetime. This is a -1 level info.

+ `log_filename` log filename, including full path and file name
+ `task` task name, will be printed
+ `debug_level` debug level, to control screen display
+ `show_time` show time in log lines or not

##### write
Write log message.

+ `msg` message, if is multiline, use array like object (ndarray, list, tuple).
+ `level` level of message, if message level is lower than or equal to debug level, it will be displayed.
+ `show_time`: if true, current time (no date) will be displayed, before content in log file, if None, use init default

##### timespan
Get time passed from start time.

##### close
Close the log file. And send a "Done" message to screen, with time used.

This is a -1 level info.

### Message Box
`common.msg_box` Class. A message box generator.

##### \_\_init\_\_
+ `border` border string, contains 3 char, respectively corner, horizontal line, vertical line. Default is "+-|".
+ `width` width of whole box, default is 80
+ `align` alignment of each line, default is centered.

##### box
Generate the box, returns a list.

+ `msg` message, a list or tuple
+ `title` title of box
+ `border`
+ `width`
+ `align`

### Progress Bar
`common.progress_bar` Class. Generate and display progress bar.

##### \_\_init\_\_
+ `value_init` progress bar initial value
+ `value_step` step value when call method step
+ `value_to` right end value of progress bar
+ `value_from` left end value of progress bar
+ `length` length of progress bar body, between bar brace
+ `format_percent` format of percent display, set None to suppress display
+ `format_value` format of value display, set None to suppress display
+ `char_brace` char of brace enclosing the bar, a 2-item tuple or list
+ `char_done` char of done part of progress bar, left part
+ `char_wait` char of waiting part of progress bar, right part

##### goto
Walk the progress bar to specified value, and flush the display.

+ `value` position of progress bar. If out of range, will display 0% or 100%

##### step
Step the bar.

+ `step` how much to add to current value, default is as set in init.

##### clear
Clear the progress bar. Use space to cover

##### end
End this progress bar, keep bar status on previous line

##### finished
Property. The progress bar is finished or not, go beyond value_to.

