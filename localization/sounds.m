clearvars;
close all;
clc;

% load in microphone data
load data1.mat

% set the mic that hit first to be ones for the entire row
hitFirst = 3;
data(:,hitFirst) = ones(size(data,1),1);

% plot data
figure(1); hold on;
plot(data(:,1));
plot(data(:,2));
plot(data(:,3));
legend('Mic 1', 'Mic 2', 'Mic 3');


% find times in seconds from sample number
tSamp = 7.55e-6;
t1 = (find(data(:,1),1)-1)*tSamp;
t2 = (find(data(:,2),1)-1)*tSamp;
t3 = (find(data(:,3),1)-1)*tSamp;