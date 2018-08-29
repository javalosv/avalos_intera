close all
figure
plot(v_t,v_jk,'b:*',...
    'LineWidth',0.5,...
    'MarkerSize',7,...
    'MarkerEdgeColor','r')
grid on
grid minor
text(v_t(1)-0.5,v_jk(1)+4,'{\alpha =0.10}','Rotation',90)
text(v_t(2)-0.5,v_jk(2)+4,'{\alpha =0.15}','Rotation',90)
text(v_t(3)-0.5,v_jk(3)+4,'{\alpha =0.20}','Rotation',90)
%text(v_t(4)-0.5,v_jk(4)+2,'{\alpha =0.25}','Rotation',90)
text(v_t(5)+0.5,v_jk(5)+4,'{\alpha =0.30}','Rotation',90)
text(v_t(6)-0.5,v_jk(6)+4,'{\alpha =0.35}','Rotation',90)
text(v_t(7)-0.5,v_jk(7)+4,'{\alpha =0.40}','Rotation',90)
text(v_t(8)-0.5,v_jk(8)+4,'{\alpha =0.45}','Rotation',90)
text(v_t(9)-0.5,v_jk(9)+4,'{\alpha =0.50}','Rotation',90)
%text(v_t(10)-0.5,v_jk(10)+2,'{\alpha =0.55}','Rotation',90)
text(v_t(11)-0.5,v_jk(11)+4,'{\alpha =0.60}','Rotation',90)
%text(v_t(12)-0.5,v_jk(12)+2,'{\alpha =0.65}','Rotation',90)
%text(v_t(13)+0.5,v_jk(13)+2,'{\alpha =0.70}','Rotation',90)
text(v_t(14)+0.5,v_jk(14)+4,'{\alpha =0.75}','Rotation',90)
text(v_t(15)-0.5,v_jk(15)+4,'{\alpha =0.80}','Rotation',90)
text(v_t(16)+0.5,v_jk(16)+4,'{\alpha =0.85}','Rotation',90)
text(v_t(17)+0.5,v_jk(17)+4,'{\alpha =0.90}','Rotation',90)
text(v_t(18),v_jk(18)+4,'{\alpha =0.95}','Rotation',90)
%figure 
xlabel("Accumulated time")
ylabel("Accumulated jerk")
axis([15 85 0 150])
%plot(alfa,time,'o-')
