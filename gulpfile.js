var gulp = require('gulp-help')(require('gulp'));

var $ = require('gulp-load-plugins')();
var awspublish = require('gulp-awspublish');
var browserSync = require('browser-sync');
var bower = require('bower');
var cloudfront = require('gulp-cloudfront');
var concat = require('gulp-concat');
var del = require('del');
var exec = require('child_process').exec;
var es = require('event-stream');
var fs = require('fs');
var spawn = require('child_process').spawn;
var gettext = require('gulp-angular-gettext');
var gulpFilter = require('gulp-filter');
var gulpif = require('gulp-if');
var gutil = require('gulp-util');
var htmlmin = require('gulp-htmlmin');
var inject = require('gulp-inject-string');
var less = require('gulp-less');
// var minifyCss = require('gulp-minify-css');
// var minifyHTML = require('gulp-minify-html');
var nano = require('gulp-cssnano');
var ngAnnotate = require('gulp-ng-annotate');
var plumber = require('gulp-plumber');
var parallelize = require("concurrent-transform");
var protractor  = require('gulp-protractor');
var rename = require('gulp-rename');
var replace = require('gulp-replace');
var request = require('request');
var RevAll = require('gulp-rev-all');
var reload      = browserSync.reload;
var runSequence = require('run-sequence');
var sass = require('gulp-sass');
var shell = require('gulp-shell');
var stripLine  = require('gulp-strip-line');
var sh = require('shelljs');
var tap = require('gulp-tap');
var templateCache = require('gulp-angular-templatecache');
var uglify = require('gulp-uglify');
var webserver = require('gulp-webserver');


////////////////////////////////
////// Configuration
////////////////////////////////
//
// Since BuddyUp has several front-end codebases, the aim here is to
// make organization and configuration simple.  The code below the config
// should largely not have to be changed - or at least, that's the goal!
// Simple, clear, and understandable.

// Options for a front-end codebase:
// {
//   name: "foo",           // Used for naming directories, etc. Required.
//   aws_bucket: "bar"      // AWS bucket name.  Required.
//   aws_dist_id:           // AWS cloudfront distribution ID. Required.
//   aws_region: "us-west-2"// Defaults to us-standard
//   dir_name: "foo",       // defaults to name
//   base_dir: "foo",       // defaults to /frontends/{dir_name}/
//   native_app: false,     // set to true to enable ionic. Defaults false.
//   i18n: true,            // Whether to build translation code in.  Defaults true.
//   lib_js_files: {
//     "js/my_lib.js"       // A list of javascript files to put into lib.js.
//                          // Defaults to everything used by the main app.
//   },
//   main_js_files: {
//     "js/my_main.js"      // A list of javascript files to put into main.js.
//                          // Defaults to an angular app, based on the main app.
//   },
//   port: 8030,            // Defaults to 8100 + the number in the list.
// }


var CODEBASES = [
  {
    name: "app",
    aws_bucket: "app.buddyup.org",
    aws_dist_id: "E3U44GC9XBQ632",
    aws_region: "us-west-2",
    dev_proxy: "app.bu.dev"
  },
  {
    name: "dashboard",
    aws_bucket: "dashboard.buddyup.org",
    aws_dist_id: "E3A6GYQXCPF4DI",
    aws_region: "us-west-2",
    dev_proxy: "dashboard.bu.dev"
  },
  {
    name: "groundcontrol",
    aws_bucket: "groundcontrol.buddyup.org",
    aws_dist_id: "E1BTGS109KGBG3",
    aws_region: "us-west-2",
    dev_proxy: "groundcontrol.bu.dev"
  },
  {
    name: "ionic",
    dir_name: "app",
    base_dir: "frontends/app/",
    target_dir: "native/code/",
    native_app: true
  },
  {
    name: "marketing",
    aws_bucket: "www.buddyup.org",
    aws_dist_id: "E2D970H8XVSH63",
    aws_region: "us-west-2",
    dev_proxy: "marketing.bu.dev"
  },
];
var CODEBASE_APP = 0;
var CODEBASE_DASHBOARD = 1;
var CODEBASE_GROUNDCONTROL = 2;
var CODEBASE_IONIC = 3;
var CODEBASE_MARKETING = 4;


// I seriously hate gulp sometimes.
// var codebase_aliases = {
//   "app": CODEBASE_APP,
//   "dashboard": CODEBASE_DASHBOARD,
//   "groundcontrol": CODEBASE_GROUNDCONTROL,
// };
// console.log(gutil.env._)
// if(gutil.env._[1] && gutil.env._[1] in codebase_aliases) {
//   CODEBASES = [CODEBASES[codebase_aliases[gutil.env._[1]]]];
//   gutil.env._.splice(1,1);
//   console.log("Only " + CODEBASES[0].name + ".");
// } else {
//   console.log("All codebases.");
// }
// console.log(gutil.env._)

////////////////////////////////
////// Initialization
////////////////////////////////

// Build vars
var BUDDYUP_API_ENDPOINT = process.env.BUDDYUP_API_ENDPOINT;
var BUDDYUP_API_VERSION = "v1";
var FIREBASE_ENDPOINT = process.env.FIREBASE_ENDPOINT;
var FIREBASE_KEY = process.env.FIREBASE_KEY;
var FIREBASE_LIVE_KEY = process.env.FIREBASE_LIVE_KEY || false;
var FIREBASE_LIVE_ENDPOINT = process.env.FIREBASE_LIVE_ENDPOINT || false;
var PRODUCTION_BUILD = (process.env.PRODUCTION_BUILD == "true")? true: false;
var BUILD_IONIC = false;
var BUILD_IONIC_DEV = false;
var IONIC_APP_ID = process.env.IONIC_APP_ID;
var IONIC_KEY = process.env.IONIC_KEY;
var GCM_KEY = process.env.GCM_KEY;
var IN_TESTS = false;
var APP_VERSION = "1.6.11";

