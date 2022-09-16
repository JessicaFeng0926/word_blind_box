from login import login_check

def test_with_correct_username_and_password():
    user = login_check('jessica','123456')
    assert user.username=='jessica' and user.password=='123456'

def test_with_correct_username_wrong_password():
    user = login_check('jessica','123444')
    assert user is None 

def test_with_wrong_username_correct_password():
    user = login_check('jolina','123456')
    assert user is None 

def test_with_empty_username():
    user = login_check('','123456')
    assert user is None 

def test_with_empty_password():
    user = login_check('jessica','')
    assert user is None 



