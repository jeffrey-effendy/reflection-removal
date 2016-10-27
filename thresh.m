function [xo,N]=thresh(ttype,xi,lambda)
    if nargin~=3;
      error('Wrong number of input arguments.');
    end;

    if (numel(lambda)~=1 || ~isnumeric(lambda))
      error('lambda must be a scalar.');
    end;

    if ischar(ttype)
      ttype=lower(ttype);
    end;

    switch ttype
      case {'hard',1}
        xo=xi.*(abs(xi)>=lambda);
      case {'soft',2}
        xa=abs(xi)-lambda;
        xo=((xa>0)*xa+0).*sign(xi);
      otherwise
        error('Unknown thresholding type.');
    end;

    if nargout==2
      work=(abs(xi)>=lambda);
      N=sum(work(:));
    end;
end