if (PRODUCTION_BUILD) {
  console.log("//////////////////////////////////////////");
  console.log("///////////// PRODUCTION MODE ////////////");
  console.log("//////////////////////////////////////////");
}

var setup_paths = function() {
  console.log("Symlinking bower and node...");
  exec('ln -s ../bower_components ./bower_components');
  exec('ln -s ../node_modules ./node_modules');
  console.log("Done.");
};

var add_defaults_to_codebases = function() {
  var counter = 0;
  for (var c_index in CODEBASES) {
    counter ++;
    var c = CODEBASES[c_index];
    if (
        (c.name === undefined ||
        c.aws_bucket === undefined ||
        c.aws_dist_id === undefined) &&
        c.native_app !== true
    ) {
      console.log("Missing name, aws_bucket, or aws_dist_id");
      process.exit(code=1);
    }
    var dir_name = c.dir_name || c.name;
    var base_dir = c.base_dir || "frontends/" + c.name + "/";
    var defaults = {
      base_dir: base_dir,
      target_dir: base_dir,
      dir_name: dir_name,
      native_app: false,
      i18n: true,
      min_lib_js_files: [
        // 'bower_components/es5-shim/es5-shim.min.js',
        // 'bower_components/es6-shim/es6-shim.min.js',
        // 'bower_components/thread/thread.min.js',
        // 'bower_components/thread/lib/eval.js',

        'bower_components/jquery/dist/jquery.min.js',
        'bower_components/jstz-detect/jstz.min.js',

        'bower_components/ionic/release/js/ionic.min.js',
        'bower_components/angular/angular.js',
        'bower_components/ngCordova/dist/ng-cordova.js',
        // 'bower_components/ionic/release/js/ionic.bundle.js',

        'bower_components/angular-animate/angular-animate.js',
        'bower_components/angular-sanitize/angular-sanitize.js',
        'bower_components/angular-ui-router/release/angular-ui-router.js',

        'node_modules/angular-hotkeys/build/hotkeys.js',
        'bower_components/angular-cookies/angular-cookies.js',
        'bower_components/firebase/firebase.js',
        // 'bower_components/firebase-simple-login/firebase-simple-login.js',
        'bower_components/angularfire/dist/angularfire.js',
        'bower_components/ionic/release/js/ionic-angular.js',
        'bower_components/ion-autocomplete/dist/ion-autocomplete.js',
        'bower_components/angucomplete-alt/dist/angucomplete-alt.min.js',
        'bower_components/angular-gettext/dist/angular-gettext.js',
        'bower_components/spectrum/spectrum.js',
        'bower_components/angular-spectrum-colorpicker/dist/angular-spectrum-colorpicker.js',
        'bower_components/ngImgCrop/compile/minified/ng-img-crop.js',
        'bower_components/moment/min/moment-with-locales.js',
        'bower_components/angular-moment/angular-moment.js',
        'bower_components/angular-filters/dist/angular-filters.js',

        // Groundcontrol - TODO: see if these should be pulled for space reasons for the app.
        'bower_components/angular-ui-grid/ui-grid.min.js',
        'bower_components/d3/d3.min.js',
        'bower_components/nvd3/nv.d3.min.js',
        'bower_components/angularjs-nvd3-directives/dist/angularjs-nvd3-directives.min.js',
        // TODO: enable once my PR is merged.
        // 'bower_components/ng-csv/build/ng-csv.js',
        'frontends/common/js/libs/ngCsv.js',


        // 'bower_components/angulartics/dist/angulartics.min.js',
        // 'bower_components/angulartics/dist/angulartics-ga.min.js',
        // 'bower_components/angulartics/dist/angulartics-ga-cordova-google-analytics-plugin.min.js',
        // 'bower_components/angulartics/dist/angulartics-ga-cordova.min.js',

        // 'bower_components/angular-thread/angular-thread.min.js',
        'bower_components/Autolinker.js/dist/Autolinker.js',

        'bower_components/ionic-service-core/ionic-core.js',
        'bower_components/ionic-service-deploy/ionic-deploy.js',
        'bower_components/ionic-service-analytics/ionic-analytics.js',
        'bower_components/ionic-service-push/ionic-push.js'
        // 'bower_components/bower-google-analytics/analytics.js'

      ],
      main_js_files: [
        'frontends/common/js/modules.js',
        'frontends/common/js/services/**/*.js',
        'frontends/common/js/filters/**/*.js',
        'frontends/common/js/directives/**/*.js',
        'frontends/common/js/controllers/**/*.js',
        base_dir + 'src/js/templates_common.js',
        base_dir + 'src/js/templates_desktop.js',
        base_dir + 'src/js/templates_shared.js',
        base_dir + 'src/js/templates_ionic.js',
        base_dir + 'src/js/app.js',
        base_dir + 'src/js/services/**/*.js',
        base_dir + 'src/js/filters/**/*.js',
        base_dir + 'src/js/directives/**/*.js',
        base_dir + 'src/js/controllers/**/*.js',
        '!' + base_dir + 'src/js/lib/**',
        '!' + base_dir + 'src/tests/**'
      ],
      aws_region: "us-standard",
      port: 8100 + counter,
      api_port: 8400 + counter
    };
    var lib_js = [];
    for (var index in defaults.min_lib_js_files) {
      lib_js.push(defaults.min_lib_js_files[index].replace(".min.js", ".js"));
    }
    defaults["lib_js_files"] = defaults.min_lib_js_files;

    config = defaults;
    for (index in c) {
      config[index] = c[index];
    }
    if (!BUDDYUP_API_ENDPOINT) {
      if (PRODUCTION_BUILD) {
        BUDDYUP_API_ENDPOINT = "https://api.buddyup.org";
      } else {
        BUDDYUP_API_ENDPOINT = "http://localhost";
      }
    }
    if (!FIREBASE_ENDPOINT) {
      if (PRODUCTION_BUILD) {
        FIREBASE_ENDPOINT = "https://buddyup.firebaseio.com";
      } else {
        FIREBASE_ENDPOINT = "https://buddyup-dev.firebaseio.com";
      }
    }

    CODEBASES[c_index] = config;

  }
};
var init = function() {
  setup_paths();
  add_defaults_to_codebases();
};
init();

