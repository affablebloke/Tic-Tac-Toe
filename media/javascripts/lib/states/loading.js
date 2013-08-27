/*
 Sets up the 3D renderer and loads all 3D assets.
 */
define(['jquery', 'lib/game', 'three', 'lib/state.manager'], function ($, game, THREE, stateManager) {
    'use strict';

    var SCREEN_WIDTH = $(window).width();
    var SCREEN_HEIGHT = $(window).height();

    function columnToAlpha(col) {
        if (col == 0) {
            return 'A';
        } else if (col == 1) {
            return 'B';
        } else {
            return 'C';
        }
    }


    return {
        enter: function (ctx) {
            var boardDfd = $.Deferred();
            var tileDfd = $.Deferred();

            // setup clock and camera
            ctx.clock = new THREE.Clock();
            ctx.camera = new THREE.PerspectiveCamera(75, SCREEN_WIDTH / SCREEN_HEIGHT, 1, 100000);
            ctx.camera.position.z = 45;
            ctx.camera.position.y = 65;
            ctx.scene = new THREE.Scene();
            ctx.cameraTarget = new THREE.Vector3(0, 0, 0);


            //load game assets
            var loader = new THREE.JSONLoader();

            var boardTexture = THREE.ImageUtils.loadTexture('blender/textures/front_wood_texture.png');
            var boardMaterial = new THREE.MeshPhongMaterial({
                map: boardTexture,
                //    normalMap: boardTexture,
                //    specularMap: boardTexture,
                color: 0xFFFFFF,
                ambient: 0xCCCCCC,
                specular: 0xFFFFFF,
                shininess: 5,
                //metal: false,
                shading: THREE.SmoothShading,
                perPixel: true,
                overdraw: true
                //bumpScale: 1.0,
            });

            loader.load("blender/board.js", function (geometry, materials) {
                var mesh = new THREE.Mesh(geometry, boardMaterial);

                mesh.castShadow = true;
                mesh.receiveShadow = true;
                mesh.dynamic = true;

                mesh.position.set(0, 0, 0);
                mesh.scale.set(5, 5, 5);
                ctx.parent.add(mesh);
                boardDfd.resolve();

            });


            var tileTexture = THREE.ImageUtils.loadTexture('blender/textures/nought_cross_texture.png');
            var tileMaterial = new THREE.MeshPhongMaterial({
                map: tileTexture,
                //    normalMap: boardTexture,
                //    specularMap: boardTexture,
                color: 0xFFFFFF,
                ambient: 0xCCCCCC,
                specular: 0xFFFFFF,
                shininess: 5,
                //metal: false,
                shading: THREE.SmoothShading,
                perPixel: true,
                overdraw: true
                //bumpScale: 1.0,
            });

            loader.load("blender/tile.js", function (geometry, materials) {
                var hSpace = 16;
                var zSpace = 15;
                game.objects = [];
                game.pieces = {};
                for (var i = 0; i < 3; i++) {
                    for (var j = 0; j < 3; j++) {
                        var column = columnToAlpha(j);
                        var mesh = new THREE.Mesh(geometry, tileMaterial);

                        mesh.castShadow = true;
                        mesh.receiveShadow = true;
                        mesh.dynamic = true;

                        mesh.position.set(j * hSpace - hSpace, -0.5, i * zSpace - zSpace);
                        mesh.scale.set(5, 5, 5);
                        ctx.parent.add(mesh);
                        var cell = column + (i + 1);
                        game.pieces[location] = mesh;
                        game.objects.push(mesh);
                        mesh.userData = {'cell': cell};
                    }
                }
                tileDfd.resolve();

            });


            //setup 3D objects
            //parenting
            ctx.parent = new THREE.Object3D();
            ctx.scene.add(ctx.parent);

            //lighting
            var ambient = new THREE.AmbientLight(0x777777);
            ctx.scene.add(ambient);

            var directionalLight = new THREE.DirectionalLight(0x444444);
            directionalLight.position.set(0, 200, 100).normalize();
            ctx.scene.add(directionalLight);

            //create renderer
            try {
                ctx.renderer = new THREE.WebGLRenderer({antialias: true});
                ctx.renderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
                $("#renderer").append(ctx.renderer.domElement);
            }
            catch (e) {
                console.log(e.message);
            }

            ctx.game = game.init(ctx);


            // Window resize fix
            $(window).resize(function () {

                if (ctx.renderer) {
                    var width = $(window).width();
                    var height = $(window).height();
                    var windowHalfX = width / 2;
                    var windowHalfY = height / 2;
                    ctx.camera.aspect = width / height;
                    ctx.camera.updateProjectionMatrix();
                    ctx.renderer.setSize(width, height);
                    ctx.renderer.clear();
                    ctx.renderer.render(ctx.scene, ctx.camera);

                }
            });


            $.when(boardDfd.promise(), tileDfd.promise())
                .done(function () {
                    stateManager.go('/menu');
                });

        },
        exit: function (ctx) {

        }
    }
});