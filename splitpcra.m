function [A, E] = splitpcra(D)
    % Split image to 50 x 50
    S = D(:,1:7500);
    [A, E] = pcra(S);
end