Sp = csvread('S_data.txt');
Ik = csvread('IK_data.txt');
l1=length(Sp);
l2=length(Ik);
t1=0.01*[1:l1];
t2=0.01*[1:l2];
%%
figure
subplot(1,2,1);
legend
for n=8:14   
    plot (t2,Ik(:,n))
    hold on
    legend
end
title('Posicion con Cinematica Inversa')

subplot(1,2,2);
legend
for n=8:14  
    plot (t1,Sp(:,n))
    hold on
    legend
end
title('Posicion con Spline')

%%
close allmatlab 
t=[0.0, 0.80083980289165202, 1.3947028509558959, 2.0645919507093304, 2.87534401171663, 3.3883570916019683, 4.1456175170202298]
t=t+0.7*ones(1,7)
y=[1.14619792,1.47199018 ,1.52219344 ,0.84023607,1.54618081, 1.58509851, 1.11148708]
plot (t2,Ik(:,4),'r-')
hold on
plot (t1,Sp(:,4),'b-')
plot (t,y,'bo')
legend
