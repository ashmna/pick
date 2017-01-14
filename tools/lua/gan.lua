require 'nn';

dataset = torch.load('data/dataset.th')

pred_mlp = nn.Sequential()  -- A network that makes predictions given x.
pred_mlp:add(nn.Linear(4, 12))
pred_mlp:add(nn.Linear(12, 48))

xy_mlp = nn.ParallelTable() -- A network for predictions and for keeping the
xy_mlp:add(pred_mlp)        -- true label for comparison with a criterion
xy_mlp:add(nn.Identity())   -- by forwarding both x and y through the network.

mlp = nn.Sequential()       -- The main network that takes both x and y.
mlp:add(xy_mlp)             -- It feeds x and y to parallel networks;


cr = nn.MSECriterion()
cr_wrap = nn.CriterionTable(cr)
mlp:add(cr_wrap)            -- and then applies the criterion.

for i = 1, 400 do
  for j = 1, 1 do           -- Do a few training iterations
     x = dataset[i][1]
     y = dataset[i][2]

     err = mlp:forward{x, y}   -- Forward both input and output.
                    -- Print error from criterion.

     mlp:zeroGradParameters() -- Do backprop...
     mlp:backward({x, y})
     mlp:updateParameters(0.05)
  end
  print(err)
end
print('--')

res = xy_mlp:forward(torch.Tensor({0, 0, 0, 1}))
print(res)

res = xy_mlp:forward(torch.Tensor({1, 0, 0, 0}))
print(res)

res = xy_mlp:forward(torch.Tensor({0, 1, 0, 0}))
print(res)

res = xy_mlp:forward(torch.Tensor({0, 0, 1, 0}))
print(res)

-- criterion = nn.MSECriterion()
-- trainer = nn.StochasticGradient(mlp, criterion)
-- trainer.learningRate = 0.04
-- trainer:train(dataset)
--
-- cr_wrap = nn.CriterionTable(cr)
-- mlp:add(cr_wrap)            -- and then applies the criterion.
--
-- for i = 1, 100 do           -- Do a few training iterations
--    x = torch.ones(5)        -- Make input features.
--    y = torch.Tensor(3)
--    y:copy(x:narrow(1,1,3))  -- Make output label.
--    err = mlp:forward{x,y}   -- Forward both input and output.
--    print(err)               -- Print error from criterion.
--
--    mlp:zeroGradParameters() -- Do backprop...
--    mlp:backward({x, y})
--    mlp:updateParameters(0.05)
-- end