////////////////////////////////
////// Utils
////////////////////////////////
var errorHandler = function(error) {
  // Output an error message
  gutil.log(gutil.colors.red('Error (' + error.plugin + '): ' + error.message));
  // emit the end event, to properly end the task
  this.emit('end');
};
var run_codebase_tasks = function(task, expression) {
    var task_list = [];
    expression = expression || "true";
    for (var c_index in CODEBASES) {
      var codebase = CODEBASES[c_index];
      if (BUILD_IONIC || codebase.native_app == false) {
        task_list.push(task(codebase));
      }
    }
    return es.merge.apply(this, task_list);
};



////////////////////////////////
////// Translation
////////////////////////////////
gulp.task('translate_extract', 'Extract translation strings', function () {
  var task = function(codebase) {
    return gulp.src([
          'frontends/common/templates/**/*.html',
          codebase.base_dir + 'src/templates/**/*.html',
          codebase.base_dir + 'src/js/**/*.js'
    ])
    // .pipe(plumber(errorHandler))
    .pipe(gettext.extract('template.pot', {}))
    .pipe(gulp.dest('po/'+ codebase.target_dir + '/'));
  };

  return run_codebase_tasks(task, "codebase.i18n");
});

gulp.task('translate_compile', 'Compile translations into the app', function () {
  var task = function(codebase) {
    return gulp.src('po/' + codebase.dir_name + '/**/*.po')
        // .pipe(plumber(errorHandler))
        .pipe(gettext.compile({format: 'json'}))
        .pipe(gulp.dest(codebase.target_dir + 'src/translations/'));
  };
  return run_codebase_tasks(task, "codebase.i18n");
});

////////////////////////////////
////// Styling (LESS and SASS)
////////////////////////////////
gulp.task('sass', 'Compile SASS', function(done) {
  var task = function(codebase) {
    return gulp.src(codebase.base_dir + 'src/sass/ionic.scss')
      // .pipe(plumber(errorHandler))
      .pipe(sass())
      .pipe(gulp.dest(codebase.target_dir + 'build/web/css/'))
      // TODO: Switch back when this is fixed.
      // .pipe(minifyCss({
      //   keepSpecialComments: 0
      // }))
      .pipe(gulpif(PRODUCTION_BUILD, nano()))
      .pipe(rename({ extname: '.min.css' }))
      .pipe(gulpif(codebase.name != "marketing", gulp.dest(codebase.target_dir + 'build/web/css/')));
  };

  return run_codebase_tasks(task);
});

gulp.task('less', 'Compile LESS', function (done) {
  var task = function(codebase) {
    return gulp.src([
        'bower_components/typopro/web/TypoPRO-FiraSans/*.css',
        // 'bower_components/typopro/web/TypoPRO-AmaticSC/*.css',
        'bower_components/font-awesome/less/font-awesome.less',
        codebase.base_dir + 'src/less/main.less',
        'frontends/common/less/common.less',
      ])
      // .pipe(plumber(errorHandler))
      .pipe(replace("url('TypoPRO-", "url('../fonts/TypoPRO-"))
      .pipe(replace("font-family:  'TypoPRO ", "font-family:  '"))
      .pipe(less())
      // .pipe(minifyCss({
      //   keepSpecialComments: 0
      // }))
      .pipe(gulpif(PRODUCTION_BUILD, nano()))
      .pipe(concat("main.min.css"))
      .pipe(gulp.dest(codebase.target_dir + 'build/web/css'));
  };
  return run_codebase_tasks(task);
});


////////////////////////////////
////// Copy, Javascript
////////////////////////////////

