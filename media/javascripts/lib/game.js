/*
 Controls the game.
 */
define(['jquery', 'three', 'tween'], function ($, THREE, TweenMax) {
    'use strict';

    var incr = 0;
    var renderFunc;
    var map = {'A1': 0, 'B1': 1, 'C1': 2, 'A2': 3, 'B2': 4, 'C2': 5, 'A3': 6, 'B3': 7, 'C3': 8};

    return {

        init: function (ctx) {

            var ref = this;
            // Paul Irish (http://www.paulirish.com/2011/requestanimationframe-for-smart-animating/)
            // shim layer with setTimeout fallback
            window.requestAnimFrame = (function () {
                return  window.requestAnimationFrame ||
                    window.webkitRequestAnimationFrame ||
                    window.mozRequestAnimationFrame ||
                    function (callback) {
                        window.setTimeout(callback, 1000 / 60);
                    };
            })();

            (function animloop() {
                requestAnimFrame(animloop);
                ref.render(ctx);
            })();

        },

        setRenderFunc: function (func) {
            renderFunc = func;
        },

        render: function (ctx) {
            if (ctx.renderer && renderFunc) {
                renderFunc(ctx);
            }
        },

        markCell: function (cell, mark) {
            var degrees = (mark == 'X') ? 240 : 120;
            var index = map[cell];
            var object = this.objects[index];
            object.userData.taken = true;
            TweenMax.to(object.rotation, 2.5, {
                z: degrees * (Math.PI / 180),
                ease: Elastic.easeOut,
                delay: 0.0
            });
        },

        markObject: function (object, mark) {
            var degrees = (mark == 'X') ? 120 : 240;
            object.userData.taken = true;
            TweenMax.to(object.rotation, 2.5, {
                z: degrees * (Math.PI / 180),
                ease: Elastic.easeOut,
                delay: 0.0
            });
        },

        checkForWin: function(ctx){
            return  $.get('/api/check_for_win', {'token': ctx.token});
        },

        reset: function (ctx) {
            delete ctx.winner;
            delete ctx.cats_game;
            delete ctx.token;
            if (!this.objects)
                return;
            for (var i = 0; i < this.objects.length; i++) {
                var object = this.objects[i];
                object.userData.taken = false;
            }
        }
    }


});