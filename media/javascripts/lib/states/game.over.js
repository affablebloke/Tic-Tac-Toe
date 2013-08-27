/*
 Game over.
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

            if(ctx.cats_game){
                $('#message').html('CATS GAME!');
            }else if(ctx.winner == 'X'){
                $('#message').html('YOU WIN!');
            }else{
                $('#message').html('YOU LOSE!');
            }

            $('.play-again-menu').removeClass('fadeInDown');
            $('.play-again-menu').removeClass('fadeOutUp');
            $('#play-again-button').on('click', function(event){
                stateManager.go('/start');
            });



            $('.play-again-menu').css('visibility', 'visible').css('display', 'block');
            $('.play-again-menu').addClass('animated fadeInDown');
            game.setRenderFunc(renderFunc);
            TweenMax.to(ctx.camera.position, 5, {
                z: 25,
                //ease: Elastic.easeOut,
                delay: 0.0
            });
//            animateInterval = setInterval(function () {
//                randomTileFlip(ctx);
//            }, 250);

        },
        exit: function (ctx) {
            $('#play-again-button').off('click');
            $('.play-again-menu').removeClass('fadeInDown');
            $('.play-again-menu').addClass('fadeOutUp');
            clearInterval(animateInterval);
        }
    }
});