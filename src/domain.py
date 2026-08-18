import torch
from torch import nn
class DomainError(Exception):
 def __init__(self,code,message):super().__init__(message);self.code=code
class RiskNet(nn.Module):
 def __init__(self):super().__init__();self.layers=nn.Sequential(nn.Linear(3,4),nn.ReLU(),nn.Linear(4,1),nn.Sigmoid())
 def forward(self,x):return self.layers(x)
class ModelGovernance:
 def __init__(self):self.model=RiskNet();self.status='draft';self.audits=[]
 def train(self,actor):
  if actor['role']!='ml-engineer':raise DomainError('FORBIDDEN','ML engineer role is required')
  x=torch.tensor([[1.,0.,0.],[0.,1.,1.],[1.,1.,0.],[0.,0.,1.]]);y=torch.tensor([[0.],[1.],[1.],[0.]])
  opt=torch.optim.SGD(self.model.parameters(),lr=.1);loss=nn.BCELoss()
  for _ in range(20):opt.zero_grad();value=loss(self.model(x),y);value.backward();opt.step()
  self.status='trained';self.audits.append('model.trained');return float(value)
 def approve(self,actor):
  if actor['role']!='model-governor':raise DomainError('FORBIDDEN','Model governor role is required')
  if self.status!='trained':raise DomainError('CONFLICT','Only trained models can be approved')
  self.status='approved';self.audits.append('model.approved');return self.status
 def predict(self,features):
  if self.status!='approved':raise DomainError('CONFLICT','Only approved models may serve predictions')
  if not isinstance(features,list) or len(features)!=3:raise DomainError('VALIDATION','Exactly three numeric features are required')
  with torch.no_grad():return float(self.model(torch.tensor([features],dtype=torch.float32))[0][0])
