from utils import utils
from apps.api.game_logic import AI
from django.views.decorators.http import require_http_methods
from apps.api.models import TicTacToeGame

@require_http_methods(["GET"])
@utils.json_view
def game(request):
    token = request.GET.get('token', '')
    game = TicTacToeGame.create()
    if token:
        objects = TicTacToeGame.objects.all().filter(token=token)
        game = objects[0]

    game.save()
    return {'token': game.token, 'cells': game.game_state.cells()}

@require_http_methods(["POST"])
@utils.json_view
def submit_move(request):
    token = request.POST.get('token','')
    mark = request.POST.get('mark','')
    cell = request.POST.get('cell','')
    objects = TicTacToeGame.objects.all().filter(token=token)
    game = objects[0]

    player = game.player_1
    if player.team != mark:
        player = game.player_2

    ai = AI(game, player)
    if player.is_human:
        ai.mark_position(cell)
    else:
        ai.run()

    game.game_state.save()
    cell = ""

    if player.team.upper() == 'X':
        cell = game.game_state.last_move_x
    else:
        cell = game.game_state.last_move_o

    return {'team': player.team, 'cell': cell.upper()}


@require_http_methods(["GET"])
@utils.json_view
def check_for_win(request):
    token = request.GET.get('token','')

    objects = TicTacToeGame.objects.all().filter(token=token)
    game = objects[0]

    ai = AI(game, game.player_1)
    x_win_list = ai.check_wins(game.game_state.crosses_bitmask())
    o_win_list = ai.check_wins(game.game_state.noughts_bitmask())

    if game.game_state.board_positions_available_bitmask() == 0 and len(x_win_list) == 0 and len(o_win_list) == 0:
        return {'cats_game': True}
    elif len(x_win_list) > 0:
        return {'winner': 'X'}
    elif len(o_win_list) > 0:
        return {'winner': 'O'}

    return {'no_winner': True}