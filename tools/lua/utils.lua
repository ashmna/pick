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
    -- months  [tonumber(month)]                     = 1
    hours   [tonumber(hour) + 1]                     = 1
    minuts  [math.floor(tonumber(min) / 5) + 1]      = 1
    return torch.cat(weekDays, hours, 1):cat(minuts, 1)
end

function genObjectInput(objId, maxObjectsCounts)
    local inputs = torch.zeros(maxObjectsCounts)
    inputs[tonumber(objId)] = 1
    return inputs
end

function file_exists(name)
    local f = io.open(name, "r")
    if f ~= nil then io.close(f) return true else return false end
end

function genOutMap(objId, dataset)
    local path = "../resources/lua/" .. objId .. "/out-map.th"
    local outMap = {}

    if file_exists(path) then
        outMap = torch.load(path)
        return outMap
    else
        outMap["indexCount"] = 0
    end

    local indexCount = tonumber(outMap["indexCount"])

    for i = 2, #dataset do
        local indexes = dataset[i][16]:split(",")

        for j = 1, #indexes do
            local index = tonumber(indexes[j])
            if index ~= 0 and outMap[index] == nil then
                indexCount = indexCount + 1
                outMap[index] = indexCount
            end
        end
    end

    outMap["indexCount"] = indexCount

    torch.save(path, outMap)
    return outMap;
end

function genOutnput(outMap, str)
    local indexCount = tonumber(outMap["indexCount"])
    local out = torch.zeros(indexCount)
    if str ~= "0" then
        local indexes = str:split(",")
        for i = 1, #indexes do
            out[outMap[tonumber(indexes[i])]] = 1
        end
    end
    return out
end

function genInputsAndOutputs(outMap, data)
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

    -- local objId   = data[1]
    local date    = data[2]
    local indexes = data[16]

    local input = torch.cat(genDateTimeInput(date), weather, 1) -- :cat(genObjectInput(objId, 403), 1)
    local output = genOutnput(outMap, indexes)

    return input, output
end

function genDataset(objId)
    local dataset = {};
    local path = "../resources/lua/".. objId.. "/dataset.th"
    local data = csvigo.load({path = "../resources/dataset_per_object/dataset_".. objId ..".csv", mode = "large"})
    local outMap = genOutMap(objId, data)

    for i = 2, #data do
        local input, output = genInputsAndOutputs(outMap, data[i])
        dataset[i-1] = {input, output}
    end
    torch.save(path, dataset)
    return dataset;
end

function getDataset(objId)
    local path = "../resources/lua/" .. objId .. "/dataset.th"
    if file_exists(path) then
        return torch.load(path)
    end
    return genDataset(objId)
end
