#!/usr/bin/env bash
# 
#  chmod +x jscss.sh
#  usage:   $jscss.sh 
#
#  Script to compress and combine JS/CSS
# 
# ----------------------------------------------------------------------------
#  TODO
#   - accept directory as parameter?
# ----------------------------------------------------------------------------
basedir=`pwd`/trunk/demisauce/public/js
cssdir=`pwd`/trunk/demisauce/public/css
echo "js Basedir = $basedir"
echo "css Basedir = $cssdir"

# remove the minified js
rm $basedir/ds.*-min.js 
java -jar ~/dev/yuicompressor-2.4.2.jar $basedir/ds.base.js -o $basedir/ds.base-min.js
java -jar ~/dev/yuicompressor-2.4.2.jar $basedir/ds.adminbase.js -o $basedir/ds.adminbase-min.js
java -jar ~/dev/yuicompressor-2.4.2.jar $basedir/ds.slugeditor.js -o $basedir/ds.slugeditor-min.js
java -jar ~/dev/yuicompressor-2.4.2.jar $basedir/ds.gears.js -o $basedir/ds.gears-min.js

echo "Combinning all static js into single lib-js.js"
rm $basedir/lib-js.js
cat $basedir/jquery-1.2.6.min.js $basedir/jquery.dimensions.js $basedir/ui.mouse.js  \
    $basedir/jquery.cookie.js $basedir/jquery.treeview.js $basedir/ui.draggable.js $basedir/ui.sortable.js \
    $basedir/jquery.form.js $basedir/jquery.hotkeys.js $basedir/jquery.tooltip.js $basedir/facebox.js \
    $basedir/jquery.bgiframe.min.js $basedir/jquery.autocomplete.js > $basedir/lib-js.js
    
echo "Combinning all demisauce js into single ds-js.js"
rm $basedir/ds-js.js
cat $basedir/ds.adminbase-min.js $basedir/ds.base-min.js \
    $basedir/ds.slugeditor-min.js $basedir/gears_init.js \
    $basedir/ds.gears.js > $basedir/ds-js.js

# now css
echo "Combinning js into single alll-css.css"
rm $cssdir/all-css.css
cat $cssdir/local.css $cssdir/ds.widgets.css $basedir/jquery.treeview.css \
   $basedir/jquery.autocomplete.css > $cssdir/all-css.css



