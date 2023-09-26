function OK = convert_mcd(path)
  % convert_mcd convert mcd at given PATH
  % if PATH is a dir convert all mcd in it, else just the one relative to that
  % path

  menu_ImportMCD();
  
  chs = ones(1,64);
  chs(1) = 0;
  chs(8) = 0;
  chs(57) = 0;
  chs(64) = 0;
  idChAct = chs;
  
  extension = 'mcd';

  output = 'uV';

  performFilteringChosen = 1;
  cutOffFrequenciesChosen = 100;

  rawDataConversionFlag = 1;
  datConversionFlag = 0;
  matConversionFlag = 1;
  anaConversionFlag = 1;
  setOffsetToZeroFlag = 1;
  filtConversionFlag = 0;
  nMeas = 1;
  
  if exist(path, 'dir')
    startFolder = path;
    list_mcd_files = [];

    path_split = strsplit(path, "/");
    outFoldersChosen = strcat(path, "/", extractBefore(path_split(end), "_"));
    
    mcd_files = listdir(path, "mcd");
    num_files = numel(mcd_files)/2;
    
    for i=1:num_files
      expNamesChosen = extractBefore(mcd_files{i, 1}, ".mcd");
      fileName = strcat(path, "/", mcd_files{i, 1});
      disp(fileName)

      convertOnExtension_ns(extension, idChAct, output, startFolder, fileName,...
			    expNamesChosen, outFoldersChosen, performFilteringChosen, ...
			    cutOffFrequenciesChosen, rawDataConversionFlag,datConversionFlag, ...
			    matConversionFlag, anaConversionFlag,...
			    setOffsetToZeroFlag, filtConversionFlag, nMeas);
    end
    
  elseif exist(path, 'file')
				% separate the path of file from the file name
    [startFolder, expNamesChosen, ext] = fileparts(path);
    outFoldersChosen = strcat(pwd, "/", expNamesChosen);
    convertOnExtension_ns(extension, idChAct, output, startFolder, path,...
			  {expNamesChosen}, {outFoldersChosen}, {performFilteringChosen}, ...
			  {cutOffFrequenciesChosen}, rawDataConversionFlag, datConversionFlag, ...
			  matConversionFlag, anaConversionFlag,...
			  setOffsetToZeroFlag, filtConversionFlag, nMeas);
    
  else
    disp([path 'is nor a file or a directory'])
    OK = false

  end

  OK = true;
end
