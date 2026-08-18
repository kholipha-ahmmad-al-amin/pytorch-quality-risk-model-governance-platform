import pytest
from src.domain import *
engineer={'role':'ml-engineer'};governor={'role':'model-governor'}
def test_train_approve_predict():
 g=ModelGovernance();g.train(engineer);g.approve(governor);assert 0<=g.predict([1,0,1])<=1
def test_block_unapproved_prediction():
 with pytest.raises(DomainError):ModelGovernance().predict([1,0,1])
def test_authorize_training():
 with pytest.raises(DomainError):ModelGovernance().train(governor)
def test_authorize_approval():
 with pytest.raises(DomainError):ModelGovernance().approve(engineer)
def test_validate_features():
 g=ModelGovernance();g.train(engineer);g.approve(governor)
 with pytest.raises(DomainError):g.predict([1,0])
