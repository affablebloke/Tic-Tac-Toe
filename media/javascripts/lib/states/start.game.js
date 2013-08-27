/*
 Starts the game.
 */
define(['jquery', 'lib/game', 'three', 'tween', 'lib/state.manager'], function ($, game, THREE, TweenMax, stateManager) {
    'use strict';

    var incr = 0;

    var renderFunc = function (ctx) {
        var delta = ctx.clock.getDelta();

        ctx.camera.lookAt(ctx.cameraTarget);
        ctx.renderer.render(ctx.scene, ctx.camera);

        var maxRotation = 5 * Math.PI / 180
        ctx.parent.rotation.y = (Math.sin(incr) * maxRotation);
        ctx.parent.rotation.z = (Math.sin(incr) * maxRotation);
        ctx.parent.rotation.x = (Math.sin(incr) * maxRotation);
        incr += .0055;

        //ctx.camera.position.x += ( mouseX - ctx.camera.position.x ) * .001 + 75;
        //ctx.camera.position.y = ((mouseY - ctx.camera.position.y ) * .1 + 10) + 75;
    }


    return {
        enter: function (ctx) {
            game.reset(ctx);
            var token = "";
            if (ctx.token)
                token = ctx.token;
            $.get("/api/game?token=" + token)
                .done(function (data) {
                    ctx.token = data['token'];
                    var cells = data['cells'];
                    for(var i = 0; i < cells.length; i ++){
                        var mark = cells[i];
                        if(mark){
                           game.markObject(game.objects[i], mark);
                        }
                    }
                    stateManager.go('/player');
                })
                .fail(function () {
                    stateManager.go('/menu');
                });

            $('.start-menu').css('visibility', 'hidden').css('display', 'none');

            game.setRenderFunc(renderFunc);
            TweenMax.to(ctx.camera.position, 2.5, {
                z: 10,
                y: 45,
                ease: Elastic.easeOut,
                delay: 0.0,
                onComplete: function () {
                    incr = 0;
                }
            });

            TweenMax.to(ctx.parent.rotation, 2.5, {
                x: 0,
                z: 0,
                y: 0,
                ease: Elastic.easeOut,
                delay: 0.0
            });

            for (var i = 0; i < game.objects.length; i++) {
                TweenMax.to(game.objects[i].rotation, 2.5, {
                    x: 0,
                    z: 0,
                    y: 0,
                    ease: Elastic.easeOut,
                    delay: 0.0
                });
            }


        },
        exit: function (ctx) {

        }
    }
});