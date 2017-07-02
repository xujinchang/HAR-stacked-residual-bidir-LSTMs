function out = imgresize(filename)


%   produce the motion blur picture
[filenames] = textread(filename,'%s%*[^\n]');

poech = 500;
%task_lists = [];
filenames_length = length(filenames)
parfor i = 1:floor(filenames_length/poech)
%for i = 1000:2000
	%filenames([(i-1)*poech+1:i*poech])
	task_lists = filenames([(i-1)*poech+1:i*poech]);
	ret = image_resize(task_lists);
end
if mod(filenames_length, poech) ~= 0
	floor((filenames_length/poech))*poech
	task_lists = filenames([floor((filenames_length/poech))*poech+1:end])
	ret = image_resize(task_lists);
end
out = true;
end
%spath2 = '/localSSD/xjc/quality_false/quality_motion_matlab/train'
function ret = image_resize(filenames)
%path1 = '/localSSD/xjc//quality_motion_matlab/test1/';
for j = 1:length(filenames)
	filename = char(filenames{j});
	img = imread(filename);
    img_small = imresize(img, 1. / 2,'bicubic');
	imwrite(img_small,filename);
ret = true;
end
end