// Copy all static assets
gulp.task('copy', 'Copy all static assets', ['translate_compile', 'less', 'sass'], function() {
  var d = new Date();
  var stamp = d.getTime();
  var fontFilter = gulpFilter([
    // "**/*",
    "**/*.woff",
    "**/*.woff2",
    "**/*.ttf",
    "!**/emojisymbols-regular.svg",
    "!**/emojisymbols-regular.eot",
    "!**/emojisymbols-regular.ttf",
    "!**/emojisymbols-regular.woff",
    "!**/emojisymbols-regular.woff2",
  ]);
  var genFontFilter = gulpFilter([
    "*/**/*.woff",
    "*/**/*.woff2",
    "*/**/*.ttf",
  ]);

  var task = function(codebase) {
    return es.merge(
      // Template cache for common components
      gulp.src('frontends/common/templates/common/**/*.html')
        // .pipe(plumber(errorHandler))
        // .pipe(minifyHTML({ empty: true, spare: true, quotes: true }))
        .pipe(htmlmin({collapseWhitespace: true, removeComments: true, caseSensitive: true}))
        .pipe(templateCache('templates_common.js', {
               'standalone': false,
               'root': "common/"
            }))
        .pipe(gulp.dest(codebase.target_dir + 'src/js')),


      // Template cache for ionic-based apps.
      gulp.src(codebase.base_dir + 'src/templates/ionic/**/*.html')
        // .pipe(plumber(errorHandler))
        // .pipe(minifyHTML({ empty: true, spare: true, quotes: true }))
        .pipe(htmlmin({collapseWhitespace: true, removeComments: true, caseSensitive: true}))
        .pipe(templateCache('templates_ionic.js', {
               'standalone': false,
               'root': "ionic/"
            }))
        .pipe(gulp.dest(codebase.target_dir + 'src/js')),

      // Template cache for desktop apps.
      gulp.src(codebase.base_dir + 'src/templates/desktop/**/*.html')
        // .pipe(plumber(errorHandler))
        // .pipe(minifyHTML({ empty: true, spare: true, quotes: true }))
        .pipe(htmlmin({collapseWhitespace: true, removeComments: true, caseSensitive: true}))
        .pipe(templateCache('templates_desktop.js', {
               'standalone': false,
               'root': "desktop/"
            }))
        .pipe(gulp.dest(codebase.target_dir + 'src/js')),

      // Template cache for shared components apps.
      gulp.src(codebase.base_dir + 'src/templates/shared/**/*.html')
        // .pipe(plumber(errorHandler))
        // .pipe(minifyHTML({ empty: true, spare: true, quotes: true }))
        .pipe(htmlmin({collapseWhitespace: true, removeComments: true, caseSensitive: true}))
        .pipe(templateCache('templates_shared.js', {
               'standalone': false,
               'root': "shared/"
            }))
        .pipe(gulp.dest(codebase.target_dir + 'src/js')),


      // Images
      gulp.src('frontends/common/img/**')
        // .pipe(plumber(errorHandler))
        .pipe(gulp.dest(codebase.target_dir + 'build/web/img')),

      gulp.src(codebase.base_dir + 'src/img/**')
        // .pipe(plumber(errorHandler))
        .pipe(gulp.dest(codebase.target_dir + 'build/web/img')),

      // Ionic support files
      gulp.src(codebase.base_dir + 'src/ionic/**')
        // .pipe(plumber(errorHandler))
        .pipe(gulp.dest(codebase.target_dir + 'build')),

      // HTML files
      gulp.src(codebase.base_dir + 'src/index.html')
        // .pipe(plumber(errorHandler))
        // .pipe(gulpif(!BUILD_IONIC, stripLine('src="cordova.js"')))
        .pipe(gulpif(PRODUCTION_BUILD,
          inject.before('<script', '<script>window.version_hash="'+stamp+
            '";window.app_version="' + APP_VERSION +
            '";window.buddyup_api_endpoint="'+BUDDYUP_API_ENDPOINT+"/"+BUDDYUP_API_VERSION+
            '";window.firebase_endpoint="'+FIREBASE_ENDPOINT+'";</script>\n'
          ))
        )
        .pipe(gulpif(!PRODUCTION_BUILD && IN_TESTS,
          inject.before('<script', '<script>window.version_hash="'+stamp+
            '";window.app_version="' + APP_VERSION +
            '";window.buddyup_api_endpoint="'+BUDDYUP_API_ENDPOINT+
            "/"+BUDDYUP_API_VERSION+'";window.firebase_endpoint="'+FIREBASE_ENDPOINT+'";</script>\n'
          ))
        )
        .pipe(gulpif(!PRODUCTION_BUILD && !IN_TESTS,
          inject.before('<script', '<script>window.version_hash="'+stamp+
            '";window.app_version="' + APP_VERSION +
            '";window.dev_mode=true'+
            ';window.buddyup_api_endpoint="'+BUDDYUP_API_ENDPOINT+
            "/"+BUDDYUP_API_VERSION+'";window.firebase_endpoint="'+FIREBASE_ENDPOINT+'";</script>\n'
          ))
        )
        .pipe(gulpif(BUILD_IONIC,
          inject.before('<script', '<script>'+
            'window.GCM_KEY="'+GCM_KEY+
            '";window.dev_mode=false'+
            ';window.IONIC_APP_ID="'+IONIC_APP_ID+
            '";window.IONIC_KEY="'+IONIC_KEY+'";</script>\n'
          ))
        )
        .pipe(gulp.dest(codebase.target_dir + 'build/web/')),

      gulp.src(['node_modules/ionic/node_modules/ionic-app-lib/lib/cordova.js',])
        // .pipe(plumber(errorHandler))
        .pipe(gulpif(BUILD_IONIC, gulp.dest(codebase.target_dir + 'build/web/'))),

      gulp.src([codebase.base_dir + 'src/*.html', "!" + codebase.base_dir + 'src/index.html'])
        // .pipe(plumber(errorHandler))
        // .pipe(gulpif(!BUILD_IONIC, stripLine('src="cordova.js"')))
        .pipe(gulp.dest(codebase.target_dir + 'build/web/')),

      // Translations
      gulp.src(codebase.base_dir + 'src/translations/**')
        // .pipe(plumber(errorHandler))
        .pipe(gulp.dest(codebase.target_dir + 'build/web/translations')),

      // Fonts
      gulp.src([
            codebase.base_dir + 'src/fonts/**',
            'frontends/common/fonts/**',
            'bower_components/ionicons/fonts/**',
            'bower_components/font-awesome/fonts/**',
            'bower_components/ionicons/fonts/**',
            'bower_components/typopro/web/TypoPRO-FiraSans/*.eot',
            // 'bower_components/typopro/web/TypoPRO-AmaticSC/*.eot',
            'bower_components/typopro/web/TypoPRO-FiraSans/*.woff',
            'bower_components/typopro/web/TypoPRO-FiraSans/*.woff2',
            // 'bower_components/typopro/web/TypoPRO-AmaticSC/*.woff',
            // 'bower_components/typopro/web/TypoPRO-AmaticSC/*.woff2',
            'bower_components/typopro/web/TypoPRO-FiraSans/*.ttf',
            // 'bower_components/typopro/web/TypoPRO-AmaticSC/*.ttf'
        ])
        .pipe(gulpif(BUILD_IONIC, fontFilter))
        // .pipe(plumber(errorHandler))
        .pipe(gulp.dest(codebase.target_dir + 'build/web/fonts')),

      // ui-grid fonts
      gulp.src([
            'bower_components/angular-ui-grid/*.eot',
            'bower_components/angular-ui-grid/*.woff',
            'bower_components/angular-ui-grid/*.ttf',
            'bower_components/angular-ui-grid/*.svg',
        ])
        .pipe(gulpif(BUILD_IONIC, genFontFilter))
        // .pipe(plumber(errorHandler))
        .pipe(gulp.dest(codebase.target_dir + 'build/web/css')),

      // Misc files
      gulp.src(codebase.base_dir + 'src/assets/misc/**')
        // .pipe(plumber(errorHandler))
        .pipe(gulp.dest(codebase.target_dir + 'build/web/misc'))
    );
  };
  return run_codebase_tasks(task);
});

