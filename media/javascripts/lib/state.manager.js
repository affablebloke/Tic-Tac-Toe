/*
 A FSM for flow control.
 */
define([], function () {
    'use strict';

    var stack = []    // current active states
        , queue = []    // next states
        , states = {}   // available states
        , context = {};


    return {
        go: function (path) {

            if (!states[path]) {
                throw new Error('path does not exist: ' + path);
            }
            while (stack.length) {
                var state = stack.pop();
                state.exit(context);
            }

            stack = stack.concat(states[path]);
            queue = queue.concat(states[path]);

            while (queue.length) {
                var state = queue.shift();
                state.enter(context);
            }

        },
        add: function (path, state) {
            if (!states[path]) {
                states[path] = [state];
            } else {
                states[path].push(state);
            }
        },

        ctx: context
    }
});