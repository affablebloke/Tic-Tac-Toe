/*
 AI turn state.
 */
define(['jquery', 'lib/game', 'three', 'lib/state.manager'], function ($, game, THREE, stateManager) {
    'use strict';

    var mouseX, mouseY = 0;
    var projector = new THREE.Projector();


    return {
        enter: function (ctx) {

            $('.ai-turn').removeClass('fadeInDown');
            $('.ai-turn').removeClass('fadeOutUp');

            $('.ai-turn').css('visibility', 'visible').css('display', 'block');
            $('.ai-turn').addClass('animated fadeInDown');

            setTimeout(function () {

                $.post('/api/submit_move', {'token': ctx.token, 'mark': 'O'})
                    .done(function (data) {
                        game.markCell(data.cell, data.team);
                        game.checkForWin(ctx)
                                .done(function (data) {
                                    if (data.cats_game) {
                                        ctx.cats_game = true;
                                        stateManager.go('/over')
                                    } else if (data.winner) {
                                        ctx.winner = data.winner;
                                        stateManager.go('/over')
                                    } else {
                                        stateManager.go('/player');
                                    }
                                });
                    });

                }, 2000
            );

        },
        exit: function (ctx) {
            $('.ai-turn').removeClass('fadeInDown');
            $('.ai-turn').addClass('fadeOutUp');
        }
    }
});