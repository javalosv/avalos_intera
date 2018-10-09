clc
clear all
close all
a = csvread('eq_me01.csv',1,0);
alfa=a(:,2);
time_process=a(:,3);

plot(a(:,4),a(:,5),'*-')
p=(a(end,5)-a(1,5))*(a(1,4)-a(end,4))
