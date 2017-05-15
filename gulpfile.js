'use strict';

const gulp = require('gulp');
const fs = require('fs');
const runSequence = require('run-sequence');
const bower = require('main-bower-files');
const gulpif = require('gulp-if');
const lint = require('gulp-eslint');
const uglify = require('gulp-uglify');
const concat = require('gulp-concat');
const flatten = require('gulp-flatten');
const rename = require('gulp-rename');
const gulpFilter = require('gulp-filter');
const browserify = require('browserify');
const babelify = require('babelify');
const source = require('vinyl-source-stream');
const gutil = require('gulp-util');
const nib = require('nib');
const stylus = require('gulp-stylus');
const imagemin = require('gulp-imagemin');
const pngquant = require('imagemin-pngquant');
const gifsicle = require('imagemin-gifsicle');
const jpegtran = require('imagemin-jpegtran');
const realFavicon = require ('gulp-real-favicon');
const FAVICON_DATA_FILE = 'faviconData.json';

// const svgo = require('imagemin-svgo');

const DEBUG = process.env.NODE_ENV === 'production';
const DEST_PATH = 'public/';

// grab libraries files from bower_components, minify and push in /public
gulp.task('bower', () => {
  const jsFilter = gulpFilter('**/*.js', {
    restore: true,
  });
  const cssFilter = gulpFilter('*.css', {
    restore: true,
  });
  const fontFilter = gulpFilter(['*.eot', '*.woff', '*.svg', '*.ttf']);
  const destPath = `${DEST_PATH}lib`;

  return gulp.src(bower({
    debugging: true,
    includeDev: true,
  }))

  // grab vendor js files from bower_components, minify and push in /public
    .pipe(jsFilter)
    .pipe(gulp.dest(`${destPath}/js/`))
    .pipe(gulpif(!DEBUG, uglify()))
    .pipe(concat('vendor.js'))
    .pipe(rename({
      suffix: '.min',
    }))
    .pipe(gulp.dest(destPath + '/js/'))
    .pipe(jsFilter.restore)

  // grab vendor css files from bower_components, minify and push in /public
    .pipe(cssFilter)
    .pipe(gulp.dest(destPath + '/css'))
  // .pipe(minifycss())
    .pipe(rename({
      suffix: '.min',
    }))
    .pipe(gulp.dest(destPath + '/css'))
    .pipe(cssFilter.restore)

  // grab vendor font files from bower_components and push in /public
    .pipe(fontFilter)
    .pipe(flatten())
    .pipe(gulp.dest(destPath + '/fonts'));
});


gulp.task('browserify', () => {
  return browserify()
    .on('error', gutil.log)
    .require('./src/js/app.js', {
      entry: true,
      extensions: ['.js', 'jsx'],
      debug: true,
    })
    .transform(babelify, {
      presets: ['es2015', 'react']
    })
    .bundle()
    .pipe(source('bundle.js'))
    .pipe(gulp.dest(DEST_PATH + 'js'));
});


gulp.task('js', () => {
  return gulp.src(['src/js/**/*.js', '!src/js/templates/**/*.js'])
    .pipe(lint.format());
});

gulp.task('css', () => {
  gulp.src('src/css/style.styl')
    .pipe(stylus({
      use: nib(),
      compress: !DEBUG,
      import: ['nib'],
    }))
    .pipe(gulp.dest(DEST_PATH + 'css/'));
});

gulp.task('img', () => {
  gulp.src('src/img/**/*')
    .pipe(gulp.dest(DEST_PATH + 'img'));
});

gulp.task('html', () => {
  gulp.src('./src/*.html')
    .pipe(gulp.dest(DEST_PATH));
});

gulp.task('files', () => {
  gulp.src(['./src/**.*', '!./src/**.*.html', '!./src/**.*js', '!./src/img/'])
    .pipe(gulp.dest(DEST_PATH));
});

gulp.task('react', () => {
  runSequence('js', 'browserify');
});

// Generate the icons. This task takes a few seconds to complete.
// You should run it at least once to create the icons. Then,
// you should run it whenever RealFaviconGenerator updates its
// package (see the check-for-favicon-update task below).
gulp.task('generate-favicon', (done) => {
  realFavicon.generateFavicon({
    masterPicture: 'src/img/favicon.png',
    dest: DEST_PATH + 'img/favicons/',
    iconsPath: '/img/favicons/',
    design: {
      ios: {
        pictureAspect: 'backgroundAndMargin',
        backgroundColor: '#ffffff',
        margin: '14%',
        assets: {
          ios6AndPriorIcons: false,
          ios7AndLaterIcons: false,
          precomposedIcons: false,
          declareOnlyDefaultIcon: true,
        },
        appName: 'ellugar.co',
      },
      desktopBrowser: {},
      windows: {
        pictureAspect: 'noChange',
        backgroundColor: '#000000',
        onConflict: 'override',
        assets: {
          windows80Ie10Tile: true,
          windows10Ie11EdgeTiles: {
            small: true,
            medium: true,
            big: true,
            rectangle: false,
          },
        },
        appName: 'ellugar.co'
      },
      androidChrome: {
        pictureAspect: 'noChange',
        themeColor: '#000000',
        manifest: {
          name: 'ellugar.co',
          display: 'standalone',
          orientation: 'notSet',
          onConflict: 'override',
          declared: true
        },
        assets: {
          legacyIcon: false,
          lowResolutionIcons: false
        }
      },
      safariPinnedTab: {
        pictureAspect: 'blackAndWhite',
        threshold: 10,
        themeColor: '#000000'
      }
    },
    settings: {
      scalingAlgorithm: 'Mitchell',
      errorOnImageTooSmall: false
    },
    versioning: {
      paramName: 'v',
      paramValue: 'rM3xw7xzqY'
    },
    markupFile: FAVICON_DATA_FILE
  }, function() {
    done();
  });
});

// Inject the favicon markups in your HTML pages. You should run
// this task whenever you modify a page. You can keep this task
// as is or refactor your existing HTML pipeline.
gulp.task('inject-favicon-markups', function() {
  return gulp.src(['views/favicon.html'])
    .pipe(
      realFavicon.injectFaviconMarkups(
        JSON.parse(
          fs.readFileSync(FAVICON_DATA_FILE)
        ).favicon.html_code
      ))
    .pipe(gulp.dest('views/'));
});

// Check for updates on RealFaviconGenerator (think: Apple has just
// released a new Touch icon along with the latest version of iOS).
// Run this task from time to time. Ideally, make it part of your
// continuous integration system.
gulp.task('check-for-favicon-update', () => {
  const currentVersion = JSON.parse(fs.readFileSync(FAVICON_DATA_FILE)).version;
  realFavicon.checkForUpdates(currentVersion, (err) => {
    if (err) {
      throw err;
    }
  });
});

gulp.task('favicon', () => {
  runSequence('generate-favicon', 'inject-favicon-markups');
});

gulp.task('init', ['css', 'bower', 'react', 'img', 'html', 'files']);

gulp.task('watch', () => {
  gulp.watch('src/css/**/*.styl', ['css']);
  gulp.watch('src/js/**/*.js', ['react']);
  gulp.watch('src/js/**/*.jsx', ['react']);
  gulp.watch(['src/img/**/*', '!src/img/favicon.png'], ['img']);
  gulp.watch('src/*.html', ['html']);
});

gulp.task('default', () => {
  runSequence('init', 'watch');
});
