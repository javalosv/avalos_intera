clear all;
clc
f=100
k=2.5
t=(linspace(0,k*6,6*k*100))';
filename = 'data_send_6_58_07_07.txt';
P = csvread(filename);

z=length(P),% size

V = zeros(z,7);
A = zeros(z,7);
J = zeros(z,7);

for i=1:7
    for j=1:z-1
        V(j,i)=P(j+1,i)-P(j,i);
    end
    V(z,:)=V(z-1,:);
end

for i=1:7
    for j=1:z-1
        A(j,i)=V(j+1,i)-V(j,i);
    end
    A(z-1,:)=A(z-2,:);
    A(z,:)=A(z-1,:);
end


for i=1:7
    for j=1:z-1
        J(j,i)=A(j+1,i)-A(j,i);
    end
    J(z-2,:)=J(z-3,:);
    J(z-1,:)=J(z-2,:);
    J(z,:)=J(z-1,:);
end

figure;
subplot(2,2,1);
hold on
plot(t,P(:,1))
plot(t,P(:,2))
plot(t,P(:,3))
plot(t,P(:,4))
plot(t,P(:,5))
plot(t,P(:,6))
%plot(t,P(:,7))
title('Posición joint')
xlabel('t(s)')
ylabel('theta')


subplot(2,2,2);
hold on
plot(t,V(:,1))
plot(t,V(:,2))
plot(t,V(:,3))
plot(t,V(:,4))
plot(t,V(:,5))
plot(t,V(:,6))
%plot(t,V(:,7))
title('Velocidad joint')
xlabel('t(s)')
ylabel('theta/s')


subplot(2,2,3);
hold on
plot(t,A(:,1))
plot(t,A(:,2))
plot(t,A(:,3))
plot(t,A(:,4))
plot(t,A(:,5))
plot(t,A(:,6))
%plot(t,A(:,7))
title('Aceleración joint')
xlabel('t(s)')
ylabel('theta/s²')


subplot(2,2,4);
hold on
plot(t,J(:,1))
plot(t,J(:,2))
plot(t,J(:,3))
plot(t,J(:,4))
plot(t,J(:,5))
plot(t,J(:,6))
%plot(t,J(:,7))
title('Jerk joint')
xlabel('t(s)')
ylabel('theta/s³')
