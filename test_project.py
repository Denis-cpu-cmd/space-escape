import project

player_reactor = project.Player("alpha", (0,2))
player_elsewhere = project.Player("beta", (1,1))
player_winner = project.Player("teta", (2,2), inventory = ["battery", "access_card"])
player_dead = project.Player("teta", (2,2), inventory = ["battery", "access_card"], oxygen = 0)
player_missing = project.Player("teta", (2,2), inventory = ["access_card"])
player_not = project.Player("teta", (1,2), inventory = ["battery", "access_card"])

def test_get_new_position():
    assert project.get_new_position((1,1), "right") == (2,1)
    assert project.get_new_position((1,1), "left") == (0,1)
    assert project.get_new_position((1,1), "up") == (1,0)
    assert project.get_new_position((1,1), "down") == (1,2)

def test_calculate_oxygen_reactor():
    assert project.calculate_oxygen(player_reactor) == "Warning! You are losing more oxygen here."
    assert player_reactor.oxygen == 90

def test_calculate_oxygen_elsewhere():
    project.calculate_oxygen(player_elsewhere)
    assert player_elsewhere.oxygen == 95

def test_check_win_winner():
    assert project.check_win(player_winner) == True

def test_check_win_death():
    assert project.check_win(player_dead) == False

def test_check_win_missing_items():
    assert project.check_win(player_missing) == False

def test_check_win_not_escapepod():
    assert project.check_win(player_not) == False


