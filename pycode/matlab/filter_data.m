function filter_data(src_dir, dst_dir, varargin)
  if nargin > 0
    params.filterType = varargin{1};
    params.cutOffFreq = varargin{2};
    params.sf = varargin{3};
  else
    params.filterType = 'high';
    params.cutOffFreq = 70;
    params.sf = 10000;
  end
  filter_comput(src_dir, dst_dir, params);
end
