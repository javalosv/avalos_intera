close all
clc
alfa=[0.10,0.15,0.20,0.30,0.40,0.50,0.60,0.80,0.85,0.90,0.95];
jerk=[2.84,3.51,4.54,6.52,8.53,10.71,14.42,21.39,27.46,36.10,49.40];
time=[80.4,72.78,64.32,54.60,47.7,42.66,37.02,30.78,26.88,23.76,20.22];
figure
plot(time,jerk,'b:*',...
    'LineWidth',0.5,...
    'MarkerSize',7,...
    'MarkerEdgeColor','r')
hold on

plot(49.92,17.53,'b*')
viscircles([49.92,17.53],1.75)

text(time(1)-0.5,jerk(1)+2,'{\alpha =0.10}','Rotation',90)
text(time(2)-0.5,jerk(2)+2,'{\alpha =0.15}','Rotation',90)
text(time(3)-0.5,jerk(3)+2,'{\alpha =0.20}','Rotation',90)
%text(time(4)-0.5,jerk(4)+2,'{\alpha =0.25}','Rotation',90)
text(time(4)-0.5,jerk(4)+2,'{\alpha =0.30}','Rotation',90)
%%text(time(5)-0.5,jerk(5)+2,'{\alpha =0.35}','Rotation',90)
text(time(5)-0.5,jerk(5)+2,'{\alpha =0.40}','Rotation',90)
%text(time(6)-0.5,jerk(6)+2,'{\alpha =0.45}','Rotation',90)
text(time(6)-0.5,jerk(6)+2,'{\alpha =0.50}','Rotation',90)
%text(time(10)-0.5,jerk(10)+2,'{\alpha =0.55}','Rotation',90)
text(time(7)-0.5,jerk(7)+2,'{\alpha =0.60}','Rotation',90)
%text(time(12)-0.5,jerk(12)+2,'{\alpha =0.65}','Rotation',90)
%text(time(13)+0.5,jerk(13)+2,'{\alpha =0.70}','Rotation',90)
%text(time(8)+0.5,jerk(8)+2,'{\alpha =0.75}','Rotation',90)
text(time(8)-0.5,jerk(8)+2,'{\alpha =0.80}','Rotation',90)
text(time(9)+0.5,jerk(9)+2,'{\alpha =0.85}','Rotation',90)
text(time(10)+0.5,jerk(10)+2,'{\alpha =0.90}','Rotation',90)
text(time(11),jerk(11)+2,'{\alpha =0.95}','Rotation',90)

xlabel("Accumulate time")
ylabel("Accumulate jerk")
axis([15 85 0 70])
grid on
grid minor