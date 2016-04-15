# EGAP-infographics
A repository for code to automate the creation of infographic slides for EGAP Burkina Faso

## To do list

 - [x] 1. read and clean indicator data set.
 - [x] 2. create `text.csv` with infographic text (unicode); read and clean.
 - [x] 3. resize `png` files to a standard size, rename if necessary.
 - [x] 4. create plots of indicator data.
 - [x] 5. create image grobs for bar, number, and summary infographic slides.
 - [x] 6. loop through indicators and apply infographic logic to combine grobs and text.
 - [x] 7. export final slides.
 - [ ] 8. unit test and debug.

### Unit test to do

 - [ ] 1. invert red/green bars for percent indicators.
 - [ ] 2. change school supply indicator to read "0 jour de retard" if the supplies were delivered prior to the start date and remove the number from the second paragraph.
 - [ ] 3. check CEP admissions indicator (generated twice, but no summary slide).
 - [ ] 4. for indicators with values in excess of 100% (birth certificate and vaccinations), change second paragraph text to show read "près de 100%" and cap green bar at 99.5% and red bar at 0.5% so it's visible.
 - [ ] 5. text resizing:
     - [ ] accouchement assistés
     - [ ] stock de gas des centres de santé
     
