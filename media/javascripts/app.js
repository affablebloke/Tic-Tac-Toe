/*
 Initialize the application.
 */
define(['jquery', 'lib/state.manager', 'lib/states/loading', 'lib/states/ai.turn', 'lib/states/player.turn',
    'lib/states/start.menu', 'lib/states/start.game', 'lib/states/game.over'], function ($, stateManager, loadingState, aiTurnState,
                                                                 playerTurnState, menuState, startGameState, gameOverState) {
    'use strict';

    var ctx = {};
    stateManager.add('/loading', loadingState);
    stateManager.add('/start', startGameState);
    stateManager.add('/menu', menuState);
    stateManager.add('/player', playerTurnState);
    stateManager.add('/ai', aiTurnState);
    stateManager.add('/over', gameOverState);

    return {
        run: function () {
            stateManager.ctx = ctx;

            setTimeout(function () {
                stateManager.go('/loading');
            }, 10);
        }
    }
});