gulp.task('scripts', 'Minify and copy all JavaScript', ['copy'], function(done) {
  var schoolsFilter = gulpFilter([
    "**/*",
    "!**/schools-full.js",
  ]);
  var task = function(codebase) {
   return es.merge(

    // Main application files
    gulp.src(codebase.main_js_files)
      // .pipe(plumber(errorHandler))
      .pipe(gulpif((codebase.name == 'app' || codebase.name == 'ionic' || BUILD_IONIC), schoolsFilter))
      .pipe(concat("main.js"))
      .pipe(gulpif(PRODUCTION_BUILD && !BUILD_IONIC_DEV, ngAnnotate()))
      .pipe(gulpif(PRODUCTION_BUILD && !BUILD_IONIC_DEV, uglify()))
      .pipe(gulp.dest(codebase.target_dir + 'build/web/js')),

    // Libraries
    gulp.src(codebase.lib_js_files)
      // .pipe(plumber(errorHandler))
      .pipe(gulpif(PRODUCTION_BUILD && !BUILD_IONIC_DEV, ngAnnotate()))
      .pipe(gulpif(PRODUCTION_BUILD && !BUILD_IONIC_DEV, uglify()))
      .pipe(concat("lib.js"))
      .pipe(gulp.dest(codebase.target_dir + 'build/web/js')),

    gulp.src([
          'bower_components/ionic/release/css/ionic.min.css',
          codebase.base_dir + 'build/web/css/ionic.min.css',
          'bower_components/ionicons/css/**/ionicons.min.css',
          // GC Libs
          'bower_components/angular-ui-grid/ui-grid.min.css',
          'bower_components/nvd3/nvd3.css',
          // Libs
          'bower_components/ion-autocomplete/dist/ion-autocomplete.css',
          'bower_components/angucomplete-alt/angucomplete-alt.css',
          'bower_components/ngImgCrop/compile/minified/ng-img-crop.css',
          'bower_components/spectrum/spectrum.css'
      ])
      // .pipe(plumber(errorHandler))
      // .pipe(minifyCss({
      //   keepSpecialComments: 0
      // }))
      .pipe(gulpif(PRODUCTION_BUILD, nano()))
      .pipe(concat("lib.min.css"))
      .pipe(gulpif(codebase.name != 'marketing', gulp.dest(codebase.target_dir + 'build/web/css')))
    );
  };
  return run_codebase_tasks(task);

});

////////////////////////////////
////// Dev tools
////////////////////////////////

gulp.task('serve', 'Serve all front-end codebases', function(done) {
  var task = function(codebase) {
    codebase.browser = serveCodebase(codebase);
  };
  run_codebase_tasks(task);
  // done();
});

var serveCodebase = function(codebase) {
  codebase.browser = browserSync.create();
  codebase.browser.init([],{
    server: {
      baseDir: codebase.target_dir + 'build/web',
    },
    open: false,
    browser: 'default',
    ghostMode: false,
    port: codebase.port + 10,
    ui: {
      port: codebase.port + 40,
    }
  });
  return codebase.browser;
};
gulp.task('serve_e2e', 'Serve codebases for e2e tests', function() {
    for (var c_index in CODEBASES) {
      CODEBASES[c_index].browser = serveCodebase(CODEBASES[c_index]);
    }
});
gulp.task('serve_e2e_app', 'Serve app codebase for e2e tests', function() {
  serveCodebase(CODEBASES[CODEBASE_APP]);
});
gulp.task('serve_e2e_dashboard', 'Serve dashboard codebase for e2e tests', function() {
  serveCodebase(CODEBASES[CODEBASE_DASHBOARD]);
});
gulp.task('serve_e2e_groundcontrol', 'Serve groundcontrol codebase for e2e tests', function() {
  serveCodebase(CODEBASES[CODEBASE_GROUNDCONTROL]);
});

gulp.task('refreeze', 'Refreeze all libraries requirements', shell.task([
  'PYTHONUNBUFFERED=1 pip freeze -r requirements.unstable.txt > requirements.txt'
  ])
);
gulp.task('sync_libs', 'Upgrade all libraries', shell.task([
  'PYTHONUNBUFFERED=1 pip install -r requirements.unstable.txt',
  'npm install .',
  'bower install',
  ])
);

gulp.task('upgrade_all_libs', 'Upgrade and refreeze all libraries', shell.task([
  'PYTHONUNBUFFERED=1 pip install -r requirements.unstable.txt --upgrade',
  'PYTHONUNBUFFERED=1 pip freeze -r requirements.unstable.txt > requirements.txt',
  'npm-check-updates -u',
  'npm install',
  'node_modules/bower-update/bin/bower-update --non-interactive',
  ])
);

gulp.task('check', 'Check for outdated dependencies', shell.task([
  'echo " "; PYTHONUNBUFFERED=1 piprot',
  'outdated',
  ])
);


