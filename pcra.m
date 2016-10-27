function [A, E] = pcra(D)
    A = zeros(size(D)); E = zeros(size(D));
    
    mu = 1.25 * norm(D); 
    rho = 1.5;
    lambda = 1 / sqrt(max(size(D)));
    
    sgn = sign(D); scl = max(norm(sgn), norm(sgn, inf) / lambda);
    Y = sgn / scl;
    
    % Keep oldA and oldE for convergence checking
    oldA = ones(size(A)); oldE = ones(size(A));
    
    % Check the convergence using 2-norm of the matrix
    while (norm(E - oldE) > 1e-4)
        oldE = E;
        while (norm(A - oldA) > 1e-4)
            oldA = A;
            [U, S, V] = svd(D - E + Y / mu);
            A = U * arrayfun(@(x) thresh('soft', x, 1 / mu), S) * V';
            E = arrayfun(@(x) thresh('soft', x, lambda / mu), D - A + Y / mu);
        end        
        Y = Y + mu * (D - A - E);
        mu = rho * mu;
    end
end