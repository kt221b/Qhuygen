%% Parte de Carga de datos

close all
clear all
clc
% Opens a folder and extracs all the csv files
selpath = uigetdir(path);
datedir = dir(fullfile(selpath,'*.csv'));

% Extract names and prepare cell for the data
filenames = {datedir.name}';
data_cell = cell(5,1);

% Extract the data matrices and build cell with names and data paired to
% each other
for i=1:5
    data_cell{i} = flip(table2array(readtable(string(strcat(selpath,'\',filenames(i))),'NumHeaderLines',1)),2);
end
data_cell=[filenames,data_cell];


% Prepare axes for plotting
dim=size(data_cell{1,2});
x=linspace(0, 100,dim(1));
y=linspace(0, 100,dim(2));

%% Plots not removing the background

figure(1)
imagesc(x,y,data_cell{1,2}'.*10^3)
colormap(gray);
a = colorbar
a.Title.String = 'mV';
addToolbarExplorationButtons(gcf)
%caxis([-10 10]);
xlabel('X (V)')
ylabel('Y (V)')
title(data_cell{1,1})
set(gca,'FontSize',16);
%graph size
x0=100;
y0=100;
width=575;
height=420;
set(gcf,'position',[x0,y0,width,height])
box on;


figure(2)
imagesc(x,y,data_cell{2,2}') % add .*10^3
colormap(redblue(10000));
a = colorbar
a.Title.String = 'mV';
addToolbarExplorationButtons(gcf)
%caxis([-10 10]);
xlabel('X (V)')
ylabel('Y (V)')
title(data_cell{2,1})
set(gca,'FontSize',16);
%graph size
x0=100;
y0=100;
width=575;
height=420;
set(gcf,'position',[x0,y0,width,height])
box on;


figure(3)
imagesc(x,y,data_cell{3,2}') % add .*10^3
colormap(redblue(10000));
a = colorbar
a.Title.String = 'mV';
addToolbarExplorationButtons(gcf)
%caxis([-10 10]);
xlabel('X (V)')
ylabel('Y (V)')
title(data_cell{3,1})
set(gca,'FontSize',16);
%graph size
x0=100;
y0=100;
width=575;
height=420;
set(gcf,'position',[x0,y0,width,height])
box on;


figure(4)
imagesc(x,y,data_cell{4,2}'.*10^3)
colormap(redblue(10000));
a = colorbar
a.Title.String = 'mV';
addToolbarExplorationButtons(gcf)
%caxis([-10 10]);
xlabel('X (V)')
ylabel('Y (V)')
title(data_cell{4,1})
set(gca,'FontSize',16);
%graph size
x0=100;
y0=100;
width=575;
height=420;
set(gcf,'position',[x0,y0,width,height])
box on;


figure(5)
imagesc(x,y,data_cell{5,2}'*10^3)
colormap(redblue(10000));
a = colorbar
a.Title.String = 'mV';
addToolbarExplorationButtons(gcf)
%caxis([-10 10]);
xlabel('X (V)')
ylabel('Y (V)')
title(data_cell{5,1})
set(gca,'FontSize',16);
%graph size
x0=100;
y0=100;
width=575;
height=420;
set(gcf,'position',[x0,y0,width,height])
box on;


%% Background sustraction

% Locate the position of Kerr and RMCD data. Could be done searching by
% filename
Kerr_index = 2;
RMCD_index = 3;

% Call Kerr plot, obtain binary mask with ROI
ax = imgca(figure(Kerr_index));
roi = images.roi.Freehand(Color='b');
draw(roi);
wait(roi);
binaryImage_subs = roi.createMask();
% roi_subs_im = labeloverlay(original_image, binaryImage_subs , transparency=.75, Colormap='jet');

% Obtain average of substrate, substract it and get range
Kerr = data_cell{Kerr_index,2}';
substrate_average_k = mean(Kerr(binaryImage_subs));
Kerr_bc = Kerr-substrate_average_k;
d = max(abs(Kerr_bc(:)));

% MOKE data
figure(10)
imagesc(x,y,(Kerr_bc))
colorbar
addToolbarExplorationButtons(gcf)
colormap(redblue(10000));
xlabel('X (V)')
ylabel('Kerr (a.u.)')
title('Kerr bc (mV)')
set(gca,'FontSize',16);
% clim([-6.5*1E-3 6.5*1E-3]);
clim([-0.06 0.06]);
% clim([-d d]);
%graph size
x0=100;
y0=100;
width=575;
height=420;
set(gcf,'position',[x0,y0,width,height])
box on;


% RMCD

ax = imgca(figure(RMCD_index));
roi = images.roi.Freehand(Color='b'); %create a ROI object
draw(roi);
wait(roi);
binaryImage_subs = roi.createMask();
% roi_subs_im = labeloverlay(original_image, binaryImage_subs , transparency=.75, Colormap='jet');
RMCD = data_cell{RMCD_index,2}';

substrate_average_r = mean(RMCD(binaryImage_subs));
RMCD_bc = RMCD-substrate_average_r;
d = max(abs(RMCD_bc(:)));

figure(20)
imagesc(x,y,(RMCD_bc))
colorbar
addToolbarExplorationButtons(gcf)
colormap(redblue(10000));
xlabel('X (V)')
ylabel('RMCD (a.u.)')
title('RMCD bc (mV)')
set(gca,'FontSize',16);
%clim([-1.5*1E-2 1.5*1E-2]);
clim([-0.05 0.05]);
% clim([-d d]);
%graph size
x0=100;
y0=100;
width=575;
height=420;
set(gcf,'position',[x0,y0,width,height])
box on;


%%
% Saving directory
mkdir(selpath,'figs')
savedir = append(selpath,'\figs');

for i = 1:5
    name = strrep(data_cell{i,1},'.csv','.fig');
    saveas(figure(i),append(savedir,name))
    name = strrep(data_cell{i,1},'.csv','.png');
    saveas(figure(i),append(savedir,name))
end


name = '\kerr_bc.fig';
saveas(figure(10),append(savedir,name))
name = '\kerr_bc.png';
saveas(figure(10),append(savedir,name))

name = '\RMCD_bc.fig';
saveas(figure(20),append(savedir,name))
name = '\RMCD_bc.png';
saveas(figure(20),append(savedir,name))








