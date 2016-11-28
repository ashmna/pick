require "csvigo" -- luarocks install csvigo

function genDateTimeInput(str)
    local pattern = "(%d+)-(%d+)-(%d+) (%d+):(%d+):(%d+)"
    local year, month, day, hour, min, sec = str:match(pattern)
    local timestamp = os.time { year = year, month = month, day = day, hour = hour, min = min, sec = sec }
    local weekDays = torch.zeros(7)
    -- local months   = torch.zeros(12)
    local hours    = torch.zeros(24)
    local minuts   = torch.zeros(12)
    weekDays[(os.date("%w", timestamp) + 6) % 7 + 1] = 1
    -- months  [tonumber(month)]                        = 1
    hours   [tonumber(hour) + 1]                     = 1
    minuts  [math.floor(tonumber(min) / 5) + 1]      = 1
    return torch.cat(weekDays, hours, 1):cat(minuts, 1)
end

function genObjectInput(objId, maxObjectsCounts)
    local inputs = torch.zeros(maxObjectsCounts)
    inputs[tonumber(objId)] = 1
    return inputs
end

function genOutnput(str, maxOutnput)
    local out = torch.zeros(maxOutnput)
    if str ~= "0" then
        local indexes = str:split(",")
        for i = 1, #indexes do
            out[tonumber(indexes[i])] = 1
        end
    end
    return out
end

function genInputsAndOutputs(data)
    -- 1  objId
    -- 2  date
    -- 3  fog
    -- 4  rain
    -- 5  snow
    -- 6  hail
    -- 7  thunder
    -- 8  tornado
    -- 9  temp
    -- 10 dewptm
    -- 11 humidity
    -- 12 wind
    -- 13 wisibility
    -- 14 pressurem
    -- 15 indexesLength
    -- 16 indexes
    local weather = torch.zeros(12)
    for i = 1, 12 do
        weather[tonumber(i)] = tonumber(data[2 + i])
    end

    local objId   = data[1]
    local date    = data[2]
    local indexes = data[16]

    local input = torch.cat(genDateTimeInput(date), weather, 1) -- :cat(genObjectInput(objId, 403), 1)
    local output = genOutnput(indexes, 7000)

    return input, output
end

function genDataet()
    for file in io.popen([[ls "../dataset_per_object" ]]):lines() do
        local dataset = {}
        local data = csvigo.load({path = "../dataset_per_object/" .. file, mode = "large"})
        print(file)
        for i = 2, #data do
            local input, output = genInputsAndOutputs(data[i])
            dataset[i-1] = {input, output}
        end
        print("../normal_io_dataset/".. file:sub(1, -5) ..".th")
        torch.save("../normal_io_dataset/".. file:sub(1, -5) ..".th", dataset)
        print("======================")
    end
end

-- genDataet()
