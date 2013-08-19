require.config({
    paths: {
        jquery: '../scripts/components/jquery/jquery',
        bootstrap: 'components/bootstrap/dist/js/bootstrap.min'
    },
    shim: {
        bootstrap: {
            deps: ['jquery'],
            exports: 'jquery'
        }
    }
});

require(['app', 'jquery', 'bootstrap'], function (app, $) {
    'use strict';


});
