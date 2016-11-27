require 'nn'
require 'optim'
require 'csvigo'
require './utils.lua'

-- The data are in a comma separated values (CSV) file. The first record
-- contains field names and subsequent records contain data. The fields and
-- their formats are:
-- - num: observation number; an integer surrounded by double quote chars
-- - brand: brand number; 1, 2, or 3 surrounded by double quote chars
-- - female: indicator for is-female: 1 if female, 0 otherwise; no quote chars
-- - age: age of the person; no quote characters

-- Reading CSV files can be tricky. This code uses the csvigo package for this:
loaded = csvigo.load('example-logistic-regression.csv')

----------------------------------------------------------------------
-- 2. Define the model (predictor)

softMaxLayer = nn.LogSoftMax()

model = nn.Sequential()
model:add(nn.Linear(470,980))
model:add(nn.Linear(980,7000))
model:add(softMaxLayer)

dataset = {}
----------------------------------------------------------------------
-- 3. Define a loss function, to be minimized.

criterion = nn.ClassNLLCriterion()

----------------------------------------------------------------------
-- 4.a. Train the model (Using SGD)

x, dl_dx = model:getParameters()

feval = function(x_new)
    -- set x to x_new, if differnt
    -- (in this simple example, x_new will typically always point to x,
    -- so the copy is really useless)
    if x ~= x_new then
        x:copy(x_new)
    end

    -- select a new training sample
    _nidx_ = (_nidx_ or 1) + 1
    if _nidx_ > #dataset then _nidx_ = 2 end

    local inputs, target = genInputsAndOutputs(dataset[_nidx_])
    -- reset gradients (gradients are always accumulated, to accomodate
    -- batch methods)
    print((#inputs)[1], (#target)[1])
    dl_dx:zero()

    -- evaluate the loss function and its derivative wrt x, for that sample
    local loss_x = criterion:forward(model:forward(inputs), target)
    model:backward(inputs, criterion:backward(model.output, target))

    -- return loss(x) and dloss/dx
    return loss_x, dl_dx
end

-- Given the function above, we can now easily train the model using SGD.
-- For that, we need to define four key parameters:
--   + a learning rate: the size of the step taken at each stochastic
--     estimate of the gradient
--   + a weight decay, to regularize the solution (L2 regularization)
--   + a momentum term, to average steps over time
--   + a learning rate decay, to let the algorithm converge more precisely

sgd_params = {
    learningRate = 1e-3,
    learningRateDecay = 1e-4,
    weightDecay = 0,
    momentum = 0
}

-- We're now good to go... all we have left to do is run over the dataset
-- for a certain number of iterations, and perform a stochastic update
-- at each iteration. The number of iterations is found empirically here,
-- but should typically be determinined using cross-validation (i.e.
-- using multiple folds of training/test subsets).

epochs = 1e2  -- number of times to cycle over our training data

print('')
print('============================================================')
print('Training with SGD')
print('')

for file in io.popen([[ls "../dataset_per_object" ]]):lines() do
    dataset = csvigo.load({path = "../dataset_per_object/" .. file, mode = "large"})
    print(file)
    print('')

    current_loss = 0

    for i = 2, #dataset do

        -- optim contains several optimization algorithms.
        -- All of these algorithms assume the same parameters:
        --   + a closure that computes the loss, and its gradient wrt to x,
        --     given a point x
        --   + a point x
        --   + some parameters, which are algorithm-specific

        _, fs = optim.sgd(feval, x, sgd_params)

        -- Functions in optim all return two things:
        --   + the new x, found by the optimization method (here SGD)
        --   + the value of the loss functions at all points that were used by
        --     the algorithm. SGD only estimates the function once, so
        --     that list just contains one value.

        current_loss = current_loss + fs[1]

        print('item = ' .. i .. ' current loss = ' .. current_loss)
    end

    -- report average error on epoch
    current_loss = current_loss / #dataset_inputs

    print('epoch = ' .. file .. ' current loss = ' .. current_loss)
end