gulp.task('native_build', 'Build and package for release', shell.task([
  'gulp ionic_build',
  'cd native/ionic; ionic build ios',
  'cd native/ionic; ionic build android --release',
  'echo "Done!"',
  ])
);
gulp.task('ios', 'Build and emulate iOS app', ['ionic_build'], shell.task([
  'ionic emulate ios'
  ], {
    'cwd': 'native/ionic'
  })
);
gulp.task('android', 'Build and emulate android app', ['ionic_build'], shell.task([
  'cd native/ionic; ionic emulate android'
  ])
);
gulp.task('run_android', 'Run app on attached android device', shell.task([
  'cd native/ionic; ionic run android -c -s'
  ])
);
gulp.task('do_ionic_upload', 'Actually do the upload',
  shell.task(['cd native/ionic; ionic upload'])
);
gulp.task('ionic_upload', 'Upload app to ionic view', ['do_ionic_upload'], function() {
  request.post('https://will.buddyup.org/api/ionic/deployed/', function (error, response, body) {
    if (!error && response.statusCode == 200) {
      console.log(body);
    }
  });
});
gulp.task('ionic_deploy', 'Build, then upload app to ionic view', function(done) {
  PRODUCTION_BUILD = true;
  return runSequence('ionic_build', 'ionic_upload', done);
});
gulp.task('import_schools', 'Import all the schools into python and js libs.',
  shell.task(['python3 manage.py import_schools'], {
    'cwd': 'api',
  })
);
gulp.task('reset_db', 'Reset the development database.', (!PRODUCTION_BUILD) ?
    shell.task(['python api/manage.py reset_dev_db']) : function() {
    console.log("Refusing to reset db in production.");
    return done;
  }
);
gulp.task('celery', 'Run celery', shell.task([
  'PYTHONUNBUFFERED=1 C_FORCE_ROOT=true cd api; python3 manage.py celeryd -B -n 8 -Q celery'
  ])
);
gulp.task('shell', 'Run manage.py shell_plus', shell.task([
  'PYTHONUNBUFFERED=1 cd api; python3 manage.py shell_plus'
  ])
);
gulp.task('update', 'Update all python and node requirements', shell.task([
  'PYTHONUNBUFFERED=1 pip install -r requirements.unstable.txt',
  'PYTHONUNBUFFERED=1 cd api; python3 manage.py syncdb',
  'PYTHONUNBUFFERED=1 cd api; python3 manage.py migrate',
  'npm install',
  'bower install',
  ])
);

gulp.task('clear_dist', 'Clear out the distribution', function(){
  var task = function(codebase) {
    // console.log("Clearing");
    del.sync([codebase.target_dir + 'build/web']);
    del.sync([codebase.target_dir + 'dist/web']);
    return gulp.src('');
  };
  return run_codebase_tasks(task);
});


gulp.task('copy_dist', 'Copy the distribution', function(){
  var task = function(codebase) {
    var non_ionic_rev = new RevAll({ dontRenameFile: [/^\/favicon.ico$/g, /^\/demo.html/g, ], dontUpdateReference: [/^\/favicon.ico$/g, /^\/demo.html/g, ]}).revision();
    var ionic_rev = new RevAll({ dontRenameFile: [/^\/favicon.ico$/g,  /^\/index.html/g, /^\/demo.html/g, /^\/error.html/g, /^\/cordova.js/g ], dontUpdateReference: [/^\/favicon.ico$/g,  /^\/index.html/g, /^\/demo.html/g, /^\/error.html/g, /^\/cordova.js/g ]}).revision();
    var marketing_rev = new RevAll({ dontRenameFile: [/^\/favicon.ico$/g,  /^\/index.html/g, /^\/for-teachers.html/g,  /^\/for-schools.html/g, /^\/demo.html/g, /^\/about.html/g, /^\/press.html/g,  /^\/error.html/g,], dontUpdateReference: [/^\/favicon.ico$/g,  /^\/index.html/g, /^\/press.html/g, /^\/for-teachers.html/g,  /^\/for-schools.html/g, /^\/demo.html/g, /^\/about.html/g,  /^\/error.html/g,]}).revision();
    var ionicFilter = gulpFilter([
      "**/*",
      "!lib.uncompressed.*",
      "!main.uncompressed.*",
      "!**/ionic.css",
      "!**/ionic.min.css",
    ]);
    return gulp.src([codebase.target_dir + 'build/web/**',])
      .pipe(gulpif((PRODUCTION_BUILD || BUILD_IONIC), ionicFilter))
      // .pipe(plumber(errorHandler))
      // .pipe(revall({ ignore: [/^\/favicon.ico$/g,  /^\/index.html/g, /^\/error.html/g] }))
      .pipe(gulpif(codebase.name == "marketing", marketing_rev))
      .pipe(gulpif(codebase.name != "marketing" && BUILD_IONIC, ionic_rev))
      .pipe(gulpif(codebase.name != "marketing" && !BUILD_IONIC, ionic_rev))
      .pipe(gulp.dest(codebase.target_dir + 'dist/web'));
  };
  return run_codebase_tasks(task);
});

gulp.task('webdriver-update', 'Update webdriver', shell.task([
  "node_modules/webdriver-manager/bin/webdriver-manager update"
]));
gulp.task('webdriver-standalone', 'Run webdriver standalone', protractor.webdriver_standalone);


function runProtractorSuite(codebase, done) {
  IN_TESTS = true;
  run_api(codebase.api_port)();

  return gulp.src(codebase.base_dir + 'tests/js/protractor/**/*Spec.js')
    .pipe(protractor.protractor({
      // configFile: 'protractor.conf.js'
      configFile: codebase.base_dir + 'src/tests/js/protractor.conf.js'
    }))
    .on('error', function (e) {
      // Make sure failed tests cause gulp to exit non-zero
      process.exit(1);
    })
    .on('end', function () {
      // Close browser sync server
      codebase.browser.exit();
      done();
    });
}

