/*
 Loads the menu.
 */
define(['jquery', 'lib/game', 'three', 'tween', 'lib/state.manager'], function ($, game, THREE, TweenMax, stateManager) {
    'use strict';

    var animateInterval;
    var incr = 0;

    var renderFunc = function (ctx) {
        var delta = ctx.clock.getDelta();

        ctx.camera.lookAt(ctx.cameraTarget);
        ctx.renderer.render(ctx.scene, ctx.camera);

        var maxRotation = 45 * Math.PI / 180
        ctx.parent.rotation.y = (Math.sin(incr) * maxRotation);
        incr += .005;
        //ctx.parent.rotation.y = incr;

        //ctx.camera.position.x += ( mouseX - ctx.camera.position.x ) * .001 + 75;
        //ctx.camera.position.y = ((mouseY - ctx.camera.position.y ) * .1 + 10) + 75;
    }

    function randomTileFlip(ctx) {
        var objects = game.objects;
        var tile = objects[parseInt(Math.random() * objects.length)];
        var randomDegrees = parseInt(Math.random() * 5) * 120;
        if (randomDegrees % 360 == 0)
            randomDegrees = 120;

        TweenMax.to(tile.rotation, 2.5, {
            z: (randomDegrees * (Math.PI / 180)),
            ease: Elastic.easeOut,
            delay: 0.0
        });
    }

    return {
        enter: function (ctx) {
            $('.start-menu').removeClass('fadeInDown');
            $('.start-menu').removeClass('fadeOutUp');
            $('#play-button').on('click', function(event){
                stateManager.go('/start');
            });

            $('.start-menu').css('visibility', 'visible').css('display', 'block');
            $('.start-menu').addClass('animated fadeInDown');
            game.setRenderFunc(renderFunc);
            TweenMax.to(ctx.camera.position, 5, {
                z: 25,
                //ease: Elastic.easeOut,
                delay: 0.0
            });
            animateInterval = setInterval(function () {
                randomTileFlip(ctx);
            }, 250);

        },
        exit: function (ctx) {
            $('#play-button').off('click');
            $('.start-menu').removeClass('fadeInDown');
            $('.start-menu').addClass('fadeOutUp');
            clearInterval(animateInterval);
        }
    }
});