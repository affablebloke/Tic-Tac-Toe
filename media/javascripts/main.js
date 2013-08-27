require.config({
    paths: {
        jquery: '../scripts/components/jquery/jquery.min',
        lib: '../scripts/lib',
        three: 'components/threejs/build/three.min',
        bootstrap: 'components/bootstrap/dist/js/bootstrap.min',
        tween: 'components/gsap/src/minified/TweenMax.min',
        ease: 'components/gsap/src/minified/easing/EasePack.min'
    },
    shim: {
        bootstrap: {
            deps: ['jquery'],
            exports: 'jquery'
        },
         three: {
            exports: 'THREE'
        },
        tween: {
            exports: 'TweenMax'
        },
        ease: {
            exports: 'Elastic'
        }
    }
});

require(['app', 'jquery', 'bootstrap'], function (app) {
    'use strict';
    app.run();
});
