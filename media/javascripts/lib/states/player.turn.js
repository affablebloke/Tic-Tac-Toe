/*
 Player turn state.
 */
define(['jquery', 'lib/game', 'three', 'lib/state.manager'], function ($, game, THREE, stateManager) {
    'use strict';

    var mouseX, mouseY = 0;
    var projector = new THREE.Projector();


    return {
        enter: function (ctx) {

            $('.player-turn').removeClass('fadeInDown');
            $('.player-turn').removeClass('fadeOutUp');

            $('.player-turn').css('visibility', 'visible').css('display', 'block');
            $('.player-turn').addClass('animated fadeInDown');

            $(window).on('mousemove', function (event) {
                mouseX = event.clientX - ($(window).width() / 2);
                mouseY = event.clientY - ($(window).height() / 2);
            });

            $(window).on('mousedown', function (event) {
                event.preventDefault();

                var vector = new THREE.Vector3(( event.clientX / window.innerWidth ) * 2 - 1, -( event.clientY / window.innerHeight ) * 2 + 1, 0.5);
                projector.unprojectVector(vector, ctx.camera);

                var raycaster = new THREE.Raycaster(ctx.camera.position, vector.sub(ctx.camera.position).normalize());

                var intersects = raycaster.intersectObjects(game.objects);

                if (intersects.length > 0 && !intersects[0].object.userData.taken) {
                    $(window).off('mousedown');
                    game.markCell(intersects[0].object.userData.cell, 'X');
                    $.post('/api/submit_move', {'token': ctx.token, 'mark': 'X', 'cell': intersects[0].object.userData.cell})
                        .done(function (data) {
                            game.checkForWin(ctx)
                                .done(function (data) {
                                    if (data.cats_game) {
                                        ctx.cats_game = true;
                                        stateManager.go('/over')
                                    } else if (data.winner) {
                                        ctx.winner = data.winner;
                                        stateManager.go('/over')
                                    } else {
                                        stateManager.go('/ai');
                                    }
                                });

                        });
                }
            });

        },
        exit: function (ctx) {
            $(window).off('mousemove');
            $(window).off('mousedown');

            $('.player-turn').removeClass('fadeInDown');
            $('.player-turn').addClass('fadeOutUp');
        }
    }
});


