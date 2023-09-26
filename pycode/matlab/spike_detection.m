function spikes = spike_detection(mat_folder, pkd_folder, varargin)
  thresh_vector = [];
  plp = 20;
  rp = 10;
  fs = 10000;
  art_thresh_analog = 1;
  art_thresh_elec = 200;
  art_dist = 200;
  nstd = 8;
  peak_detection_PTSD_mex_autThComp (plp, rp, fs, art_thresh_analog, ...
				     art_thresh_elec, art_dist, ...
				     thresh_vector, nstd, mat_folder, pkd_folder)
end
