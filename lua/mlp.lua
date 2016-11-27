require 'nn';

dataset = torch.load('data/dataset.th')

mlp = nn.Sequential()  -- A network that makes predictions given x.
mlp:add(nn.Linear(4, 48))
mlp:add(nn.Tanh())
mlp:add(nn.Linear(48, 48))
mlp:add(nn.Tanh())
mlp:add(nn.Linear(48, 48))
mlp:add(nn.Tanh())
mlp:add(nn.Linear(48, 48))
mlp:add(nn.Tanh())
mlp:add(nn.Linear(48, 48))
mlp:add(nn.Tanh())
mlp:add(nn.Linear(48, 48))

criterion = nn.MSECriterion()
-- trainer = nn.StochasticGradient(mlp, criterion)
-- trainer.learningRate = 0.01
-- trainer:train(dataset)



for i = 1,12500 do
  -- random sample
  local input = dataset[i%400 + 1][1]
  local output = dataset[i%400 + 1][2]

  -- feed it to the neural network and the criterion
  criterion:forward(mlp:forward(input), output)

  -- train over this example in 3 steps
  -- (1) zero the accumulation of the gradients
  mlp:zeroGradParameters()
  -- (2) accumulate gradients
  mlp:backward(input, criterion:backward(mlp.output, output))
  -- (3) update parameters with a 0.01 learning rate
  mlp:updateParameters(0.01)
end

print(mlp)

print('--')


res = mlp:forward(torch.Tensor({1, 0, 0, 0}))
print(res:round())

res = mlp:forward(torch.Tensor({0, 1, 0, 0}))
print(res:round())

res = mlp:forward(torch.Tensor({0, 0, 1, 0}))
print(res:round())

res = mlp:forward(torch.Tensor({0, 0, 0, 1}))
print(res:round())