function runProtractor (done) {
  return run_codebase_tasks(runProtractorSuite);
}
function runProtractorApp(done) {
  // gulp.run('run_api');
  var codebase_app = CODEBASES[CODEBASE_APP];
  return runProtractorSuite(codebase_app, done);
}
function runProtractordashboard(done) {
  var CODEBASE_DASHBOARD = CODEBASES[CODEBASE_DASHBOARD];
  return runProtractorSuite(CODEBASE_DASHBOARD, done);
}
function runProtractorGroundcontrol(done) {
  var codebase_groundcontrol = CODEBASES[CODEBASE_GROUNDCONTROL];
  return runProtractorSuite(codebase_groundcontrol, done);
}
gulp.task('build_test', 'Build, in test mode', function(done){
  IN_TESTS = true;
  return runSequence('build', done);
});


gulp.task('protractor', 'Run protractor for all apps', ['build_test', 'serve_e2e', 'webdriver-update'], runProtractor);
gulp.task('protractor:app', 'Run protractor for app', ['serve_e2e_app', 'webdriver-update'], runProtractorApp);
gulp.task('protractor:dashboard', 'Run protractor for dashboard', ['serve_e2e_dashboard', 'webdriver-update'], runProtractordashboard);
gulp.task('protractor:groundcontrol', 'Run protractor for groundcontrol', ['serve_e2e_groundcontrol', 'webdriver-update'], runProtractorGroundcontrol);
// gulp.task('protractor:dist', ['serve:e2e-dist', 'webdriver-update'], runProtractor);

gulp.task('build', 'Build all apps', function(done) {
    return runSequence('clear_dist', 'scripts', 'copy_dist', done);
});
gulp.task('build_production', 'Build all apps, for PRODUCTION', function(done) {
    // TODO: Https
    BUDDYUP_API_ENDPOINT = "https://api.buddyup.org";
    FIREBASE_ENDPOINT = "https://buddyup.firebaseio.com";
    PRODUCTION_BUILD = true;
    return runSequence('clear_dist', 'scripts', 'copy_dist', done);
});
gulp.task('push_aws', 'Push apps to AWS', ['build_production'], function(done){
  var task = function(codebase) {
    if (codebase.native_app !== true) {
      var aws_options = {
          "accessKeyId": process.env.AWS_ACCESS_KEY_ID,
          "secretAccessKey": process.env.AWS_SECRET_ACCESS_KEY,
          "params": {
            "Bucket": codebase.aws_bucket,
          },
          // "patternIndex": /^\/index\-[a-f0-9]{4}\.html(\.gz)*$/gi,
          "patternError": /^\/error\-[a-f0-9]{4}\.html(\.gz)*$/gi,
          "distributionId": codebase.aws_dist_id,
          "region": codebase.aws_region
      };
      var publisher = awspublish.create(aws_options);
      var headers = {
           // 'Cache-Control': 'max-age=315360000, no-transform, public',
           'x-amz-acl': 'public-read',

           // 'Accept-Encoding': 'Vary',
           // 'Accept-Encoding': 'gzip',
      };
      return gulp.src([codebase.target_dir + 'dist/web/**/*'])
          // .pipe(plumber(errorHandler))
           // gzip, Set Content-Encoding headers and add .gz extension
           // { ext: '.gz' })
          .pipe(awspublish.gzip())

          // publisher will add Content-Length, Content-Type and headers specified above
          // If not specified it will set x-amz-acl to public-read by default
          .pipe(parallelize(publisher.publish(headers), 10))
          // .pipe(publisher.publish())

          // create a cache file to speed up consecutive uploads
          .pipe(publisher.cache())

           // print upload updates to console
          .pipe(awspublish.reporter())

          // update cloudfront edges
          .pipe(cloudfront(aws_options));
    }
  };
  return run_codebase_tasks(task);
});
gulp.task('purge_cloudflare', 'Purge Cloudflare', function(done){

  var api_key = process.env.CLOUDFLARE_KEY;
  var email = process.env.CLOUDFLARE_EMAIL;
  var result = null;

  console.log("Purging Cloudflare Cache...");
// request.debug = true
  // Get the zone from cloudflare
  var request_headers = {
      "X-Content-Type": "application/json",
      "Content-Type": "application/json",
      "content-type": "application/json",
      "X-Auth-Key": api_key,
      "X-Auth-Email": email,
  };
  url = "https://api.cloudflare.com/client/v4/zones/";
  params = {
      "name": "buddyup.org",
      "status": "active",
      "page": 1,
      "per_page": 20,
      "order": "status",
      "direction": "desc",
      "match": "all",
  };
  request.get({
      url: url,
      headers: request_headers,
      form: params,
      // json:true,
    }, function (error, response, body) {
    if (!error && response.statusCode == 200) {
      result = JSON.parse(body).result;

      if (result)  {
          zone_id = result[0]["id"];
          url = url + zone_id + "/purge_cache";

          data = {
              "purge_everything": true
          };

          request({
              method: "delete",
              url: url,
              headers: request_headers,
              body: data,
              json: true,
            }, function (error, response, body) {
            if (!error && response.statusCode == 200) {
              console.log("Cache purged.");
            } else {
              console.log("Error purging cache: ");
              console.log(response.statusCode);
              console.log(body);

              process.exit(code=1);
            }
          });
      }


    } else {
      console.log("Error getting cloudflare zone.");
      console.log(response.statusCode);
      console.log(body);

      process.exit(code=1);
    }
  });
});
// gulp.task('push_heroku', 'Push API to Heroku', shell.task([
//   'PYTHONUNBUFFERED=1 git push git@heroku.com:buddyup-api.git master; heroku run "cd api; python3 manage.py migrate" --app buddyup-api'
//   ])
// );
gulp.task('deploy', 'Deploy apps', ['push_heroku', 'push_aws', 'purge_cloudflare'], function() {
    // runSequence('push_heroku', 'push_aws');
});
var run_api = function(port) {
  return shell.task(['PYTHONUNBUFFERED=1 python3 manage.py runserver 0.0.0.0:' + port], {
    'cwd': 'api',
    'ignoreErrors': true
  });
};
gulp.task('run_api', 'Run the API for development', run_api(8120));
gulp.task('migrate', 'Run Python migrations', shell.task(['PYTHONUNBUFFERED=1 python3 manage.py migrate'], {
    'cwd': 'api'
}));

