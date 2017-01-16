local dataset = {}

function dataset:size() return 400 end

for i=1, 4 do
  output = torch.zeros(4)
  output[i] = 1;
  for j=1, 100 do
    input = torch.zeros(48)
    for k=i, 48, 4 do
      input[k] = torch.random(i*2, i*3)
    end
    dataset[(i-1)*100 + j] = {output, input}
  end
end

torch.save('data/dataset.th', dataset)