gulp.task('blaze', 'Compile the blaze rules', shell.task('../node_modules/blaze_compiler/bin/blaze.js rules.yml'));
gulp.task('blaze_dev', 'Auto-reload the blaze rules on save', function(){
  gulp.watch(['rules.yml'], function(event) {
      gulp.run('blaze');
    });
});
gulp.task('deploy_blaze', 'Push the blaze rules to the server.', function() {
  var key = (PRODUCTION_BUILD) ? FIREBASE_LIVE_KEY : FIREBASE_KEY;
  var end = (PRODUCTION_BUILD) ? FIREBASE_LIVE_ENDPOINT : FIREBASE_ENDPOINT;
  console.log("Deploying to " + end);
  var endpoint = end + "/.settings/rules.json?auth=" + key;
  fs.createReadStream('rules.json').pipe(
    request.put(endpoint, function (error, response, body) {
      if (!error && response.statusCode == 200) {
        console.log("Blaze Rules Deployed.");
      } else {
        console.log("Error deploying blaze rules.");
        console.log(response.statusCode);
        console.log(body);
        process.exit(code=1);
      }
    })
  );
});

function buildAndRunCodebase(codebase) {
  gulp.watch([
    codebase.base_dir + 'src/js/**/*.js',
    'frontends/common/js/**/*.js',
    '!' + codebase.base_dir + 'src/js/**/templates_common.js',
    '!' + codebase.base_dir + 'src/js/**/templates_desktop.js',
    '!' + codebase.base_dir + 'src/js/**/templates_shared.js',
    '!' + codebase.base_dir + 'src/js/**/templates_ionic.js',
    ], function(event) {
      if (codebase.browser) {
        gulp.run('scripts', codebase.browser.reload);
      } else {
        gulp.run('scripts');
      }
    });
  gulp.watch([
    'frontends/common/less/*',
    codebase.base_dir + 'src/less/**',
    codebase.base_dir + 'src/sass/**',
  ], function(event) {
    if (codebase.browser) {
      runSequence('copy', codebase.browser.reload);
    } else {
      gulp.run('copy');
    }
  });
  gulp.watch([
    codebase.base_dir + 'src/templates/**/*.html',
    'frontends/common/templates/**/*.html',
    ], function(event) {
      if (codebase.browser) {
        gulp.run('scripts', codebase.browser.reload);
      } else {
        gulp.run('scripts');
      }
  });
  gulp.watch(['bower_components/ionic/scss/**/*.scss'], ['sass', codebase.browser.reload]);
  // gulp.watch(['rules.yml'], ['blaze']);

  gulp.watch([
    'frontends/common/img/*',
    codebase.base_dir + 'src/img/**',
    codebase.base_dir + 'src/assets/fonts/**',
    codebase.base_dir + 'src/assets/misc/**',
  ], function(event) {
    if (codebase.browser) {
      runSequence('copy', codebase.browser.reload);
    } else {
      gulp.run('copy');
    }
  });
  gulp.watch(['*', '*.js'], function(e){
    // console.log("change");
    // console.log(e);
  });
}
// The default task (called when you run `gulp`)
gulp.task('dev', 'Run all apps for development', ['build'], function() {
  // runSequence('translate_compile', 'less', 'sass', 'scripts', 'copy');
  gulp.run('run_api');
  gulp.run('celery');
  gulp.run('serve');
  // Watch files and run tasks if they change
  for (var c_index in CODEBASES) {
    buildAndRunCodebase(CODEBASES[c_index]);
  }
});

gulp.task('app', 'Develop on the main app', function(codebase_name) {
  CODEBASES = [CODEBASES[CODEBASE_APP]];
  return gulp.run('dev');
});

gulp.task('gc', 'Develop on ground control', function(codebase_name) {
  CODEBASES = [CODEBASES[CODEBASE_GROUNDCONTROL]];
  return gulp.run('dev');
});

gulp.task('dashboard', 'Develop on the dashboard app', function(codebase_name) {
  CODEBASES = [CODEBASES[CODEBASE_DASHBOARD]];
  return gulp.run('dev');
});
gulp.task('marketing', 'Develop on the marketing app', function(codebase_name) {
  CODEBASES = [CODEBASES[CODEBASE_MARKETING]];
  return gulp.run('dev');
});

gulp.task('ionic_build', 'Build the ionic app', function(codebase_name) {
  CODEBASES = [CODEBASES[CODEBASE_IONIC]];
  BUILD_IONIC = true;
  del.sync(['native/code/dist']);
  return gulp.run('build_production');
});
gulp.task('ionic_build_dev', 'Build the ionic app in dev mode', function(codebase_name) {
  CODEBASES = [CODEBASES[CODEBASE_IONIC]];
  BUILD_IONIC = true;
  BUILD_IONIC_DEV = true;
  del.sync(['native/code/dist']);
  return gulp.run('build_production');
});

gulp.task('ionic_dev_build', 'Build the ionic app', function(done) {
  console.log("THIS IS INCOMPLETE AND UNSUPPORTED.")
  CODEBASES = [CODEBASES[CODEBASE_IONIC]];
  // PRODUCTION_BUILD = false;
  BUILD_IONIC = true;
  del.sync(['native/code/dist']);
  return runSequence('clear_dist', 'scripts', 'copy_dist', done);
});
